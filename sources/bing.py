# sources/bing.py

import requests
import re
from bs4 import BeautifulSoup

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

def scan_bing(domain):

    results = []

    found_emails = set()

    visited_links = set()

    queries = [
        f'site:{domain} "@{domain}"',
        f'site:{domain} contact',
        f'site:{domain} staff',
        f'site:{domain} faculty',
        f'site:{domain} team'
    ]

    for query in queries:

        bing_url = (
            "https://www.bing.com/search?"
            f"q={query}"
        )

        try:

            response = requests.get(
                bing_url,
                headers=HEADERS,
                timeout=10
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            links = soup.find_all("a", href=True)

            for link in links:

                href = link["href"]

                if domain not in href:
                    continue

                if href in visited_links:
                    continue

                visited_links.add(href)

                try:

                    page = requests.get(
                        href,
                        headers=HEADERS,
                        timeout=10
                    )

                    text = page.text

                    emails = extract_emails(
                        text,
                        domain
                    )

                    for email in emails:

                        if email in found_emails:
                            continue

                        found_emails.add(email)

                        results.append({

                            "type": "email",

                            "email": email,

                            "username": email.split("@")[0],

                            "domain": domain,

                            "source": "Bing",

                            "page": href
                        })

                except:
                    continue

        except Exception as e:

            print(f"Bing Error: {e}")

    return results

# def scan_bing(domain):

#     results = []

#     found_emails = set()

#     queries = [
#         f'"@{domain}"',
#         f'site:{domain} "@{domain}"',
#         f'site:{domain} email',
#         f'site:{domain} contact',
#         f'site:{domain} faculty',
#         f'site:{domain} staff'
#     ]

#     for query in queries:

#         for first in range(1, 30, 10):

#             url = (
#                 "https://www.bing.com/search?"
#                 f"q={query}&first={first}"
#             )

#             try:

#                 response = requests.get(
#                     url,
#                     headers=HEADERS,
#                     timeout=10
#                 )

#                 if response.status_code != 200:
#                     continue

#                 soup = BeautifulSoup(
#                     response.text,
#                     "html.parser"
#                 )

#                 text = soup.get_text(" ", strip=True)

#                 emails = extract_emails(text, domain)

#                 for email in emails:

#                     if email in found_emails:
#                         continue

#                     found_emails.add(email)

#                     results.append({
#                         "type": "email",
#                         "email": email,
#                         "username": email.split("@")[0],
#                         "domain": domain,
#                         "source": "Bing"
#                     })

#             except Exception as e:

#                 print(f"Bing Error: {e}")

#     return results