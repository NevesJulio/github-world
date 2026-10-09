"""Desenha o cenário e anima o personagem sobre os caminhos."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from assets import assets
from layout import TILE_SIZE

BASE_DIR = Path(__file__).resolve().parent


def paste_asset(canvas, name, x, y):
    sprite = assets.get(name).image
    canvas.paste(sprite, (x*TILE_SIZE, y*TILE_SIZE), sprite)


def render_map(islands, dimensions):
    canvas = Image.new('RGBA', tuple(n*TILE_SIZE for n in dimensions), (0, 0, 0, 0))
    font = ImageFont.truetype(str(BASE_DIR/'assets/fonts/pixel.ttf'), 10)
    draw = ImageDraw.Draw(canvas)
    for island in islands:
        # A união dos hexágonos forma a costa; lados compartilhados desaparecem.
        for x,y in sorted(island.ground):
            left = (x-1,y) not in island.ground
            right = (x+1,y) not in island.ground
            top = (x,y-1) not in island.ground
            bottom = (x,y+1) not in island.ground
            if top:
                tile = 'g1' if left else 'g3' if right else 'g2'
            elif bottom:
                tile = 'g7' if left else 'g9' if right else 'g8'
            else:
                tile = 'g4' if left else 'g6' if right else 'g5'
            paste_asset(canvas,tile,x,y)
        # Jardins têm um tom suave; não há linhas divisórias entre módulos.
        tint = Image.new('RGBA',canvas.size)
        tint_draw = ImageDraw.Draw(tint)
        for module in island.modules:
            if module.kind == 'garden':
                for x,y in module.cells:
                    if all((x+dx,y+dy) in island.ground for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):
                        tint_draw.rectangle((x*TILE_SIZE,y*TILE_SIZE,(x+1)*TILE_SIZE-1,(y+1)*TILE_SIZE-1),fill=(18,95,40,24))
        canvas.alpha_composite(tint)
        for x,y in sorted(island.paths):
            paste_asset(canvas, 'path1', x,y)
        for name,x,y in sorted(island.objects, key=lambda obj: (obj[2]+assets.get(obj[0]).height,obj[1])):
            paste_asset(canvas,name,x,y)
        # Rótulos próprios para identificar os bairros representados.
        for district,x,y in island.districts:
            text = district.name
            while len(text) > 1 and draw.textlength(text, font=font) > 12*TILE_SIZE:
                text = text[:-2] + '…'
            draw.text((x*TILE_SIZE,y*TILE_SIZE+2),text,font=font,fill=(20,25,20,255),stroke_width=1,stroke_fill=(220,235,180,255))
        p = island.profile
        center = (island.x+island.width/2)*TILE_SIZE
        title = p.name + (' *' if p.incomplete else '')
        draw.text((center,(island.y-3)*TILE_SIZE),title,font=font,anchor='mt',fill='white',stroke_width=1,stroke_fill=(20,35,25,255))
        draw.text((center,(island.y-2)*TILE_SIZE),f'{p.main_language} | {p.files} arquivos | {p.directories} dirs',font=font,anchor='mt',fill=(230,240,230,255),stroke_width=1,stroke_fill=(20,35,25,255))
        labels = {'plaza': 'Praça', 'garden': 'Jardim', 'workshop': 'Oficina', 'tests': 'Testes', 'docs': 'Documentação'}
        for module in island.modules:
            if module.kind in labels:
                cx,cy = module.center
                draw.text((cx*TILE_SIZE,(cy-6)*TILE_SIZE),labels[module.kind],font=font,anchor='mt',fill=(20,45,25,255))
    for left,right in zip(islands,islands[1:]):
        sx,sy = left.exit
        ex,ey = right.entrance
        middle = (sx+ex)//2
        for x in range(sx+1,middle+1):
            paste_asset(canvas,'p2',x,sy-1)
        for y in range(min(sy,ey),max(sy,ey)+1):
            paste_asset(canvas,'p5',middle,y)
        for x in range(middle,ex):
            paste_asset(canvas,'p2',x,ey-1)
    return canvas


def save_world(islands, dimensions, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True,exist_ok=True)
    background = render_map(islands,dimensions)
    background.save(output_dir/'map.png')
    # Retrato animado: os frames de frente ficam em um painel no canto
    # superior direito, independentes dos caminhos do mapa.
    player_size = (64, 64)
    sprites = [Image.open(path).convert('RGBA').resize(player_size,Image.Resampling.NEAREST)
               for path in sorted((BASE_DIR/'assets/me/frente').glob('*.png'))]
    if not sprites:
        raise ValueError('Nenhum frame de personagem em assets/me/frente.')

    panel_width, panel_height = 96, 96
    panel_x = background.width - panel_width - 24
    panel_y = 56
    frames = []
    for i, sprite in enumerate(sprites):
        frame = background.copy()
        panel = Image.new('RGBA', (panel_width, panel_height), (18, 42, 30, 210))
        panel_draw = ImageDraw.Draw(panel)
        panel_draw.rounded_rectangle(
            (0, 0, panel_width-1, panel_height-1),
            radius=8,
            outline=(220, 235, 180, 255),
            width=2,
        )
        panel_draw.text(
            (panel_width//2, 8),
            'PERSONAGEM',
            font=ImageFont.truetype(str(BASE_DIR/'assets/fonts/pixel.ttf'), 8),
            anchor='mt',
            fill=(230, 240, 230, 255),
        )
        frame.alpha_composite(panel, (panel_x, panel_y))
        bob = (0, 1, 0, -1)[i % 4]
        sprite_x = panel_x + (panel_width-sprite.width)//2
        sprite_y = panel_y + panel_height-sprite.height-5+bob
        frame.paste(sprite, (sprite_x, sprite_y), sprite)
        frames.append(frame)
    # GIF só suporta transparência binária. Reserve o índice 255 em todos os frames.
    palette = background.convert('RGB').quantize(colors=255).getpalette()
    palette[255*3:256*3] = [0,0,0]
    reference = Image.new('P',(1,1))
    reference.putpalette(palette)
    indexed = []
    for frame in frames:
        converted = frame.convert('RGB').quantize(palette=reference,dither=Image.Dither.NONE)
        transparent = frame.getchannel('A').point(lambda a: 255 if a < 128 else 0)
        converted.paste(255,mask=transparent)
        converted.info['transparency'] = 255
        indexed.append(converted)
    indexed[0].save(output_dir/'world.gif',save_all=True,append_images=indexed[1:],duration=120,loop=0,disposal=2,transparency=255,background=255,optimize=False)
