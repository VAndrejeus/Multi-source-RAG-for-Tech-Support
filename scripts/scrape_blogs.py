import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

#Where blog articles go
OUTPUT_DIR = Path("data_sources/blogs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#OpenEMR blog homepage
BLOG_HOME = "https://www.open-emr.org/blog/"

#Pull 10 articles 
MAX_ARTICLES = 10


def clean_text(text):

    #Remove excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def safe_filename(title):

    #Nromalize title to remove weird characters
    name = title.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)

    return name.strip("_")[:80] + ".json"


def get_blog_urls():

    #Homepage already has the article links we need
    response = requests.get(BLOG_HOME, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    urls = []

    for link in soup.find_all("a", href=True):

        href = link["href"].strip()

        if href.startswith("https://www.open-emr.org/blog/"):
            if href != BLOG_HOME and not href.endswith("index.xml"):
                urls.append(href)

    #Remove duplicates but keep order
    unique_urls = list(dict.fromkeys(urls))

    return unique_urls[:MAX_ARTICLES]


def scrape_blog_article(url):

    #Download article page
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    #Grab article title
    title_tag = soup.find("h1")

    if title_tag:
        title = title_tag.get_text(" ", strip=True)
    else:
        title = soup.title.get_text(" ", strip=True)

    #Most useful content lives in paragraph tags
    paragraphs = [
        p.get_text(" ", strip=True)
        for p in soup.find_all("p")
    ]

    content = clean_text(
        "\n\n".join(paragraphs)
    )

    return {
        "source_type": "blog",
        "document_type": "website",
        "title": title,
        "url": url,
        "content": content,
    }


def main():

    urls = get_blog_urls()

    print(f"Found {len(urls)} blog articles")

    for url in urls:

        print(f"Scraping: {url}")

        try:

            article = scrape_blog_article(url)

            output_path = OUTPUT_DIR / safe_filename(
                article["title"]
            )

            #Store raw article before chunking
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(
                    article,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            print(f"Saved: {output_path}")

        except Exception as e:

            #Don't let one bad article stop the scrape
            print(f"Failed: {url}")
            print(f"Reason: {e}")


if __name__ == "__main__":
    main()