import requests
from collections import defaultdict

USERNAME = "NevesJulio"


def get_activity():

    url = f"https://api.github.com/users/{USERNAME}/repos"

    response = requests.get(
        url,
        params={
            "per_page": 100,
            "sort": "updated"
        }
    )

    response.raise_for_status()

    repos = response.json()

    languages = defaultdict(int)

    for repo in repos:

        # Ignora forks
        if repo["fork"]:
            continue

        language = repo["language"]

        if language:
            languages[language] += 1

    total = sum(languages.values())

    if total == 0:
        return {
            "destination": "Python",
            "languages": {}
        }

    percentages = {
        language: count / total
        for language, count in languages.items()
    }

    destination = max(
        percentages,
        key=percentages.get
    )

    return {
        "destination": destination,
        "languages": percentages
    }


if __name__ == "__main__":
    print(get_activity())