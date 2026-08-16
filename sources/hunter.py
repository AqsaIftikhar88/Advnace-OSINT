# sources/hunter.py

import requests

API_KEY = "abc123.."  #paste your api key here....


def scan_hunter(domain):
    results = []

    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={API_KEY}"

    try:
        r = requests.get(url)
        data = r.json()

        for item in data["data"]["emails"]:
            email = item["value"]

            results.append({
                "email": email,
                "username": email.split("@")[0],
                "source": "Hunter"
            })

    except:
        pass

    return results