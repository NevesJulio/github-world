from pathlib import Path
from PIL import Image
from tiles import Tile, AssetManager


BASE_DIR = Path(__file__).resolve().parent
assets = AssetManager()


# =========================
# ASSET GLOSSARY
# =========================

ASSET_GLOSSARY = {
    "g": "Grass / tiles que formam as ilhas",
    "e": "Earth / terra",
    "r": "Rocks / pedras",
    "c": "Fences / cercas",
    "f": "Foliage / folhas e vegetação",

    "co": "Orange houses / casas laranja",
    "cc": "Gray houses / casas cinza",
    "cv": "Green houses / casas verdes",

    "p": "Bridges / pontes",
    "x": "Special tiles / entradas e outros elementos especiais",

    "m": "Map / elementos do mapa ou minimapa",
}



Ilhas = Image.open(
    BASE_DIR / "assets/Ilhas.png"
).convert("RGBA")

mapa = Image.open(
    BASE_DIR / "assets/mapa.png"
).convert("RGBA")



# =========================
# GRASS / ISLAND
# =========================

# canto superior esquerdo
assets.add(Tile(
    "g1",
    Ilhas,
    col=0,
    row=1
))

# borda superior
assets.add(Tile(
    "g2",
    Ilhas,
    col=1,   # ajustar
    row=1
))

# canto superior direito
assets.add(Tile(
    "g3",
    Ilhas,
    col=2,   # ajustar
    row=1
))

# borda esquerda
assets.add(Tile(
    "g4",
    Ilhas,
    col=0,   # ajustar
    row=2
))

# centro
assets.add(Tile(
    "g5",
    Ilhas,
    col=1,
    row=2
))

# borda direita
assets.add(Tile(
    "g6",
    Ilhas,
    col=2,   # ajustar
    row=2
))

# canto inferior esquerdo
assets.add(Tile(
    "g7",
    Ilhas,
    col=0,   # ajustar
    row=3
))

# borda inferior
assets.add(Tile(
    "g8",
    Ilhas,
    col=1,   # ajustar
    row=3
))

# canto inferior direito
assets.add(Tile(
    "g9",
    Ilhas,
    col=2,   # ajustar
    row=3
))


# =========================
# terra
# =========================

n = 1

for row in range(0, 9):
    for col in range(2, 11):
        assets.add(Tile(
            f"e{n}",
            Ilhas,
            col=col,
            row=row
        ))
        n += 1


# =========================
# pedras
# =========================

n = 1

for row in range(0, 2):
    for col in range(10, 16):
        assets.add(Tile(
            f"r{n}",
            Ilhas,
            col=col,
            row=row
        ))
        n += 1

# =========================
# cercas
# =========================

n = 1

for row in range(5, 13):
    for col in range(7, 15):
        assets.add(Tile(
            f"c{n}",
            Ilhas,
            col=col,
            row=row
        ))
        n += 1


# =========================
# folhas
# =========================

n = 1

for row in range(0, 2):
    for col in range(5, 10):
        assets.add(Tile(
            f"f{n}",
            Ilhas,
            col=col,
            row=row
        ))
        n += 1


# =========================
# casas laranja
# =========================


assets.add(Tile(
    "co1",
    Ilhas,
    col=16,
    row=9,
    width=8,
    height=7
))


assets.add(Tile(
    "co2",
    Ilhas,
    col=24,
    row=9,
    width=8,
    height=7
))

assets.add(Tile(
    "co3",
    Ilhas,
    col=16,
    row=0,
    width=12,
    height=9
))



# =========================
# casas cinza
# =========================

assets.add(Tile(
    "cc1",
    Ilhas,
    col=16,
    row=25,
    width=8,
    height=7
))

assets.add(Tile(
    "cc2",
    Ilhas,
    col=24,
    row=25,
    width=8,
    height=7
))

assets.add(Tile(
    "cc3",
    Ilhas,
    col=16,
    row=16,
    width=12,
    height=9
))


# =========================
# casas cinza
# =========================


assets.add(Tile(
    "cv1",
    Ilhas,
    col=0,
    row=25,
    width=8,
    height=7
))


assets.add(Tile(
    "cv2",
    Ilhas,
    col=8,
    row=25,
    width=8,
    height=7
))

assets.add(Tile(
    "cv3",
    Ilhas,
    col=0,
    row=16,
    width=12,
    height=9
))


# =========================
# pontes
# =========================

