"""Carrega o catálogo declarativo de sprites definido em assets.yaml."""
from pathlib import Path

from PIL import Image
import yaml

from tiles import AssetManager, Tile


BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "assets.yaml"


def _mapping(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} deve ser um objeto YAML.")
    return value


def _positive_int(value, label, default=1):
    value = default if value is None else value
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{label} deve ser um inteiro positivo.")
    return value


def _coordinate(value, label):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} deve ser um inteiro maior ou igual a zero.")
    return value


def load_asset_catalog(path=CATALOG_PATH):
    """Cria o AssetManager e os grupos a partir de um catálogo YAML validado."""
    path = Path(path)
    with path.open(encoding="utf-8") as stream:
        config = yaml.safe_load(stream) or {}
    config = _mapping(config, str(path))

    source_paths = _mapping(config.get("sources", {}), "sources")
    sources = {}
    for name, relative_path in source_paths.items():
        if not isinstance(name, str) or not isinstance(relative_path, str):
            raise ValueError("Cada source deve associar um nome a um caminho.")
        image_path = path.parent / relative_path
        if not image_path.is_file():
            raise ValueError(f"Spritesheet inexistente para sources.{name}: {image_path}")
        sources[name] = Image.open(image_path).convert("RGBA")

    manager = AssetManager()

    def add(name, definition):
        if not isinstance(name, str) or not name:
            raise ValueError("Todo asset precisa ter um nome não vazio.")
        if name in manager.assets:
            raise ValueError(f"Asset duplicado em {path.name}: {name}")
        definition = _mapping(definition, f"assets.{name}")
        unknown = set(definition) - {"source", "col", "row", "width", "height", "tile_size"}
        if unknown:
            raise ValueError(f"Campos desconhecidos em {name}: {', '.join(sorted(unknown))}")
        source_name = definition.get("source")
        if source_name not in sources:
            raise ValueError(f"Source desconhecido em {name}: {source_name}")
        col = _coordinate(definition.get("col"), f"{name}.col")
        row = _coordinate(definition.get("row"), f"{name}.row")
        width = _positive_int(definition.get("width"), f"{name}.width")
        height = _positive_int(definition.get("height"), f"{name}.height")
        tile_size = _positive_int(definition.get("tile_size"), f"{name}.tile_size", 16)
        source = sources[source_name]
        if (col + width) * tile_size > source.width or (row + height) * tile_size > source.height:
            raise ValueError(f"Recorte de {name} ultrapassa o spritesheet {source_name}.")
        manager.add(Tile(name, source, col, row, width, height, tile_size))

    sequences = config.get("sequences", [])
    if not isinstance(sequences, list):
        raise ValueError("sequences deve ser uma lista.")
    for index, sequence in enumerate(sequences):
        sequence = _mapping(sequence, f"sequences[{index}]")
        unknown = set(sequence) - {"prefix", "start", "source", "rows", "columns", "width", "height", "tile_size"}
        if unknown:
            raise ValueError(f"Campos desconhecidos em sequences[{index}]: {', '.join(sorted(unknown))}")
        prefix = sequence.get("prefix")
        start = _positive_int(sequence.get("start"), f"sequences[{index}].start")
        rows = sequence.get("rows")
        columns = sequence.get("columns")
        if not isinstance(prefix, str) or not prefix:
            raise ValueError(f"sequences[{index}].prefix deve ser texto não vazio.")
        if not isinstance(rows, list) or len(rows) != 2 or not isinstance(columns, list) or len(columns) != 2:
            raise ValueError(f"sequences[{index}] precisa de rows e columns no formato [início, fim].")
        first_row, last_row = (_coordinate(value, f"sequences[{index}].rows") for value in rows)
        first_col, last_col = (_coordinate(value, f"sequences[{index}].columns") for value in columns)
        if last_row < first_row or last_col < first_col:
            raise ValueError(f"Intervalo invertido em sequences[{index}].")
        number = start
        base = {key: value for key, value in sequence.items() if key not in {"prefix", "start", "rows", "columns"}}
        for row in range(first_row, last_row + 1):
            for col in range(first_col, last_col + 1):
                add(f"{prefix}{number}", {**base, "col": col, "row": row})
                number += 1

    for name, definition in _mapping(config.get("tiles", {}), "tiles").items():
        add(name, definition)

    for name, definition in _mapping(config.get("derived", {}), "derived").items():
        definition = _mapping(definition, f"derived.{name}")
        unknown = set(definition) - {"from", "width", "height"}
        if unknown:
            raise ValueError(f"Campos desconhecidos em derived.{name}: {', '.join(sorted(unknown))}")
        parent_name = definition.get("from")
        if parent_name not in manager.assets:
            raise ValueError(f"Asset-base desconhecido em derived.{name}: {parent_name}")
        if name in manager.assets:
            raise ValueError(f"Asset duplicado em {path.name}: {name}")
        parent = manager.get(parent_name)
        width = _positive_int(definition.get("width"), f"derived.{name}.width")
        height = _positive_int(definition.get("height"), f"derived.{name}.height")
        derived = Tile(name, parent.tileset, parent.col, parent.row, width, height, parent.tile_size)
        derived.image = parent.image.resize(
            (width * parent.tile_size, height * parent.tile_size), Image.Resampling.NEAREST
        )
        manager.add(derived)

    groups = _mapping(config.get("groups", {}), "groups")
    for group_name, names in groups.items():
        if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
            raise ValueError(f"groups.{group_name} deve ser uma lista de nomes.")
        missing = [name for name in names if name not in manager.assets]
        if missing:
            raise ValueError(f"Assets inexistentes em groups.{group_name}: {', '.join(missing)}")

    glossary = _mapping(config.get("glossary", {}), "glossary")
    return manager, groups, glossary, sources


assets, DECORATION_GROUPS, ASSET_GLOSSARY, SOURCES = load_asset_catalog()

# Compatibilidade temporária com código externo que importava os spritesheets.
Ilhas = SOURCES["ilhas"]
mapa = SOURCES["mapa"]
arvores = SOURCES["arvores"]
madeira = SOURCES["madeira"]
grama = SOURCES["grama"]
