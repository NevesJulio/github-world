"""Coordena coleta, interpretação, layout e renderização."""
import argparse
import base64
import json
from pathlib import Path
import sys
import requests
from github_activity import GitHubClient, USERNAME
from repo_profile import profile_repository
from layout import build_layout
from renderer import save_world

BASE_DIR = Path(__file__).resolve().parent


def local_repository(root):
    excluded = {'.git', '.venv', 'venv', '__pycache__', 'node_modules', '.pytest_cache', '.agents', '.codex', '.aws'}
    tree = []
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if path.is_file() and not (set(relative.parts) & excluded):
            tree.append({'path': relative.as_posix(), 'type': 'blob'})
    icon_path = root / f'{root.name}.png'
    icon_base64 = base64.b64encode(icon_path.read_bytes()).decode() if icon_path.is_file() else None
    return {'name': root.name, 'icon_base64': icon_base64, 'main_language': 'Python', 'languages': {'Python': 1}, 'tree': tree, 'recent_commits': None, 'topics': []}


def main():
    parser = argparse.ArgumentParser(description='Gera ilhas a partir de árvores reais de repositórios.')
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--offline', action='store_true', help='Usa a árvore local; atividade e linguagens não são consultadas.')
    source.add_argument('--data', type=Path, help='Lê snapshot JSON (lista de repositórios).')
    parser.add_argument('--username', default=USERNAME)
    parser.add_argument(
        '--limit',
        type=int,
        default=1,
        help='Quantidade de repositórios no mapa (padrão: 1; máximo: 3).',
    )
    parser.add_argument('--output-dir', type=Path, default=BASE_DIR)
    parser.add_argument('--save-data', type=Path, help='Salva dados coletados para repetir a geração offline.')
    args = parser.parse_args()
    if not 1 <= args.limit <= 3:
        parser.error('--limit deve estar entre 1 e 3')
    if args.offline:
        data = [local_repository(BASE_DIR)]
    elif args.data:
        data = json.loads(args.data.read_text())[:args.limit]
    else:
        try:
            data = GitHubClient().collect(args.username,args.limit)
        except requests.RequestException as exc:
            print(f'Falha ao consultar GitHub: {exc}. Use --offline ou --data SNAPSHOT.json.', file=sys.stderr)
            return 1
    if not data:
        print('Nenhum repositório encontrado.',file=sys.stderr)
        return 1
    if args.save_data:
        args.save_data.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    for repo in data:
        for warning in repo.get('warnings',[]):
            print(f"Aviso [{repo['name']}]: {warning}",file=sys.stderr)
    profiles = [profile_repository(repo) for repo in data]
    islands,dimensions = build_layout(profiles)
    save_world(islands,dimensions,args.output_dir)
    for profile,island in zip(profiles,islands):
        print(f'{profile.name}: {profile.files} arquivos, {len(island.districts)} construções' + (' (dados incompletos)' if profile.incomplete else ''))
    print(f'map.png e world.gif gerados em {args.output_dir.resolve()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
