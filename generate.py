from PIL import Image
from pathlib import Path
import random
from assets_config import assets


BASE_DIR = Path(__file__).resolve().parent

TILE_SIZE = 16


# ============================================================
# MAPS
# ============================================================

# ============================================================
# MAP CONFIG
# ============================================================

MAP_COLS = 25
MAP_ROWS = 12


# ============================================================
# CREATE LAYERS
# ============================================================
GRASS_TILES = [
    "g1",
    "g2",
    "g3",
    "g4",
    "g5",
    "g6",
    "g7",
    "g8"
]

GRASS_WEIGHTS = [
    5,  # g1
    5,  # g2
    75,  # g3
    5,  # g4
    2,   # g5
    3,   # g6
    3,   # g7
    2    # g8
]

GROUND_MAP = [
    [
        random.choices(
            GRASS_TILES,
            weights=GRASS_WEIGHTS,
            k=1
        )[0]
        for _ in range(MAP_COLS)
    ]
    for _ in range(MAP_ROWS)
]

OBJECT_MAP = [
    [None for _ in range(MAP_COLS)]
    for _ in range(MAP_ROWS)
]

TOP_MAP = [
    [None for _ in range(MAP_COLS)]
    for _ in range(MAP_ROWS)
]


# ============================================================
# TERRAIN
# ============================================================

for col in range(MAP_COLS):
    GROUND_MAP[5][col] = "f2"
    GROUND_MAP[6][col] = "f5"


# ============================================================
# TREES
# ============================================================

OBJECT_MAP[2][2] = "t1"
OBJECT_MAP[2][7] = "t2"

OBJECT_MAP[8][19] = "t1"
OBJECT_MAP[7][23] = "t2"


# ============================================================
# BUILDINGS
# ============================================================

OBJECT_MAP[3][15] = "c1"


# ============================================================
# RENDER FUNCTION
# ============================================================

def render_layer(canvas, layer):

    for row, line in enumerate(layer):

        for col, asset_name in enumerate(line):

            if asset_name is None:
                continue

            asset = assets.get(asset_name)

            x = col * TILE_SIZE
            y = row * TILE_SIZE

            canvas.paste(
                asset.image,
                (x, y),
                asset.image
            )


# ============================================================
# MAP SIZE
# ============================================================

MAP_WIDTH = len(GROUND_MAP[0]) * TILE_SIZE
MAP_HEIGHT = len(GROUND_MAP) * TILE_SIZE


# ============================================================
# BACKGROUND
# ============================================================

background = Image.new(
    "RGBA",
    (MAP_WIDTH, MAP_HEIGHT),
    (0, 0, 0, 0)
)

render_layer(background, GROUND_MAP)
render_layer(background, OBJECT_MAP)

background.save("map.png")


# ============================================================
# PLAYER
# ============================================================

sprites = [
    Image.open(BASE_DIR / "assets/me/frame_01.png").convert("RGBA"),
    Image.open(BASE_DIR / "assets/me/frame_02.png").convert("RGBA"),
    Image.open(BASE_DIR / "assets/me/frame_03.png").convert("RGBA"),
]

SPRITE_SIZE = (32, 32)

sprites = [
    sprite.resize(
        SPRITE_SIZE,
        Image.Resampling.NEAREST
    )
    for sprite in sprites
]


# ============================================================
# PLAYER POSITION
# ============================================================

player_col = 2
player_row = 3

player_x = player_col * TILE_SIZE
player_y = player_row * TILE_SIZE


# ============================================================
# ANIMATION
# ============================================================

frames = []

for sprite in sprites:

    img = background.copy()

    position = (
        player_x - sprite.width // 2,
        player_y - sprite.height
    )

    # personagem
    img.paste(
        sprite,
        position,
        sprite
    )

    # coisas que precisam ficar na frente
    render_layer(img, TOP_MAP)

    frames.append(img)


# ============================================================
# SAVE GIF
# ============================================================

frames[0].save(
    "world.gif",
    save_all=True,
    append_images=frames[1:],
    duration=180,
    loop=0
)

print("map.png generated!")
print("world.gif generated!")