assets.add(Tile(
    "p1",
    Ilhas,
    col=12,
    row=12,
    width=1,
    height=3
))


assets.add(Tile(
    "p2",
    Ilhas,
    col=13,
    row=12,
    width=1,
    height=3
))

assets.add(Tile(
    "p3",
    Ilhas,
    col=15,
    row=12,
    width=1,
    height=3
))

assets.add(Tile(
    "p4",
    Ilhas,
    col=10,
    row=13,
    width=2,
    height=1
))

assets.add(Tile(
    "p5",
    Ilhas,
    col=10,
    row=14,
    width=2,
    height=1
))

assets.add(Tile(
    "p6",
    Ilhas,
    col=10,
    row=15,
    width=2,
    height=1
))




# =========================
# entrada
# =========================

assets.add(Tile(
    "x3",
    Ilhas,
    col=5,
    row=2,
    width=3,
    height=2
))


# =========================
# mapa
# =========================

assets.add(Tile(
    "y1",
    mapa,
    col=50,
    row=3,
    width = 9,
    height=16
))


# =========================
# barris
# =========================

#caixa1
assets.add(Tile(
    "m1",
    Ilhas,
    col=5,
    row=8,
    width = 1,
    height=1
))

#caixa2
assets.add(Tile(
    "m2",
    Ilhas,
    col=5,
    row=9,
    width = 1,
    height=1
))

#caixa3
assets.add(Tile(
    "m3",
    Ilhas,
    col=5,
    row=10,
    width = 1,
    height=1
))

#caixa4
assets.add(Tile(
    "m4",
    Ilhas,
    col=5,
    row=11,
    width = 1,
    height=1
))

#caixa grande
assets.add(Tile(
    "m5",
    Ilhas,
    col=6,
    row=8,
    width = 2,
    height=2
))

#barril grande
assets.add(Tile(
    "m6",
    Ilhas,
    col=8,
    row=8,
    width = 2,
    height=2
))

#caixa pequena
assets.add(Tile(
    "m7",
    Ilhas,
    col=10,
    row=8,
    width = 1,
    height=2
))

#caixa media
assets.add(Tile(
    "m8",
    Ilhas,
    col=11,
    row=8,
    width = 1,
    height=2
))

#barril media
assets.add(Tile(
    "m9",
    Ilhas,
    col=11,
    row=10,
    width = 1,
    height=2
))

 
#fonte cheia 1
assets.add(Tile(
    "m11",
    Ilhas,
    col=14,
    row=7,
    width = 1,
    height=2
))

#fonte cheia 2
assets.add(Tile(
    "m12",
    Ilhas,
    col=15,
    row=7,
    width = 1,
    height=2
))


#fonte vazia 1
assets.add(Tile(
    "m13",
    Ilhas,
    col=14,
    row=8,
    width = 1,
    height=2
))

#fonte vazia 2
assets.add(Tile(
    "m14",
    Ilhas,
    col=15,
    row=8,
    width = 1,
    height=2
))

#banco pequeno
assets.add(Tile(
    "m15",
    Ilhas,
    col=13,
    row=6,
    width = 1,
    height=1
))

#banco grande
assets.add(Tile(
    "m16",
    Ilhas,
    col=13,
    row=7,
    width = 1,
    height=1
))

#varal
assets.add(Tile(
    "m17",
    Ilhas,
    col=12,
    row=8,
    width = 2,
    height=1
))

#fonte grande
assets.add(Tile(
    "m18",
    Ilhas,
    col=14,
    row=2,
    width = 2,
    height=3
))

#fonte média
assets.add(Tile(
    "m19",
    Ilhas,
    col=14,
    row=5,
    width = 2,
    height=2
))

#banco vertical
assets.add(Tile(
    "m20",
    Ilhas,
    col=10,
    row=6,
    width = 1,
    height=2
))

#banco horizontal
assets.add(Tile(
    "m21",
    Ilhas,
    col=11,
    row=6,
    width = 2,
    height=1
))


n = 22

# placas
for row in range(4, 6):
    for col in range(10, 13):
        assets.add(Tile(
            f"m{n}",
            Ilhas,
            col=col,
            row=row
        ))
        n += 1



DECORATION_GROUPS = {
    # Trabalho / atividade recente
    "activity": [
        "m1", "m2", "m3", "m4",
        "m5", "m6", "m7", "m8", "m9"
    ],

    # Saúde / manutenção do projeto
    "health_full": [
        "m11", "m12", "m18", "m19"
    ],

    "health_empty": [
        "m13", "m14"
    ],

    # Elementos ambientais
    "ambient": [
        "m15", "m16", "m17",
        "m20", "m21"
    ],

    # Informações / marcos
    "signs": [
        "m22", "m23", "m24",
        "m25", "m26", "m27"
    ]
}

