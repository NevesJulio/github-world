"""Coleta dados do GitHub sem executar requests durante imports."""
from datetime import datetime, timedelta, timezone
import os
from urllib.parse import quote
import requests

USERNAME = "NevesJulio"


class GitHubClient:
    def __init__(self, token=None):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/vnd.github+json"})
        token = token or os.getenv("GITHUB_TOKEN")
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get(self, path, **params):
        response = self.session.get(f"https://api.github.com{path}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def repositories(self, username, limit):
        repos = []
        page = 1
        while len(repos) < limit:
            batch = self.get(f"/users/{username}/repos", per_page=100, sort="updated", page=page)
            repos.extend(repo for repo in batch if not repo["fork"])
            if len(batch) < 100:
                break
            page += 1
        return repos[:limit]

    def collect(self, username=USERNAME, limit=1):
        now = datetime.now(timezone.utc)
        since = (now - timedelta(days=30)).isoformat()
        result = []
        for repo in self.repositories(username, limit):
            path = f"/repos/{repo['full_name']}"
            warnings = []
            def optional(suffix, default, **params):
                try:
                    return self.get(path + suffix, **params)
                except requests.RequestException as exc:
                    warnings.append(f"{suffix}: {exc}")
                    return default
            # A árvore recursiva pode ser truncada: o perfil registra essa limitação.
            tree = optional(f"/git/trees/{quote(repo['default_branch'], safe='')}", {"tree": [], "unavailable": True}, recursive=1)
            languages = optional("/languages", {})
            commits = optional("/commits", None, since=since, per_page=100)
            icon_name = f"{repo['name']}.png"
            icon_entry = next(
                (entry for entry in tree.get("tree", [])
                 if entry.get("type") == "blob" and entry.get("path") == icon_name),
                None,
            )
            icon_base64 = None
            if icon_entry:
                blob = optional(f"/git/blobs/{icon_entry['sha']}", {})
                if blob.get("encoding") == "base64":
                    icon_base64 = blob.get("content")
            result.append({
                "name": repo["name"], "main_language": repo.get("language"),
                "languages": languages, "topics": repo.get("topics", []),
                "pushed_at": repo.get("pushed_at"), "as_of": now.isoformat(),
                "tree": tree.get("tree", []), "tree_truncated": tree.get("truncated", False),
                "tree_unavailable": tree.get("unavailable", False),
                "recent_commits": len(commits) if commits is not None else None,
                "commits_capped": commits is not None and len(commits) == 100,
                "icon_base64": icon_base64,
                "warnings": warnings,
            })
        return result


def get_top_repositories(limit=1):
    """Compatibilidade para consumidores que precisam somente dos nomes."""
    return [repo["name"] for repo in GitHubClient().repositories(USERNAME, limit)]
