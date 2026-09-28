from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
from assets_config_V2 import assets, DECORATION_GROUPS
from github_activity import get_top_repositories


BASE_DIR = Path(__file__).resolve().parent

TILE_SIZE = 16

top_repos = get_top_repositories(3)

print(top_repos)


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
# decoração
# ============================================================


def place_decorations(
    layer,
    valid_positions,
    group,
    amount
):
    decorations = DECORATION_GROUPS[group]

    available_positions = [
        (x, y)
        for x, y in valid_positions
        if layer[y][x] is None
    ]

    for _ in range(amount):

        if not available_positions:
            break

        x, y = random.choice(available_positions)
        asset_name = random.choice(decorations)

        layer[y][x] = asset_name

        available_positions.remove((x, y))


# ============================================================
# mapa
# ============================================================


def show_minimap(
    layer,
    lines,
    asset_name="y1",
    width=120,
    margin=15,
    font_size=15,
    text_x=15,
    text_y=30,
    line_spacing=50
):
    """
    Mostra o mapa com informações escritas nele.

    text_x / text_y:
        posição do texto dentro do asset ORIGINAL.

    line_spacing:
        distância entre as linhas.
    """

    asset = assets.get(asset_name)

    # cópia do mapa original
    minimap = asset.image.copy()

    # fonte
    font = ImageFont.truetype(
        BASE_DIR / "assets/fonts/pixel.ttf",
        font_size
    )

    draw = ImageDraw.Draw(minimap)

    # ========================================================
    # ESCREVE INFORMAÇÕES
    # ========================================================

    current_y = text_y

    for line in lines:

        draw.text(
            (text_x, current_y),
            line,
            font=font,
            fill=(0, 0, 0, 255)
        )

        current_y += line_spacing

    # ========================================================
    # REDIMENSIONA MAPA + TEXTO
    # ========================================================

    ratio = width / minimap.width

    height = int(
        minimap.height * ratio
    )

    minimap = minimap.resize(
        (width, height),
        Image.Resampling.NEAREST
    )

    # ========================================================
    # POSIÇÃO NA TELA
    # ========================================================

    x = layer.width - minimap.width - margin - 80
    y = margin - 20

    layer.paste(
        minimap,
        (x, y),
        minimap
    )



# ============================================================
# BRIDGE SYSTEM
# ============================================================

