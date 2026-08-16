import requests
import re
import time

API_KEY = "e936759e-20e2-48fc-a14b-261a7df09df3"


def scan_intelx(domain):

    results = []

    headers = {
        "x-key": API_KEY,
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    payload = {
        "term": f"@{domain}",
        "maxresults": 10
    }

    try:

        r = requests.post(
            "https://free.intelx.io/intelligent/search",
            json=payload,
            headers=headers,
            timeout=20
        )

        print("SEARCH STATUS:", r.status_code)

        if r.status_code != 200:
            print(r.text)
            return results

        try:
            data = r.json()
        except:
            print("Invalid JSON from IntelX")
            print(r.text)
            return results

        search_id = data.get("id")

        if not search_id:
            print("No search ID returned")
            return results

        time.sleep(3)

        rr = requests.get(
            f"https://free.intelx.io/intelligent/search/result?id={search_id}",
            headers=headers,
            timeout=20
        )

        print("RESULT STATUS:", rr.status_code)

        if rr.status_code != 200:
            print(rr.text)
            return results

        try:
            result_data = rr.json()
        except:
            print("Invalid result JSON")
            print(rr.text)
            return results

        for record in result_data.get("records", []):

            text = str(record)

            emails = set(
                re.findall(
                    rf"[a-zA-Z0-9_.+-]+@{re.escape(domain)}",
                    text,
                    re.IGNORECASE
                )
            )

            for email in emails:

                results.append({

                    "type": "email",

                    "email": email,

                    "username": email.split("@")[0],

                    "domain": domain,

                    "source": "IntelX",

                    "page": record.get("name", "Unknown")
                })

    except Exception as e:

        print(f"IntelX Error: {e}")

    return results