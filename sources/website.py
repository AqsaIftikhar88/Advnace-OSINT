# sources/website.py

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def extract_emails(text, domain):

    pattern = rf"[a-zA-Z0-9_.+-]+@{re.escape(domain)}"

    return set(re.findall(pattern, text))


def extract_phones(text):

    pattern = r"(?:\+92|0)?[0-9]{10,12}"

    return set(re.findall(pattern, text))


def extract_socials(html):

    socials = []

    social_patterns = {
        "Facebook": r"facebook\.com",
        "Twitter": r"twitter\.com|x\.com",
        "LinkedIn": r"linkedin\.com",
        "Instagram": r"instagram\.com",
        "YouTube": r"youtube\.com"
    }

    for platform, pattern in social_patterns.items():

        matches = re.findall(
            rf'https?://[^\s"\']*{pattern}[^\s"\']*',
            html
        )

        for match in matches:
            socials.append({
                "platform": platform,
                "url": match
            })

    return socials


def scan_website(domain):

    results = []

    visited_emails = set()

    pages = [
        "",
        "/contact",
        "/contact-us",
        "/about",
        "/about-us",
        "/staff",
        "/team",
        "/faculty",
        "/directory",
        "/administration",
        "/admissions"
    ]

    for path in pages:

        url = f"https://{domain}{path}"

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            text = soup.get_text(" ", strip=True)

            # =========================
            # EMAIL EXTRACTION
            # =========================

            emails = extract_emails(text, domain)

            for email in emails:

                if email in visited_emails:
                    continue

                visited_emails.add(email)

                results.append({
                    "type": "email",
                    "email": email,
                    "username": email.split("@")[0],
                    "domain": domain,
                    "source": "Website",
                    "page": url
                })
                
            # =========================
            # PHONE EXTRACTION
            # =========================

            # phones = extract_phones(text)

            # for phone in phones:

            #     results.append({
            #         "type": "phone",
            #         "phone": phone,
            #         "source": "Website",
            #         "page": url
            #     })

            # =========================
            # SOCIAL LINKS
            # =========================

            socials = extract_socials(response.text)

            for social in socials:

                results.append({
                    "type": "social",
                    "platform": social["platform"],
                    "url": social["url"],
                    "source": "Website",
                    "page": url
                })

            # =========================
            # INTERNAL LINKS
            # =========================

            links = soup.find_all("a", href=True)

            for link in links:

                href = link["href"]

                full_url = urljoin(url, href)

                # PDF Detection
                if ".pdf" in full_url:

                    results.append({
                        "type": "document",
                        "document": full_url,
                        "source": "Website"
                    })

        except Exception as e:

            print(f"Website scan error ({url}): {e}")

    return results