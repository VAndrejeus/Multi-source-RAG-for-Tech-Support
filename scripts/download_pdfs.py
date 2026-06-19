from pathlib import Path

import requests

#Where we save PDF manuals
OUTPUT_DIR = Path("data_sources/documentation/pdfs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#Download 2 user guide pdfs
PDF_URLS = {
    "openemr_4_1_users_guide.pdf": "https://www.open-emr.org/files/OpenEMR_4.1_Users_Guide_V1.pdf",
    "openemr_3_1_users_guide.pdf": "https://www.open-emr.org/files/OpenEMR_3.1_Users_Guide.pdf",
}


def download_pdf(filename, url):

    print(f"Downloading: {url}")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    output_path = OUTPUT_DIR / filename

    #Save PDF locally  for further processing with PYPDF
    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Saved: {output_path}")


def main():

    for filename, url in PDF_URLS.items():

        try:
            download_pdf(filename, url)

        except Exception as e:

            #Continue, even if one pdf is broken
            print(f"Failed: {url}")
            print(f"Reason: {e}")


if __name__ == "__main__":
    main()