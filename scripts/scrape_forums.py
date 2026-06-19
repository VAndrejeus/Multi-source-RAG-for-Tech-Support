import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

#This is where the forum posts go
OUTPUT_DIR = Path("data_sources/forums")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#OpenEMr uses Discourse, load lates topics json
LATEST_URL = "https://community.open-emr.org/latest.json"

#10 thread max here should be good
MAX_THREADS = 10


def clean_text(text):

    #Normalize, remove all extra white space, blank lines, etc..
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def clean_html(html):

    #Forum posts come as HTML, so strip tags
    soup = BeautifulSoup(html, "html.parser")
    return clean_text(
        soup.get_text(" ", strip=True)
    )


def safe_filename(title):

    #Convert thread title into regular filenames
    name = title.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)

    return name.strip("_")[:80] + ".json"


def get_latest_topics():

    #Get recent forum topics 
    response = requests.get(LATEST_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    return data["topic_list"]["topics"][:MAX_THREADS]


def get_topic_detail(topic_id):

    #Forum topic detail endpoint
    url = f"https://community.open-emr.org/t/{topic_id}.json"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.json(), url


def scrape_topic(topic):

    topic_id = topic["id"]

    data, url = get_topic_detail(topic_id)

    posts = data["post_stream"]["posts"]

    #First post is usually the question/problem
    question = clean_html(posts[0].get("cooked", "")) if posts else ""

    replies = []

    for post in posts[1:]:

        replies.append({
            "author": post.get("username", ""),
            "content": clean_html(post.get("cooked", "")),
            "created_at": post.get("created_at", "")
        })

    return {
        "source_type": "forum",
        "document_type": "discourse_thread",
        "title": data.get("title", ""),
        "url": url,
        "category_id": data.get("category_id", ""),
        "created_at": data.get("created_at", ""),
        "question": question,
        "replies": replies,
    }


def main():

    topics = get_latest_topics()

    print(f"Found {len(topics)} forum topics")

    for topic in topics:

        print(f"Scraping: {topic['title']}")

        try:

            thread = scrape_topic(topic)

            output_path = OUTPUT_DIR / safe_filename(
                thread["title"]
            )

            #Store raw forum thread before chunking
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(
                    thread,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            print(f"Saved: {output_path}")

        except Exception as e:

            #Don't let one bad thread stop the scrape
            print(f"Failed: {topic['title']}")
            print(f"Reason: {e}")


if __name__ == "__main__":
    main()