# Assets exclusivos do catálogo antigo; IDs da V2 têm prioridade.
arvores = Image.open(BASE_DIR / "assets/arvores.png").convert("RGBA")
# TREES
# =========================

assets.add(Tile(
    "t1",
    arvores,
    col=0,
    row=0,
    width=3,
    height=4
))

assets.add(Tile(
    "t2",
    arvores,
    col=3,
    row=0,
    width=3,
    height=4
))

assets.add(Tile(
    "t3",
    arvores,
    col=6,
    row=1,
    width=2,
    height=3
))

assets.add(Tile(
    "t4",
    arvores,
    col=8,
    row=1,
    width=2,
    height=3
))


assets.add(Tile(
    "t5",
    arvores,
    col=0,
    row=4,
    width=3,
    height=1
))

assets.add(Tile(
    "t6",
    arvores,
    col=3,
    row=4,
    width=3,
    height=1
))

assets.add(Tile(
    "t7",
    arvores,
    col=7,
    row=4,
    width=1,
    height=1
))

assets.add(Tile(
    "t8",
    arvores,
    col=8,
    row=4,
    width=1,
    height=1
))


madeira = Image.open(BASE_DIR / "assets/madeira.png").convert("RGBA")
assets.add(Tile("wood1", madeira, col=2, row=2, width=3, height=1))
assets.add(Tile("wood2", madeira, col=7, row=2, width=3, height=2))
assets.add(Tile("wood3", madeira, col=6, row=1, width=1, height=2))

# IDs próprios preservam a folhagem f1–f10 da V2.
grama = Image.open(BASE_DIR / "assets/grama.png").convert("RGBA")
assets.add(Tile("floor1", grama, col=4, row=6))
assets.add(Tile("floor2", grama, col=5, row=6))
assets.add(Tile("floor3", grama, col=6, row=6))
assets.add(Tile("floor4", grama, col=4, row=7))
assets.add(Tile("floor5", grama, col=5, row=7))
assets.add(Tile("floor6", grama, col=6, row=7))
assets.add(Tile("floor7", grama, col=1, row=6, width=3, height=4))
assets.add(Tile("floor8", grama, col=5, row=3, width=1, height=1))
assets.add(Tile("floor9", grama, col=3, row=3, width=1, height=1))
assets.add(Tile("floor10", grama, col=4, row=3, width=1, height=1))
# Flores da linha 3, colunas 3–5 do tileset de grama (índices zero-based).
# Mantemos os IDs floor8–floor10 por compatibilidade e oferecemos nomes claros
# para a composição controlada da floresta.
assets.add(Tile("flower1", grama, col=3, row=3))
assets.add(Tile("flower2", grama, col=4, row=3))
assets.add(Tile("flower3", grama, col=5, row=3))
assets.add(Tile("grass1", grama, col=10, row=1))
assets.add(Tile("grass2", grama, col=11, row=1))
assets.add(Tile("grass3", grama, col=12, row=1))
assets.add(Tile("grass4", grama, col=13, row=1))
assets.add(Tile("grass5", grama, col=10, row=2))
assets.add(Tile("grass6", grama, col=11, row=2))
assets.add(Tile("grass7", grama, col=12, row=2))
assets.add(Tile("grass8", grama, col=13, row=2))

DECORATION_GROUPS["flowers"] = ["flower1", "flower2", "flower3"]
ASSET_GLOSSARY.update({"t": "Árvores", "flower": "Flores", "wood": "Madeira antiga", "floor": "Pisos antigos", "grass": "Grama antiga", "y": "Mapa"})

# Centro do bloco de terra; e1 é decorativo no tileset consolidado.
assets.add(Tile('path1', Ilhas, col=1, row=6))
ASSET_GLOSSARY['path'] = 'Caminhos de terra'

# Variante compacta das casas maiores, preservando todos os recortes originais.
for color in ('co', 'cc', 'cv'):
    original = assets.get(f'{color}3')
    compact = Tile(f'{color}3_compact', Ilhas, original.col, original.row, width=10, height=7)
    compact.image = original.image.resize((160, 112), Image.Resampling.NEAREST)
    assets.add(compact)
