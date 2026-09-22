from PIL import Image, ImageDraw

WIDTH = 800
HEIGHT = 160

img = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(img)

nodes = {
    "Python": (150, 80),
    "AI / ML": (400, 80),
    "C++": (650, 80),
}

# Paths
draw.line((150, 80, 650, 80), fill="gray", width=3)

# Nodes
for name, (x, y) in nodes.items():
    draw.ellipse((x-8, y-8, x+8, y+8), fill="black")
    draw.text((x-25, y-35), name, fill="black")

# Temporary player
player_x = 350
player_y = 105

draw.rectangle(
    (player_x-5, player_y-10, player_x+5, player_y+10),
    fill="black"
)

img.save("world.png")