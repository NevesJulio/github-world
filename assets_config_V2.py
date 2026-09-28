from PIL import Image
from tiles import Tile, AssetManager


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
    "assets/Ilhas.png"
).convert("RGBA")

mapa = Image.open(
    "assets/mapa.png"
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