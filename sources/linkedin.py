import requests
import re
from bs4 import BeautifulSoup


def generate_usernames(name):

    usernames = set()

    parts = name.lower().split()

    if len(parts) >= 2:

        first = parts[0]
        last = parts[-1]

        usernames.add(f"{first}.{last}")
        usernames.add(f"{first}{last}")
        usernames.add(f"{first}_{last}")
        usernames.add(f"{first[0]}{last}")
        usernames.add(f"{first}{last[0]}")
        usernames.add(f"{last}.{first}")

    elif len(parts) == 1:

        usernames.add(parts[0])

    return list(usernames)


def scan_linkedin(domain):

    results = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    query = (
        f'site:linkedin.com/in "{domain}"'
    )

    url = (
        "https://www.bing.com/search?q="
        + query
    )

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text(" ")

        # Extract LinkedIn names

        matches = re.findall(
            r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\s-\sLinkedIn',
            text
        )

        found = set()

        for name in matches:

            if name in found:
                continue

            found.add(name)

            usernames = generate_usernames(name)

            for username in usernames:

                results.append({
                    "name": name,
                    "username": username,
                    "source": "LinkedIn"
                })

    except Exception as e:

        print(f"LinkedIn Error: {e}")

    return results
