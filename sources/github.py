# sources/github.py

import requests
import re
import base64

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Optional GitHub token
GITHUB_TOKEN = "abc123.." #paste your github token here. 

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"


def scan_github(domain):

    results = []

    found = set()

    queries = [
        f'"@{domain}"',
        f'{domain}',
        f'"{domain}" password',
        f'"{domain}" mail'
    ]

    for query in queries:

        url = (
            "https://api.github.com/search/code"
            f"?q={query}&per_page=20"
        )

        try:

            r = requests.get(
                url,
                headers=HEADERS,
                timeout=15
            )

            if r.status_code != 200:
                continue

            data = r.json()

            items = data.get("items", [])

            for item in items:

                api_url = item.get("url")

                if not api_url:
                    continue

                file_response = requests.get(
                    api_url,
                    headers=HEADERS,
                    timeout=15
                )

                if file_response.status_code != 200:
                    continue

                file_data = file_response.json()

                content = file_data.get("content", "")

                if not content:
                    continue

                try:
                    decoded = base64.b64decode(
                        content
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )
                except:
                    continue

                emails = set(
                    re.findall(
                        rf"[a-zA-Z0-9_.+-]+@{re.escape(domain)}",
                        decoded
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
                        "source": "GitHub",
                        "repo": item.get("repository", {}).get("full_name"),
                        "file": item.get("path")
                    })

        except Exception as e:

            print("GitHub Error:", e)

    return results