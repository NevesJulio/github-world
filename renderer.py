"""Desenha o cenário e anima o personagem sobre os caminhos."""
import base64
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from assets import assets
from layout import TILE_SIZE

BASE_DIR = Path(__file__).resolve().parent
SHOW_PATH_TILES = False


def make_info_panel(title, content_size, font):
    padding_x = 12
    title_height = 24
    padding_bottom = 6
    text_box = font.getbbox(title)
    text_width = text_box[2] - text_box[0]
    width = max(content_size[0] + padding_x*2, text_width + padding_x*2)
    height = content_size[1] + title_height + padding_bottom
    panel = Image.new('RGBA', (width, height), (18, 42, 30, 210))
    draw = ImageDraw.Draw(panel)
    draw.rounded_rectangle(
        (0, 0, width-1, height-1),
        radius=8,
        outline=(220, 235, 180, 255),
        width=2,
    )
    draw.text(
        (width//2, 8), title, font=font, anchor='mt',
        fill=(230, 240, 230, 255),
    )
    return panel, title_height, padding_bottom


def repository_icon(profile, size=(80, 80)):
    """Decodifica nome-do-repositorio.png ou cria um fallback com a inicial."""
    if profile.icon_base64:
        try:
            source = Image.open(BytesIO(base64.b64decode(profile.icon_base64))).convert('RGBA')
            contained = ImageOps.contain(source, size, Image.Resampling.NEAREST)
            icon = Image.new('RGBA', size, (0, 0, 0, 0))
            icon.paste(contained, ((size[0]-contained.width)//2, (size[1]-contained.height)//2), contained)
            return icon
        except (OSError, ValueError):
            pass
    icon = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    draw.ellipse((8, 8, size[0]-9, size[1]-9), fill=(42, 112, 72, 255), outline=(220, 235, 180, 255), width=2)
    font = ImageFont.truetype(str(BASE_DIR/'assets/fonts/pixel.ttf'), 28)
    draw.text((size[0]//2, size[1]//2), profile.name[:1].upper(), font=font, anchor='mm', fill='white')
    return icon


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
        # A rota continua existindo para guiar o personagem e reservar espaço
        # entre os objetos. Sua aparência pode ser ligada novamente sem mexer
        # na lógica do layout.
        if SHOW_PATH_TILES:
            for x,y in sorted(island.paths):
                paste_asset(canvas, 'path1', x,y)
        for name,x,y in sorted(island.objects, key=lambda obj: (obj[2]+assets.get(obj[0]).height,obj[1])):
            paste_asset(canvas,name,x,y)
        for name,x,y in sorted(island.overlays, key=lambda obj: (obj[2],obj[1])):
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
        draw.text((center,TILE_SIZE),title,font=font,anchor='mt',fill='white',stroke_width=1,stroke_fill=(20,35,25,255))
        draw.text((center,2*TILE_SIZE),f'{p.main_language} | {p.files} arquivos | {p.directories} dirs',font=font,anchor='mt',fill=(230,240,230,255),stroke_width=1,stroke_fill=(20,35,25,255))
        labels = {'plaza': 'Poço e horta', 'garden': 'Floresta'}
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
    # O retrato usa os frames frontais; o personagem do mapa mantém os
    # frames laterais e percorre um trecho livre do caminho.
    portrait_sprites = [Image.open(path).convert('RGBA').resize((80,80),Image.Resampling.NEAREST)
               for path in sorted((BASE_DIR/'assets/me/frente').glob('*.png'))]
    walker_sprites = [Image.open(path).convert('RGBA').resize((48,48),Image.Resampling.NEAREST)
                      for path in sorted((BASE_DIR/'assets/me/lado').glob('*.png'))]
    if not portrait_sprites:
        raise ValueError('Nenhum frame de personagem em assets/me/frente.')
    if not walker_sprites:
        raise ValueError('Nenhum frame de personagem em assets/me/lado.')

    first = islands[0]
    runs = [(x,y) for x,y in sorted(first.paths)
            if all((x+n,y) in first.paths for n in range(4))]
    start = min(
        runs,
        key=lambda p: abs(p[0]-first.modules[0].anchor[0]) + abs(p[1]-first.modules[0].anchor[1]),
    ) if runs else first.modules[0].anchor
    start_x, path_y = (n*TILE_SIZE for n in start)
    outbound = list(range(0,49,4))
    returning = list(range(44,-1,-4))
    offsets = outbound + returning if runs else [0]*len(walker_sprites)

    panel_font = ImageFont.truetype(str(BASE_DIR/'assets/fonts/pixel.ttf'), 8)
    panel_title = 'NevesJulio'
    portrait_width = max(sprite.width for sprite in portrait_sprites)
    portrait_height = max(sprite.height for sprite in portrait_sprites)
    panel, panel_title_height, panel_padding_bottom = make_info_panel(
        panel_title,
        (portrait_width, portrait_height),
        panel_font,
    )
    panel_width, panel_height = panel.size
    panel_x = background.width - panel_width - 24
    panel_y = 56

    repo_icon = repository_icon(first.profile)
    repo_panel, repo_title_height, repo_padding_bottom = make_info_panel(
        first.profile.name,
        repo_icon.size,
        panel_font,
    )
    repo_panel_x = 24
    repo_panel_y = panel_y
    frames = []
    for i, offset in enumerate(offsets):
        frame = background.copy()
        frame.alpha_composite(panel, (panel_x, panel_y))
        portrait = portrait_sprites[i % len(portrait_sprites)]
        bob = (0, 1, 0, -1)[i % 4]
        portrait_x = panel_x + (panel_width-portrait.width)//2
        portrait_y = panel_y + panel_height-portrait.height-panel_padding_bottom+bob
        frame.paste(portrait, (portrait_x, portrait_y), portrait)

        frame.alpha_composite(repo_panel, (repo_panel_x, repo_panel_y))
        repo_icon_x = repo_panel_x + (repo_panel.width-repo_icon.width)//2
        repo_icon_y = repo_panel_y + repo_title_height
        frame.paste(repo_icon, (repo_icon_x, repo_icon_y), repo_icon)

        walker = walker_sprites[i % len(walker_sprites)]
        # Os frames laterais originais olham para a esquerda.
        if runs and i < len(outbound):
            walker = walker.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        frame.paste(
            walker,
            (start_x+offset, path_y-walker.height+TILE_SIZE),
            walker,
        )
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
