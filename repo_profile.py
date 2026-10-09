"""Interpreta árvores de arquivos, sem dependência da API ou do desenho."""
from dataclasses import dataclass
from datetime import datetime
from pathlib import PurePosixPath


@dataclass(frozen=True)
class DirectoryProfile:
    name: str
    files: int
    max_depth: int

    @property
    def size(self):
        return 3 if self.files >= 80 else 2 if self.files >= 20 else 1


@dataclass(frozen=True)
class RepoProfile:
    name: str
    icon_base64: str | None
    main_language: str
    languages: tuple
    files: int
    directories: int
    max_depth: int
    recent_commits: int | None
    days_inactive: int | None
    has_tests: bool
    has_docs: bool
    dependencies: int
    complexity_level: int
    theme: str
    districts: tuple
    incomplete: bool


def profile_repository(data):
    paths = sorted({entry['path'] for entry in data.get('tree', []) if entry.get('type') == 'blob'})
    directories = set()
    grouped = {}
    has_tests = has_docs = False
    dependencies = 0
    manifests = {'package.json', 'requirements.txt', 'pyproject.toml', 'cargo.toml', 'go.mod', 'pom.xml', 'gemfile'}
    for path in paths:
        parts = PurePosixPath(path).parts
        lower = tuple(part.lower() for part in parts)
        for depth in range(1, len(parts)):
            directories.add('/'.join(parts[:depth]))
        district = parts[0] if len(parts) > 1 else '(raiz)'
        grouped.setdefault(district, []).append(len(parts) - 1)
        has_tests |= any(p in {'test', 'tests', '__tests__', 'spec', 'specs'} for p in lower[:-1]) or lower[-1].startswith('test_') or '.test.' in lower[-1] or '.spec.' in lower[-1]
        has_docs |= any(p in {'doc', 'docs', 'documentation'} for p in lower[:-1]) or lower[-1].startswith('readme')
        dependencies += lower[-1] in manifests
    districts = [DirectoryProfile(name, len(depths), max(depths)) for name, depths in grouped.items()]
    districts.sort(key=lambda item: (-item.files, item.name))
    # Todos os arquivos continuam representados; excedentes viram um bairro agregado.
    if len(districts) > 6:
        rest = districts[5:]
        districts = districts[:5] + [DirectoryProfile('(outros)', sum(d.files for d in rest), max(d.max_depth for d in rest))]
    if not districts:
        districts = [DirectoryProfile('(sem arquivos)', 0, 0)]
    language = data.get('main_language') or 'Unknown'
    languages = tuple(sorted(data.get('languages', {}), key=lambda key: (-data['languages'][key], key)))
    topics = set(data.get('topics', []))
    theme = 'research' if topics & {'machine-learning', 'research', 'data-science', 'ai'} else 'hardware' if topics & {'arduino', 'embedded', 'iot'} else 'web' if topics & {'web', 'frontend', 'website'} else 'forest'
    inactive = None
    if data.get('pushed_at') and data.get('as_of'):
        inactive = max(0, (datetime.fromisoformat(data['as_of'].replace('Z', '+00:00')) - datetime.fromisoformat(data['pushed_at'].replace('Z', '+00:00'))).days)
    count = len(paths)
    return RepoProfile(data['name'], data.get('icon_base64'), language, languages, count, len(directories), max((len(PurePosixPath(p).parts)-1 for p in paths), default=0), data.get('recent_commits'), inactive, has_tests, has_docs, dependencies, 3 if count >= 200 else 2 if count >= 40 else 1, theme, tuple(districts), bool(data.get('tree_truncated') or data.get('tree_unavailable')))
