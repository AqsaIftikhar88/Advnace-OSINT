import requests
import re
import io
import pdfplumber

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def extract_emails(text, pattern):
    return set(pattern.findall(text))


def process_pdf(session, pdf_url, pattern, found):

    results = []

    try:
        pdf_response = session.get(
            pdf_url,
            timeout=20
        )

        pdf_file = io.BytesIO(pdf_response.content)

        with pdfplumber.open(pdf_file) as pdf:

            full_text = []

            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)

            emails = extract_emails(
                "\n".join(full_text),
                pattern
            )

            for email in emails:

                if email in found:
                    continue

                found.add(email)

                results.append({
                    "type": "email",
                    "email": email,
                    "username": email.split("@")[0],
                    "source": "PDF",
                    "pdf": pdf_url
                })

    except Exception as e:
        print("PDF Error:", pdf_url, e)

    return results


def scan_pdf(domain):

    results = []

    found = set()

    base_url = f"https://{domain}"

    email_pattern = re.compile(
        rf"[a-zA-Z0-9_.+-]+@{re.escape(domain)}",
        re.IGNORECASE
    )

    session = requests.Session()
    session.headers.update(HEADERS)

    try:

        r = session.get(
            base_url,
            timeout=15
        )

        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )

        pdf_links = set()

        for link in soup.find_all("a", href=True):

            href = link["href"]

            full_url = urljoin(base_url, href)

            if full_url.lower().endswith(".pdf"):
                pdf_links.add(full_url)

        # Parallel PDF processing
        with ThreadPoolExecutor(max_workers=10) as executor:

            futures = [
                executor.submit(
                    process_pdf,
                    session,
                    pdf_url,
                    email_pattern,
                    found
                )
                for pdf_url in pdf_links
            ]

            for future in as_completed(futures):
                results.extend(future.result())

    except Exception as e:
        print("PDF Scanner Error:", e)

    finally:
        session.close()

    return results