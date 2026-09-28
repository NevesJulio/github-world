import requests

USERNAME = "NevesJulio"


def get_top_repositories(limit=3):

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

    # remove forks
    repos = [
        repo
        for repo in repos
        if not repo["fork"]
    ]

    # ordena pelos atualizados mais recentemente
    repos.sort(
        key=lambda repo: repo["updated_at"],
        reverse=True
    )

    # pega apenas os nomes
    top_repos = [
        repo["name"]
        for repo in repos[:limit]
    ]

    return top_repos