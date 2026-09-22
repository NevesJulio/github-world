from PIL import Image

# ============================================================
# CONFIG
# ============================================================

TILE_SIZE = 16

# ============================================================
# TILESETS
# ============================================================

tileset_grass = Image.open(
    "/workspaces/github-world/taiga_.png"
).convert("RGBA")

tileset_path = Image.open(
    "/workspaces/github-world/forestPath_.png"
).convert("RGBA")


def get_tile(col, row, tileset, size):
    x = col * size
    y = row * size

    return tileset.crop((
        x,
        y,
        x + size,
        y + size
    ))


# ============================================================
# TILES
# ============================================================

grass = get_tile(
    8, 1,
    tileset_grass,
    TILE_SIZE
)

floor = get_tile(
    6, 1,
    tileset_path,
    TILE_SIZE
)


# ============================================================
# MAP
# ============================================================

MAP = [
    "GGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGG",
    "PPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPP",
    "GGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGG",
]

tiles = {
    "G": grass,
    "P": floor,
}


# ============================================================
# RENDER MAP
# ============================================================

MAP_WIDTH = len(MAP[0]) * TILE_SIZE
MAP_HEIGHT = len(MAP) * TILE_SIZE

background = Image.new(
    "RGBA",
    (MAP_WIDTH, MAP_HEIGHT)
)

for row, line in enumerate(MAP):

    for col, tile_code in enumerate(line):

        tile = tiles[tile_code]

        x = col * TILE_SIZE
        y = row * TILE_SIZE

        background.paste(
            tile,
            (x, y),
            tile
        )


# Salva só para conseguirmos visualizar o mapa
background.save("map.png")


# ============================================================
# PLAYER
# ============================================================

sprites = [
    Image.open("assets/me/frame_01.png").convert("RGBA"),
    Image.open("assets/me/frame_02.png").convert("RGBA"),
    Image.open("assets/me/frame_03.png").convert("RGBA"),
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

# Vamos colocar o boneco no centro do mapa

player_x = MAP_WIDTH // 2

# Linha 5 do mapa = caminho
player_y = 6 * TILE_SIZE


# ============================================================
# ANIMATION
# ============================================================

frames = []

for frame_number in range(len(sprites)):

    # IMPORTANTE:
    # Agora copiamos o mapa, em vez de criar fundo branco
    img = background.copy()

    sprite = sprites[frame_number]

    position = (
        player_x - sprite.width // 2,
        player_y - sprite.height
    )

    img.paste(
        sprite,
        position,
        sprite
    )

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