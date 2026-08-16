# sources/crtsh.py

import requests
import re
import json
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


def scan_crtsh(domain):

    results = []

    found = set()

    session = create_session()

    url = (
        f"https://crt.sh/?q=%25.{domain}&output=json"
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

            try:

                data = json.loads(
                    response.text.replace("\n", "")
                )

            except:
                return results

        # LIMIT HUGE DATASETS
        data = data[:500]

        for item in data:

            value = item.get(
                "name_value",
                ""
            )

            emails = re.findall(
                rf"[a-zA-Z0-9._%+-]+@{re.escape(domain)}",
                value,
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

                    "source": "crt.sh"
                })

    except requests.exceptions.Timeout:

        print("crt.sh Timeout")

    except Exception as e:

        print(f"crt.sh Error: {e}")

    return results