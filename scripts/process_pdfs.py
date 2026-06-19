import json
import re
from pathlib import Path

from pypdf import PdfReader

#PDF location
PDF_DIR = Path("data_sources/documentation/pdfs")

#Where extracted text from PDFs go
OUTPUT_DIR = Path("data_sources/documentation/pdf_processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text):

    #Remove excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def safe_filename(filename):

    #Normalize JSON filename from the PDF filename
    name = filename.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)

    return name.strip("_") + ".json"


def process_pdf(pdf_path):

    print(f"Processing: {pdf_path}")

    reader = PdfReader(str(pdf_path))

    pages = []

    for i, page in enumerate(reader.pages):

        #Extract text page by page so one weird page does not break everything
        text = page.extract_text() or ""

        pages.append(
            f"\n\n--- Page {i + 1} ---\n\n{text}"
        )

    document = {
        "source_type": "documentation",
        "document_type": "pdf",
        "title": pdf_path.stem,
        "url": str(pdf_path),
        "content": clean_text("\n".join(pages)),
    }

    output_path = OUTPUT_DIR / safe_filename(pdf_path.stem)

    #Save extracted PDF text as JSON for chunking
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            document,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved: {output_path}")


def main():

    pdf_files = list(PDF_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDFs")

    for pdf_path in pdf_files:

        try:
            process_pdf(pdf_path)

        except Exception as e:

            #Keep going if one PDF fails
            print(f"Failed: {pdf_path}")
            print(f"Reason: {e}")


if __name__ == "__main__":
    main()