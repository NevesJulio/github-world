from PIL import Image
from tiles import Tile, AssetManager

assets = AssetManager()

# =========================
# TILESETS
# =========================

arvores = Image.open(
    "assets/arvores.png"
).convert("RGBA")

chao = Image.open(
    "assets/arvores.png"
).convert("RGBA")

grama = Image.open(
    "assets/arvores.png"
).convert("RGBA")

madeira = Image.open(
    "assets/arvores.png"
).convert("RGBA")

taiga = Image.open(
    "assets/arvores.png"
).convert("RGBA")

variados = Image.open(
    "assets/arvores.png"
).convert("RGBA")



# =========================
# GRASS
# =========================

n = 1

for row in range(1, 3):
    for col in range(8, 12):
        assets.add(Tile(
            f"g{n}",
            taiga,
            col=col,
            row=row
        ))
        n += 1


# =========================
# FLOORS
# =========================

n = 1

for row in range(6, 8):
    for col in range(4, 7):
        assets.add(Tile(
            f"f{n}",
            grama,
            col=col,
            row=row
        ))
        n += 1


# =========================
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

# =========================
# CONSTRUCTIONS
# =========================

assets.add(Tile(
    "c1",
    madeira,
    col=2,
    row=2,
    width=3,
    height=1
))

assets.add(Tile(
    "c2",
    madeira,
    col=7,
    row=2,
    width=3,
    height=2
))


assets.add(Tile(
    "c3",
    madeira,
    col=6,
    row=1,
    width=1,
    height=2
))