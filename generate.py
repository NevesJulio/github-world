from PIL import Image, ImageDraw

WIDTH = 800
HEIGHT = 160

# -----------------------
# MAP
# -----------------------

nodes = {
    "Python": (150, 80),
    "AI / ML": (400, 80),
    "C++": (650, 80),
}

# -----------------------
# PLAYER SPRITES
# -----------------------

sprites = [
    Image.open("assets/me/frame_01.png").convert("RGBA"),
    Image.open("assets/me/frame_02.png").convert("RGBA"),
    Image.open("assets/me/frame_03.png").convert("RGBA"),
]

# Ajuste se seus sprites estiverem grandes
SPRITE_SIZE = (32, 32)

sprites = [
    sprite.resize(SPRITE_SIZE, Image.Resampling.NEAREST)
    for sprite in sprites
]

# -----------------------
# ANIMATION
# -----------------------

start_x = 80
end_x = nodes["Python"][0]

player_y = 90

number_of_frames = 30

frames = []

for frame_number in range(number_of_frames):

    # Cria fundo
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    # Caminho
    draw.line(
        (150, 80, 650, 80),
        fill="gray",
        width=3
    )

    # Nós
    for name, (x, y) in nodes.items():

        draw.ellipse(
            (x - 8, y - 8, x + 8, y + 8),
            fill="black"
        )

        draw.text(
            (x - 25, y - 35),
            name,
            fill="black"
        )

    # -----------------------
    # PLAYER POSITION
    # -----------------------

    progress = frame_number / (number_of_frames - 1)

    player_x = int(
        start_x + (end_x - start_x) * progress
    )

    # Alterna os sprites
    sprite = sprites[
        frame_number % len(sprites)
    ]

    # Centraliza o sprite
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

# -----------------------
# SAVE GIF
# -----------------------

frames[0].save(
    "world.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0
)

print("world.gif generated!")