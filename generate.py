from PIL import Image
from pathlib import Path
import random
from assets_config import assets


BASE_DIR = Path(__file__).resolve().parent

TILE_SIZE = 16


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
    2,   # g1
    2,   # g2
    2,  # g3
    80,   # g4
    4,   # g5
    4,   # g6
    4,   # g7
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
# PATH SYSTEM
# ============================================================

# f1 ╭
# f2 ─
# f3 ╮
# f4 ╰
# f5 ─
# f6 ╯
# f7 │

PATH_TILES = {

    # retas
    frozenset(["left", "right"]): "f2",
    frozenset(["up", "down"]): "f7",

    # cantos
    frozenset(["right", "down"]): "f1",
    frozenset(["left", "down"]): "f3",

    frozenset(["right", "up"]): "f4",
    frozenset(["left", "up"]): "f6",
}


def direction(current, neighbor):

    x, y = current
    nx, ny = neighbor

    if nx < x:
        return "left"

    if nx > x:
        return "right"

    if ny < y:
        return "up"

    if ny > y:
        return "down"

    raise ValueError("Current and neighbor cannot be the same position.")


def expand_path(points):

    path = []

    for i in range(len(points) - 1):

        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        # trecho horizontal
        if y1 == y2:

            step = 1 if x2 > x1 else -1

            for x in range(x1, x2, step):
                path.append((x, y1))

        # trecho vertical
        elif x1 == x2:

            step = 1 if y2 > y1 else -1

            for y in range(y1, y2, step):
                path.append((x1, y))

        else:
            raise ValueError(
                "Path segments must be horizontal or vertical."
            )

    path.append(points[-1])

    return path


def draw_path(ground_map, points):

    path = expand_path(points)

    # desenha os tiles internos
    for i in range(1, len(path) - 1):

        previous = path[i - 1]
        current = path[i]
        next_point = path[i + 1]

        connections = frozenset([
            direction(current, previous),
            direction(current, next_point)
        ])

        tile = PATH_TILES[connections]

        x, y = current

        ground_map[y][x] = tile

    # ========================================================
    # EXTREMIDADES
    # ========================================================

    # primeiro tile
    first = path[0]
    second = path[1]

    first_direction = direction(first, second)

    if first_direction in ("left", "right"):
        first_tile = "f2"
    else:
        first_tile = "f7"

    x, y = first
    ground_map[y][x] = first_tile

    # último tile
    last = path[-1]
    before_last = path[-2]

    last_direction = direction(last, before_last)

    if last_direction in ("left", "right"):
        last_tile = "f5"
    else:
        last_tile = "f7"

    x, y = last
    ground_map[y][x] = last_tile


# ============================================================
# PATH
# ============================================================

PATH_POINTS = [
    (0, 6),
    (7, 6),
    (7, 3),
    (17, 3),
    (17, 8),
    (24, 8),
]

draw_path(
    GROUND_MAP,
    PATH_POINTS
)


# ============================================================
# TREES
# ============================================================

OBJECT_MAP[2][2] = "t1"
OBJECT_MAP[7][7] = "t2"

OBJECT_MAP[8][19] = "t1"
OBJECT_MAP[7][23] = "t2"


# ============================================================
# BUILDINGS
# ============================================================

OBJECT_MAP[3][15] = "c1"

OBJECT_MAP[10][8] = "f8"
OBJECT_MAP[7][15] = "f9"
OBJECT_MAP[5][19] = "f10"



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

MAP_WIDTH = MAP_COLS * TILE_SIZE
MAP_HEIGHT = MAP_ROWS * TILE_SIZE


# ============================================================
# BACKGROUND
# ============================================================

background = Image.new(
    "RGBA",
    (MAP_WIDTH, MAP_HEIGHT),
    (0, 0, 0, 0)
)

render_layer(
    background,
    GROUND_MAP
)

render_layer(
    background,
    OBJECT_MAP
)

background.save(
    BASE_DIR / "map.png"
)


# ============================================================
# PLAYER
# ============================================================

sprites = [
    Image.open(
        BASE_DIR / "assets/me/frame_01.png"
    ).convert("RGBA"),

    Image.open(
        BASE_DIR / "assets/me/frame_02.png"
    ).convert("RGBA"),

    Image.open(
        BASE_DIR / "assets/me/frame_03.png"
    ).convert("RGBA"),
]


SPRITE_SIZE = (
    32,
    32
)


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
player_row = 7

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

    # objetos que ficam na frente do personagem
    render_layer(
        img,
        TOP_MAP
    )

    frames.append(img)


# ============================================================
# SAVE GIF
# ============================================================

frames[0].save(
    BASE_DIR / "world.gif",
    save_all=True,
    append_images=frames[1:],
    duration=180,
    loop=0
)


print("map.png generated!")
print("world.gif generated!")