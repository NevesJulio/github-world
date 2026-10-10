"""Carrega regras visuais editáveis sem misturá-las à lógica do layout."""
from pathlib import Path
import random

import yaml


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / 'world.yaml'
TREE_ORDER = ('large', 'small', 'large_stump', 'small_stump')


def load_visual_config(path=CONFIG_PATH):
    with Path(path).open(encoding='utf-8') as stream:
        config = yaml.safe_load(stream) or {}
    if not isinstance(config, dict):
        raise ValueError('world.yaml deve conter um objeto YAML.')
    return config


def rule_matches(profile, conditions):
    comparisons = {
        'min_files': profile.files,
        'min_directories': profile.directories,
        'min_depth': profile.max_depth,
        'min_dependencies': profile.dependencies,
        'min_recent_commits': profile.recent_commits,
        'min_days_inactive': profile.days_inactive,
    }
    allowed = set(comparisons) | {'has_tests', 'has_docs'}
    unknown = set(conditions) - allowed
    if unknown:
        raise ValueError(f'Condições desconhecidas em world.yaml: {", ".join(sorted(unknown))}')
    for key, actual in comparisons.items():
        if key in conditions and (actual is None or actual < conditions[key]):
            return False
    for key, actual in {'has_tests': profile.has_tests, 'has_docs': profile.has_docs}.items():
        if key in conditions and actual != bool(conditions[key]):
            return False
    return True


def tree_counts(profile, config=None):
    vegetation = (config or load_visual_config()).get('vegetation', {})
    counts = dict(vegetation.get('defaults', {}))
    for rule in vegetation.get('rules', []):
        if rule_matches(profile, rule.get('when', {})):
            counts.update(rule.get('trees', {}))
    override = vegetation.get('repositories', {}).get(profile.name, {})
    counts.update(override.get('trees', {}))
    return {name: max(0, min(12, int(counts.get(name, 0)))) for name in TREE_ORDER}


def tree_assets_for(profile, config=None):
    config = config or load_visual_config()
    vegetation = config.get('vegetation', {})
    groups = vegetation.get('assets', {})
    counts = tree_counts(profile, config)
    rng = random.Random(f'{profile.name}/tree-variants')
    selected = []
    for category in TREE_ORDER:
        variants = groups.get(category, [])
        if counts[category] and not variants:
            raise ValueError(f'Nenhum asset configurado para vegetation.assets.{category}')
        selected.extend(rng.choice(variants) for _ in range(counts[category]))
    return selected
