import json
import re
from pathlib import Path

from sentence_transformers import SentenceTransformer, util

#Input folders
DOC_DIR = Path("data_sources/documentation")
PDF_PROCESSED_DIR = Path("data_sources/documentation/pdf_processed")
BLOG_DIR = Path("data_sources/blogs")
FORUM_DIR = Path("data_sources/forums")

#Output folder
OUTPUT_DIR = Path("data_sources/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#Embedding model for semantic chunking
model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_text(text):

    #Normalize spacing before chunking
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def word_count(text):

    return len(text.split())


def split_paragraphs(text):

    #Paragraphs give better boundaries than raw word splitting
    paragraphs = text.split("\n\n")

    return [
        clean_text(p)
        for p in paragraphs
        if word_count(p) >= 15
    ]


def semantic_chunks(text, max_words, min_words, similarity_threshold):

    #Split document into paragraph-sized units
    paragraphs = split_paragraphs(text)

    if not paragraphs:
        return []

    #Create embeddings for semantic similarity comparisons
    embeddings = model.encode(
        paragraphs,
        convert_to_tensor=True
    )

    chunks = []
    current_chunk = [paragraphs[0]]
    current_words = word_count(paragraphs[0])

    for i in range(1, len(paragraphs)):

        prev_embedding = embeddings[i - 1]
        current_embedding = embeddings[i]

        #Measure how closely related neighboring paragraphs are
        similarity = util.cos_sim(
            prev_embedding,
            current_embedding
        ).item()

        next_words = word_count(paragraphs[i])

        #Start a new chunk when topic similarity drops
        should_split = (
            similarity < similarity_threshold
            and current_words >= min_words
        )

        #Prevent chunks from becoming too large
        too_large = current_words + next_words > max_words

        if should_split or too_large:

            chunks.append(
                "\n\n".join(current_chunk)
            )

            current_chunk = [paragraphs[i]]
            current_words = next_words

        else:

            #Keep related paragraphs together
            current_chunk.append(paragraphs[i])
            current_words += next_words

    #Save final chunk
    if current_chunk:
        chunks.append(
            "\n\n".join(current_chunk)
        )

    return chunks


def load_json_files(folder):

    return list(folder.glob("*.json"))


def chunk_documentation():

    chunks = []
    chunk_id = 0

    #Load wiki documentation and processed PDF documents
    json_files = load_json_files(DOC_DIR)

    if PDF_PROCESSED_DIR.exists():
        json_files += load_json_files(PDF_PROCESSED_DIR)

    for file_path in json_files:

        with open(file_path, "r", encoding="utf-8") as f:
            document = json.load(f)

        #Documentation uses medium-sized semantic chunks
        doc_chunks = semantic_chunks(
            document["content"],
            max_words=500,
            min_words=120,
            similarity_threshold=0.45
        )

        for chunk_number, chunk_text in enumerate(doc_chunks):

            chunk_id += 1

            chunks.append({
                "chunk_id": f"doc_{chunk_id}",
                "source_type": "documentation",
                "document_type": document.get("document_type", ""),
                "title": document.get("title", ""),
                "url": document.get("url", ""),
                "chunk_number": chunk_number,
                "chunk_text": chunk_text,
            })

    return chunks


def chunk_blogs():

    chunks = []
    chunk_id = 0

    for file_path in load_json_files(BLOG_DIR):

        with open(file_path, "r", encoding="utf-8") as f:
            document = json.load(f)
        #Blogs benefit from slightly larger chunks
        blog_chunks = semantic_chunks(
            document["content"],
            max_words=600,
            min_words=150,
            similarity_threshold=0.42
        )

        for chunk_number, chunk_text in enumerate(blog_chunks):

            chunk_id += 1

            chunks.append({
                "chunk_id": f"blog_{chunk_id}",
                "source_type": "blog",
                "document_type": document.get("document_type", ""),
                "title": document.get("title", ""),
                "url": document.get("url", ""),
                "chunk_number": chunk_number,
                "chunk_text": chunk_text,
            })

    return chunks


def chunk_forums():

    chunks = []
    chunk_id = 0

    for file_path in load_json_files(FORUM_DIR):

        with open(file_path, "r", encoding="utf-8") as f:
            thread = json.load(f)

        title = thread.get("title", "")
        url = thread.get("url", "")
        #Original question becomes its own chunk
        question = clean_text(thread.get("question", ""))

        if question:

            chunk_id += 1

            chunks.append({
                "chunk_id": f"forum_{chunk_id}",
                "source_type": "forum",
                "document_type": thread.get("document_type", ""),
                "title": title,
                "url": url,
                "chunk_type": "question",
                "chunk_text": question,
            })
        #Keep forum replies as separate retrieval units
        for reply_index, reply in enumerate(thread.get("replies", [])):

            reply_text = clean_text(reply.get("content", ""))
            #Skip very short replies that add little retrieval value
            if word_count(reply_text) < 10:
                continue

            chunk_id += 1

            chunks.append({
                "chunk_id": f"forum_{chunk_id}",
                "source_type": "forum",
                "document_type": thread.get("document_type", ""),
                "title": title,
                "url": url,
                "chunk_type": "reply",
                "reply_index": reply_index,
                "author": reply.get("author", ""),
                "created_at": reply.get("created_at", ""),
                "authority_score": 1,
                "chunk_text": reply_text,
            })

    return chunks


def save_chunks(filename, chunks):

    output_path = OUTPUT_DIR / filename

    #Save chunks separately so we can inspect each source type
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved {len(chunks)} chunks to {output_path}")


def main():

    documentation_chunks = chunk_documentation()
    blog_chunks = chunk_blogs()
    forum_chunks = chunk_forums()

    save_chunks("documentation_chunks.json", documentation_chunks)
    save_chunks("blog_chunks.json", blog_chunks)
    save_chunks("forum_chunks.json", forum_chunks)

    print("Chunking complete")


if __name__ == "__main__":
    main()