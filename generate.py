from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

from assets_config_V2 import assets


BASE_DIR = Path(__file__).resolve().parent

TILE_SIZE = 16


# ============================================================
# MAP CONFIG
# ============================================================

MAP_COLS = 50
MAP_ROWS = 30


# ============================================================
# CREATE LAYERS
# ============================================================

GROUND_MAP = [
    [None for _ in range(MAP_COLS)]
    for _ in range(MAP_ROWS)
]

DETAIL_MAP = [
    [None for _ in range(MAP_COLS)]
    for _ in range(MAP_ROWS)
]

PATH_MAP = [
    [None for _ in range(MAP_COLS)]
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
# BRIDGE SYSTEM
# ============================================================

def create_bridge(
    layer,
    start,
    end
):
    """
    Cria uma ponte horizontal.

    p1 = início
    p2 = meio
    p3 = final
    """

    start_x, start_y = start
    end_x, end_y = end

    if start_y != end_y:
        raise ValueError(
            "Bridge must be horizontal."
        )

    if start_x > end_x:
        start_x, end_x = end_x, start_x

    if end_x - start_x < 2:
        raise ValueError(
            "Bridge must be at least 3 tiles long."
        )

    # início
    layer[start_y][start_x] = "p1"

    # meio
    for x in range(start_x + 1, end_x):
        layer[start_y][x] = "p2"

    # final
    layer[start_y][end_x] = "p3"


# ============================================================
# REPOSITORY TAG
# ============================================================

def create_repo_tag(
    layer,
    repo_name,
    center_x,
    y,
    font_size=25,
    scale=3,
    opacity=0.7,
    offset_y=-10
):
    """
    Cria uma tag com o nome do repositório.

    scale:
        tamanho da tag (1, 2, 3...)

    opacity:
        opacidade da tag (0.0 até 1.0)
    """

    # ========================================================
    # CARREGA TAG
    # ========================================================

    tag = Image.open(
        BASE_DIR / "assets/tag.png"
    ).convert("RGBA")


    # ========================================================
    # AUMENTA TAG
    # ========================================================

    tag = tag.resize(
        (
            tag.width * scale,
            tag.height * scale
        ),
        Image.Resampling.NEAREST
    )


    # ========================================================
    # APLICA TRANSPARÊNCIA NA TAG
    # ========================================================

    alpha = tag.getchannel("A")

    alpha = alpha.point(
        lambda p: int(p * opacity)
    )

    tag.putalpha(alpha)


    # ========================================================
    # FONTE
    # ========================================================

    font = ImageFont.truetype(
        BASE_DIR / "assets/fonts/pixel.ttf",
        font_size
    )


    # ========================================================
    # TEXTO
    # ========================================================

    draw = ImageDraw.Draw(tag)

    bbox = draw.textbbox(
        (0, 0),
        repo_name,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (
        tag.width - text_width
    ) // 2

    text_y = (
        (tag.height - text_height) // 2
        - bbox[1]
    )


    # ========================================================
    # ESCREVE TEXTO
    # ========================================================

    draw.text(
        (text_x, text_y),
        repo_name,
        font=font,

        # texto continua totalmente visível
        fill=(0, 0, 0, 255)
    )


    # ========================================================
    # POSIÇÃO NO MAPA
    # ========================================================

    x = (
        center_x * TILE_SIZE
        - tag.width // 2
    )

    pixel_y = y * TILE_SIZE + offset_y


    # ========================================================
    # DESENHA
    # ========================================================

    layer.paste(
        tag,
        (x, pixel_y),
        tag
    )


# ============================================================
# ISLAND SYSTEM
# ============================================================

# Estrutura lógica:
#
# g1  g2  g3
# g4  g5  g6
# g7  g8  g9


def create_organic_island(
    layer,
    object_layer,
    center_x,
    center_y,
    width,
    height,
    entrance=True
):
    """
    Cria uma ilha no formato:

            ╭───────╮
        ╭───         ───╮
        │               │
        │               │
        ╰───         ───╯
            ╰───────╯
    """

    width = max(7, width)
    height = max(6, height)

    # quanto topo/base ficam recuados
    top_inset = 4

    full_width = width
    narrow_width = width - (top_inset * 2)

    # ========================================================
    # DEFINE FORMATO
    # ========================================================

    widths = []

    # topo
    widths.append(narrow_width)

    # transição superior
    widths.append(full_width)

    # centro
    middle_rows = height - 4

    for _ in range(middle_rows):
        widths.append(full_width)

    # transição inferior
    widths.append(full_width)

    # base
    widths.append(narrow_width)

    # ========================================================
    # CALCULA POSIÇÕES
    # ========================================================

    start_y = center_y - height // 2

    rows = []

    for row_width in widths:

        left = center_x - row_width // 2
        right = left + row_width - 1

        rows.append(
            (left, right)
        )

    # ========================================================
    # DESENHA ILHA
    # ========================================================

    for row_index, (left, right) in enumerate(rows):

        y = start_y + row_index

        if not 0 <= y < MAP_ROWS:
            continue

        # ====================================================
        # TOPO
        # ====================================================

        if row_index == 0:

            for x in range(left, right + 1):

                if not 0 <= x < MAP_COLS:
                    continue

                if x == left:
                    tile = "g1"

                elif x == right:
                    tile = "g3"

                else:
                    tile = "g2"

                layer[y][x] = tile

        # ====================================================
        # TRANSIÇÃO SUPERIOR
        # ====================================================

        elif row_index == 1:

            for x in range(left, right + 1):

                if not 0 <= x < MAP_COLS:
                    continue

                if x == left:
                    tile = "g1"

                elif x == right:
                    tile = "g3"

                else:
                    tile = "g5"

                layer[y][x] = tile

        # ====================================================
        # BASE
        # ====================================================

        elif row_index == height - 1:

            for x in range(left, right + 1):

                if not 0 <= x < MAP_COLS:
                    continue

                if x == left:
                    tile = "g7"

                elif x == right:
                    tile = "g9"

                else:
                    tile = "g8"

                layer[y][x] = tile

        # ====================================================
        # TRANSIÇÃO INFERIOR
        # ====================================================

        elif row_index == height - 2:

            for x in range(left, right + 1):

                if not 0 <= x < MAP_COLS:
                    continue

                if x == left:
                    tile = "g7"

                elif x == right:
                    tile = "g9"

                else:
                    tile = "g5"

                layer[y][x] = tile

        # ====================================================
        # CENTRO
        # ====================================================

        else:

            for x in range(left, right + 1):

                if not 0 <= x < MAP_COLS:
                    continue

                if x == left:
                    tile = "g4"

                elif x == right:
                    tile = "g6"

                else:
                    tile = "g5"

                layer[y][x] = tile

    # ========================================================
    # ENTRADA
    # ========================================================

    if entrance:

        bottom_y = start_y + height - 1

        entrance_x = center_x - 1
        entrance_y = bottom_y - 1

        if (
            0 <= entrance_x < MAP_COLS
            and 0 <= entrance_y < MAP_ROWS
        ):
            object_layer[entrance_y][entrance_x] = "x3"


# ============================================================
# ISLAND 2
# ============================================================

create_organic_island(
    GROUND_MAP,
    OBJECT_MAP,
    center_x=25,
    center_y=8,
    width=19,
    height=12
)


# ============================================================
# ISLAND 3
# ============================================================

create_organic_island(
    GROUND_MAP,
    OBJECT_MAP,
    center_x=13,
    center_y=22,
    width=17,
    height=12
)


# ============================================================
# ISLAND 4
# ============================================================

create_organic_island(
    GROUND_MAP,
    OBJECT_MAP,
    center_x=37,
    center_y=22,
    width=17,
    height=12
)


# ============================================================
# BRIDGE BETWEEN ISLANDS
# ============================================================

create_bridge(
    OBJECT_MAP,
    start=(21, 20),
    end=(29, 20)
)


# ============================================================
# BUILDINGS
# ============================================================

# Ilha 2
OBJECT_MAP[5][25] = "cc1"

# Ilha 3
OBJECT_MAP[19][9] = "cv1"

# Ilha 4
OBJECT_MAP[19][33] = "co2"


# ============================================================
# RENDER FUNCTION
# ============================================================

def render_layer(canvas, layer):

    for row, line in enumerate(layer):

        for col, asset_name in enumerate(line):

            if asset_name is None:
                continue

            asset = assets.get(
                asset_name
            )

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


# ============================================================
# RENDER GROUND
# ============================================================

render_layer(
    background,
    GROUND_MAP
)


# ============================================================
# RENDER DETAILS
# ============================================================

render_layer(
    background,
    DETAIL_MAP
)


# ============================================================
# RENDER PATHS
# ============================================================

render_layer(
    background,
    PATH_MAP
)


# ============================================================
# RENDER OBJECTS
# ============================================================

render_layer(
    background,
    OBJECT_MAP
)


# ============================================================
# REPOSITORY TAGS
# ============================================================

create_repo_tag(
    background,
    repo_name="github-world",
    center_x=25,
    y=1,
    font_size=12,
    offset_y=-15
)

create_repo_tag(
    background,
    repo_name="repo-2",
    center_x=13,
    y=15,
    font_size=12,
    offset_y=-15
)

create_repo_tag(
    background,
    repo_name="repo-3",
    center_x=37,
    y=15,
    font_size=12,
    offset_y=-15
)


# ============================================================
# SAVE STATIC MAP
# ============================================================

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

player_col = 12
player_row = 10

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

    # elementos que ficam na frente do personagem
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
    loop=0,
    disposal=2
)


print("map.png generated!")
print("world.gif generated!")