import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scan_commoncrawl(domain):

    results = []

    found = set()

    url = (
        "https://index.commoncrawl.org/"
        "CC-MAIN-2024-10-index"
        f"?url=*.{domain}/*&output=json"
    )

    try:

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        if r.status_code != 200:
            return results

        lines = r.text.splitlines()

        for line in lines[:50]:

            try:

                data = eval(line)

                page_url = data.get("url")

                if not page_url:
                    continue

                page = requests.get(
                    page_url,
                    headers=HEADERS,
                    timeout=10
                )

                text = page.text

                emails = set(
                    re.findall(
                        rf"[a-zA-Z0-9_.+-]+@{re.escape(domain)}",
                        text
                    )
                )

                for email in emails:

                    if email in found:
                        continue

                    found.add(email)

                    results.append({
                        "type": "email",
                        "email": email,
                        "username": email.split("@")[0],
                        "source": "CommonCrawl",
                        "url": page_url
                    })

            except:
                continue

    except Exception as e:

        print("CommonCrawl Error:", e)

    return results