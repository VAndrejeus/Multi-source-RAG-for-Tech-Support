import sys
from pathlib import Path

import ollama

#Allow imports from scripts folder
sys.path.append(str(Path(__file__).parent))

from retrieval import retrieve

#Using Gemma 2:9b here as I alway do, most reliable and good enough for most things
OLLAMA_MODEL = "gemma2:9b"


def build_context(results, max_chunks=5):

    #Only send the best chunks to the LLM
    selected = results[:max_chunks]

    context_blocks = []

    for i, result in enumerate(selected, start=1):

        block = f"""
Source {i}
Title: {result["title"]}
Source Type: {result["source_type"]}
URL: {result["url"]}

{result["text"]}
"""
        context_blocks.append(block)

    return "\n\n".join(context_blocks), selected


def build_prompt(question, context):

    #Keep the model grounded in retrieved context
    return f"""
You are a technical support assistant for OpenEMR.

Answer the user's question using only the retrieved context below.
If the context does not contain enough information, say that the available sources do not provide enough detail.
Prefer official documentation over blogs and forums when sources disagree.

Retrieved Context:
{context}

User Question:
{question}

Answer:
"""


def generate_answer(question):

    results = retrieve(question)

    context, selected_sources = build_context(results)

    prompt = build_prompt(question, context)

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    return answer, selected_sources


def main():

    question = input("Ask an OpenEMR support question: ")

    answer, sources = generate_answer(question)

    print("\nAnswer:\n")
    print(answer)

    print("\nSources Used:\n")

    for source in sources:
        print(f"- {source['source_type']} | {source['title']} | {source['url']}")


if __name__ == "__main__":
    main()