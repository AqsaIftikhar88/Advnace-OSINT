# sources/wayback.py

import requests
import re

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def create_session():

    session = requests.Session()

    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )

    adapter = HTTPAdapter(
        max_retries=retries
    )

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def scan_wayback(domain):

    results = []

    found = set()

    session = create_session()

    url = (
        "https://web.archive.org/cdx/search/cdx?"
        f"url=*.{domain}/*"
        "&output=json"
        "&fl=timestamp,original"
        "&filter=statuscode:200"
        "&collapse=urlkey"
        "&limit=5"
    )

    try:

        response = session.get(
            url,
            headers=HEADERS,
            timeout=(10, 30)
        )

        if response.status_code != 200:
            return results

        try:

            data = response.json()

        except:
            return results

        for row in data[1:]:

            try:

                timestamp = row[0]
                original = row[1]

                archived_url = (
                    f"https://web.archive.org/web/"
                    f"{timestamp}/{original}"
                )

                page = session.get(
                    archived_url,
                    headers=HEADERS,
                    timeout=(5, 15)
                )

                text = page.text

                emails = re.findall(
                    rf"[a-zA-Z0-9._%+-]+@{re.escape(domain)}",
                    text,
                    re.IGNORECASE
                )

                for email in emails:

                    email = email.lower().strip()

                    if email in found:
                        continue

                    found.add(email)

                    results.append({

                        "email": email,

                        "username": email.split("@")[0],

                        "source": "Wayback"
                    })

            except:
                continue

    except requests.exceptions.Timeout:

        print("Wayback Timeout")

    except Exception as e:

        print(f"Wayback Error: {e}")

    return results
