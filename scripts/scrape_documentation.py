import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

#Where we save the documentation pages from wiki
OUTPUT_DIR = Path("data_sources/documentation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#Set of OpenEMR docs I want in the knowledge base
DOC_URLS = [
    "https://www.open-emr.org/wiki/index.php/OpenEMR_Wiki_Home_Page",
    "https://www.open-emr.org/wiki/index.php/OpenEMR_Installation_Guides",
    "https://www.open-emr.org/wiki/index.php/OpenEMR_Upgrade_Guides",
    "https://www.open-emr.org/wiki/index.php/OpenEMR_7.0.0_Users_Guide",
    "https://www.open-emr.org/wiki/index.php/OpenEMR_7.0.0_API",
    "https://www.open-emr.org/wiki/index.php/Patient_Portal",
    "https://www.open-emr.org/wiki/index.php/Securing_OpenEMR",
]
#Remove excessive blank lines and spacing
def clean_text(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()

def scrape_wiki_page(url):
    #Download page
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    #Grab page title
    title_tag = soup.find("h1")

    if title_tag:
        title = title_tag.get_text(" ", strip=True)
    else:
        title = soup.title.get_text(" ", strip=True)

    #MediaWiki stores article content here
    content = soup.find("div", {"id": "mw-content-text"})

    #Fallback just in case page structure changes
    if not content:
        content = soup.body

    #Remove stuff I don't want in embeddings
    for unwanted in content.select(
        "script, style, table.toc, div.printfooter, div.catlinks"
    ):
        unwanted.decompose()

    text = clean_text(
        content.get_text("\n", strip=True)
    )

    return {
        "source_type": "documentation",
        "document_type": "website",
        "title": title,
        "url": url,
        "content": text,
    }

#normalize filename so it doesn't have crazy title and is windows friendly
def safe_filename(title):
    name = title.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)

    return name.strip("_")[:80] + ".json"



def main():

    for url in DOC_URLS:

        print(f"Scraping: {url}")

        try:
            document = scrape_wiki_page(url)

            output_path = OUTPUT_DIR / safe_filename(
                document["title"]
            )

            #Save page as JSON so later stages don't need to rescrape
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(
                    document,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            print(f"Saved: {output_path}")

        except requests.exceptions.HTTPError as e:
            #Skip bad links and keep going
            print(f"Skipped bad URL: {url}")
            print(f"Reason: {e}")

        except Exception as e:
            #Catch unexpected issues so one page does not stop the scrape
            print(f"Failed to scrape: {url}")
            print(f"Reason: {e}")

        #Be nice to the server, pause 1 sec between requests
        time.sleep(1)


if __name__ == "__main__":
    main()