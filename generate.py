from PIL import Image
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

    start e end usam:
        (col, row)

    Exemplo:
        start = (10, 8)
        end   = (18, 8)
    """

    start_x, start_y = start
    end_x, end_y = end

    # Por enquanto somente ponte horizontal
    if start_y != end_y:
        raise ValueError(
            "Bridge must be horizontal."
        )

    # garante que start está à esquerda
    if start_x > end_x:
        start_x, end_x = end_x, start_x

    # precisa existir espaço para começo e fim
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
# ISLAND SYSTEM
# ============================================================

# Estrutura lógica dos tiles:
#
# g1  g2  g3
# g4  g5  g6
# g7  g8  g9
#
# g1 = canto superior esquerdo
# g2 = borda superior
# g3 = canto superior direito
#
# g4 = borda esquerda
# g5 = centro
# g6 = borda direita
#
# g7 = canto inferior esquerdo
# g8 = borda inferior
# g9 = canto inferior direito




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

    width:
        largura máxima da ilha.

    height:
        altura total da ilha.

    entrance:
        coloca automaticamente x3 centralizado
        na frente da ilha.
    """

    # largura mínima
    width = max(7, width)

    # altura mínima
    height = max(6, height)

    # --------------------------------------------------------
    # CONFIGURAÇÃO DO FORMATO
    # --------------------------------------------------------

    # quanto a primeira/última linha ficam recuadas
    top_inset = 4

    # largura da região principal
    full_width = width

    # largura da parte superior/inferior
    narrow_width = width - (top_inset * 2)

    # --------------------------------------------------------
    # CRIA AS LARGURAS DAS LINHAS
    # --------------------------------------------------------

    widths = []

    # topo
    widths.append(narrow_width)

    # transição superior
    widths.append(full_width)

    # parte central
    middle_rows = height - 4

    for _ in range(middle_rows):
        widths.append(full_width)

    # transição inferior
    widths.append(full_width)

    # base
    widths.append(narrow_width)

    # --------------------------------------------------------
    # POSIÇÕES
    # --------------------------------------------------------

    start_y = center_y - height // 2

    rows = []

    for row_width in widths:

        left = center_x - row_width // 2
        right = left + row_width - 1

        rows.append((left, right))

    # --------------------------------------------------------
    # DESENHA A ILHA
    # --------------------------------------------------------

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

        # x3 possui largura de 3 tiles.
        # -1 centraliza o asset em center_x.
        entrance_x = center_x - 1

        # sobrepõe a entrada à parte inferior da ilha
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
# PONTE ENTRE ILHAS
# ============================================================


create_bridge(
    OBJECT_MAP,
    start=(21, 20),
    end=(29, 20)
)



# ============================================================
# subilhas
# ============================================================

# create_organic_island(
#     DETAIL_MAP,
#     center_x=37,
#     center_y=22,
#     widths=[
#         3,
#         7,
#         9,
#         11,
#         11,
#         11,
#         11,
#         9,
#         7,
#         3,
#     ]
# )

# create_organic_island(
#     DETAIL_MAP,
#     center_x=13,
#     center_y=22,
#     widths=[
#         3,
#         7,
#         9,
#         11,
#         11,
#         11,
#         11,
#         9,
#         7,
#         3,
#     ]
# )

# create_organic_island(
#     DETAIL_MAP,
#     center_x=25,
#     center_y=8,
#     widths=[
#         3,
#         7,
#         9,
#         11,
#         11,
#         11,
#         11,
#         9,
#         7,
#         3,
#     ]
# )


# ============================================================
# BUILDINGS
# ============================================================

# Casas disponíveis:
#
# laranja
# co1
# co2
# co3
#
# cinza
# cc1
# cc2
# cc3
#
# verde
# cv1
# cv2
# cv3




# Ilha 2
OBJECT_MAP[5][25] = "cc1"


# Ilha 3
OBJECT_MAP[19][9] = "cv1"


# Ilha 4
OBJECT_MAP[19][33] = "co2"


# ============================================================
# OPTIONAL DETAILS
# ============================================================

# Depois podemos colocar aqui:
#
# pedras:
# p1, p2, p3...
#
# cercas:
# c1, c2, c3...
#
# folhas:
# f1, f2, f3...
#
#
# Exemplos:
#
# DETAIL_MAP[10][10] = "p1"
# DETAIL_MAP[9][15] = "f1"


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

# Primeira ilha

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