def analyze_data(all_data):

    emails = {}
    usernames = set()

    for item in all_data:

        # SUPPORT MULTIPLE KEYS
        email = (
            item.get("email")
            or item.get("value")
            or item.get("mail")
        )

        if not email:
            continue

        username = (
            item.get("username")
            or email.split("@")[0]
        )

        source = item.get(
            "source",
            "Unknown"
        )

        usernames.add(username)

        if email not in emails:

            emails[email] = {
                "email": email,
                "username": username,
                "sources": [source]
            }

        else:

            if source not in emails[email]["sources"]:

                emails[email]["sources"].append(source)

    return {

        "total_emails": len(emails),

        "total_usernames": len(usernames),

        "emails": list(emails.values()),

        "usernames": list(usernames)
    }