def create_bridgeH(
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


def create_bridgeV(
    layer,
    start,
    end
):
    """
    Cria uma ponte vertical.

    p4 = início
    p5 = meio
    p6 = final
    """

    start_x, start_y = start
    end_x, end_y = end

    if start_x != end_x:
        raise ValueError(
            "Bridge must be vertical."
        )

    if start_y > end_y:
        start_y, end_y = end_y, start_y

    if end_y - start_y < 2:
        raise ValueError(
            "Bridge must be at least 3 tiles long."
        )

    # início
    layer[start_y][start_x] = "p4"

    # meio
    for y in range(start_y + 1, end_y):
        layer[y][start_x] = "p5"

    # final
    layer[end_y][start_x] = "p6"

# ============================================================
# REPOSITORY TAG
# ============================================================

def create_repo_tag(
    layer,
    repo_name,
    center_x,
    y,
    font_size=10,
    scale=4,
    opacity=0.7,
    offset_y=20,
    padding_x=16
):
    """
    Cria uma tag para o repositório.

    - Mantém a fonte no tamanho escolhido.
    - Aumenta a largura da tag se o nome for grande.
    - Centraliza usando o bounding box real da fonte.
    """
    text_offset_y = -5  # ajuste fino para centralizar verticalmente
    # ========================================================
    # CARREGA TAG BASE
    # ========================================================

    original_tag = Image.open(
        BASE_DIR / "assets/tag.png"
    ).convert("RGBA")

    tag = original_tag.resize(
        (
            original_tag.width * scale,
            original_tag.height * scale
        ),
        Image.Resampling.NEAREST
    )

    # ========================================================
    # FONTE
    # ========================================================

    font = ImageFont.truetype(
        BASE_DIR / "assets/fonts/pixel.ttf",
        font_size
    )

    # Canvas temporário apenas para medir o texto
    temp_draw = ImageDraw.Draw(tag)

    bbox = temp_draw.textbbox(
        (0, 0),
        repo_name,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # ========================================================
    # AUMENTA TAG HORIZONTALMENTE SE NECESSÁRIO
    # ========================================================

    required_width = int(text_width * 1.5) + (padding_x * 2)

    if required_width > tag.width:

        tag = tag.resize(
            (
                required_width,
                tag.height
            ),
            Image.Resampling.NEAREST
        )

    # ========================================================
    # OPACIDADE DA TAG
    # ========================================================

    alpha = tag.getchannel("A")

    alpha = alpha.point(
        lambda p: int(p * opacity)
    )

    tag.putalpha(alpha)

    # ========================================================
    # RECALCULA DRAW
    # ========================================================

    draw = ImageDraw.Draw(tag)

    bbox = draw.textbbox(
        (0, 0),
        repo_name,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # ========================================================
    # CENTRALIZA CORRETAMENTE
    # ========================================================

    text_x = (
        tag.width // 2
        - (bbox[0] + bbox[2]) // 2
    )

    text_y = (
        tag.height // 2
        - (bbox[1] + bbox[3]) // 2
        + text_offset_y
    )

    # ========================================================
    # DESENHA TEXTO
    # ========================================================

    draw.text(
        (text_x, text_y),
        repo_name,
        font=font,
        fill=(0, 0, 0, 255)
    )

    # ========================================================
    # CENTRALIZA A TAG NO MAPA
    # ========================================================

    center_pixel_x = center_x * TILE_SIZE

    x = center_pixel_x - tag.width // 2

    pixel_y = (
        y * TILE_SIZE
        + offset_y
    )

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
    detail_layer,
    center_x,
    center_y,
    width,
    height,
    entrance=True,
    decorate=True
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

    # ========================================================
    # DECORAÇÃO DA ILHA
    # ========================================================

    if decorate:

        # quantidade baseada no tamanho da ilha
        island_area = width * height

        num_rocks = max(10, island_area // 35)
        num_leaves = max(25, island_area // 25)

        # ----------------------------------------------------
        # posições válidas
        # ----------------------------------------------------

        valid_positions = []

        for row_index, (left, right) in enumerate(rows):

            y = start_y + row_index

            if not 0 <= y < MAP_ROWS:
                continue

            # evita colocar decoração exatamente na borda
            safe_left = left + 2
            safe_right = right - 2

            for x in range(safe_left, safe_right + 1):

                if not 0 <= x < MAP_COLS:
                    continue

                valid_positions.append(
                    (x, y)
                )

        # ----------------------------------------------------
        # evita entrada
        # ----------------------------------------------------

        entrance_positions = set()

        if entrance:

            entrance_positions.update({
                (entrance_x, entrance_y),
                (entrance_x + 1, entrance_y),
                (entrance_x + 2, entrance_y),

                (entrance_x, entrance_y + 1),
                (entrance_x + 1, entrance_y + 1),
                (entrance_x + 2, entrance_y + 1),
            })

        valid_positions = [
            position
            for position in valid_positions
            if position not in entrance_positions
        ]

        # ----------------------------------------------------
        # PEDRAS
        # ----------------------------------------------------

        for _ in range(num_rocks):

            if not valid_positions:
                break

            x, y = random.choice(valid_positions)

            # você possui r1 até r10
            rock = f"r{random.randint(1, 10)}"

            detail_layer[y][x] = rock

            valid_positions.remove((x, y))

        # ----------------------------------------------------
        # FOLHAS
        # ----------------------------------------------------

        for _ in range(num_leaves):

            if not valid_positions:
                break

            x, y = random.choice(valid_positions)

            # range(0, 1) = 2 linhas
            # range(5, 9) = 5 colunas
            # portanto 40 folhas
            leaf = f"f{random.randint(1, 10)}"

            detail_layer[y][x] = leaf

            valid_positions.remove((x, y))

        # ----------------------------------------------------
        # decorations de atividade
        # ----------------------------------------------------



    return valid_positions



island_1_positions = create_organic_island(
    GROUND_MAP,
    OBJECT_MAP,
    DETAIL_MAP,
    center_x=25,
    center_y=8,
    width=19,
    height=12
)

island_2_positions = create_organic_island(
    GROUND_MAP,
    OBJECT_MAP,
    DETAIL_MAP,
    center_x=13,
    center_y=22,
    width=17,
    height=12
)

island_3_positions = create_organic_island(
    GROUND_MAP,
    OBJECT_MAP,
    DETAIL_MAP,
    center_x=37,
    center_y=22,
    width=17,
    height=12
)



# ============================================================
# BRIDGE BETWEEN ISLANDS
# ============================================================

create_bridgeH(
    OBJECT_MAP,
    start=(21, 20),
    end=(29, 20)
)

create_bridgeV(
    OBJECT_MAP,
    start=(25, 14),
    end=(25, 22)
)


# ============================================================
# decoração
# ============================================================

place_decorations(
    OBJECT_MAP,
    island_1_positions,
    group="activity",
    amount=3
)

place_decorations(
    OBJECT_MAP,
    island_2_positions,
    group="activity",
    amount=3
)

place_decorations(
    OBJECT_MAP,
    island_3_positions,
    group="activity",
    amount=3
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
    repo_name=top_repos[0],
    center_x=25,
    y=1,
    font_size=10,
    offset_y= -65
)

create_repo_tag(
    background,
    repo_name=top_repos[1],
    center_x=13,
    y=15,
    font_size=10,
    offset_y= -65
)

create_repo_tag(
    background,
    repo_name=top_repos[2],
    center_x=37,
    y=15,
    font_size=10,
    offset_y= -65
)

# ============================================================
# render map
# ============================================================

show_minimap(
    background,
    lines=[
        "NevesJulio",
        "Python: 65%",
        "C++: 20%"
    ],
    text_x=30,
    text_y=45,
    line_spacing=20
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

player_col = 20
player_row = 8

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