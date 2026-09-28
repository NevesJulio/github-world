from PIL import Image
from tiles import Tile, AssetManager


assets = AssetManager()


Ilhas = Image.open(
    "assets/Ilhas.png"
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

for row in range(0, 12):
    for col in range(4, 15):
        assets.add(Tile(
            f"p{n}",
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

for row in range(5, 0):
    for col in range(9, 1):
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