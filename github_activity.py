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

    # API indisponível / rate limit
    if response.status_code != 200:

        print(
            f"GitHub API error: "
            f"{response.status_code}"
        )

        return [
            "github-world",
            "Carcinoma_Segmentation",
            "Repository"
        ][:limit]

    repos = response.json()

    repos = [
        repo
        for repo in repos
        if not repo["fork"]
    ]

    repos.sort(
        key=lambda repo: repo["updated_at"],
        reverse=True
    )

    return [
        repo["name"]
        for repo in repos[:limit]
    ]