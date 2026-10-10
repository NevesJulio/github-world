"""Colônias de hexágonos anexados pelos seis lados, com caminhos conectados."""
from collections import deque
from dataclasses import dataclass, field
import hashlib
import random
from assets import assets, DECORATION_GROUPS
from repo_profile import DirectoryProfile
from visual_config import farm_settings, flower_assets_for, house_style, tree_assets_for

TILE_SIZE = 16
DIRECTIONS = ((1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1))


def hex_center(q, r):
    return 12*q, 16*r + 8*q


def hex_cells(q, r):
    """Hexágono de 16×16 tiles; centros em coordenadas axiais."""
    cx, cy = hex_center(q, r)
    return {(x, y) for x in range(cx-8, cx+8) for y in range(cy-8, cy+8)
            if abs(x+.5-cx) + .5*abs(y+.5-cy) <= 8}


@dataclass
class Module:
    key: str
    kind: str
    q: int
    r: int
    parent: tuple | None = None
    cells: set = field(default_factory=set)
    center: tuple = (0, 0)
    anchor: tuple = (0, 0)


@dataclass
class Island:
    profile: object
    x: int
    y: int
    width: int
    height: int
    objects: list = field(default_factory=list)
    overlays: list = field(default_factory=list)
    paths: set = field(default_factory=set)
    occupied: set = field(default_factory=set)
    districts: list = field(default_factory=list)
    modules: list = field(default_factory=list)
    ground: set = field(default_factory=set)
    entrance: tuple = (0, 0)
    exit: tuple = (0, 0)

    def place(self, name, x, y, allowed=None):
        tile = assets.get(name)
        cells = {(a, b) for a in range(x, x+tile.width) for b in range(y, y+tile.height)}
        if cells & (self.occupied | self.paths) or not cells <= (self.ground if allowed is None else allowed):
            return False
        self.occupied.update(cells)
        self.objects.append((name, x, y))
        return True

    def overlay(self, name, x, y, allowed=None):
        tile = assets.get(name)
        cells = {(a, b) for a in range(x, x+tile.width) for b in range(y, y+tile.height)}
        if not cells <= (self.ground if allowed is None else allowed):
            return False
        self.overlays.append((name, x, y))
        return True


def attach(modules, key, kind, seed):
    occupied = {(m.q, m.r) for m in modules}
    # Escolha de borda local e reproduzível. Os vazios preservam braços orgânicos.
    candidates = {}
    for m in modules:
        for dq, dr in DIRECTIONS:
            cell = m.q+dq, m.r+dr
            if cell not in occupied:
                candidates.setdefault(cell, (m.q, m.r))
    def score(cell):
        q, r = cell
        radius = max(abs(q), abs(r), abs(q+r))
        noise = int.from_bytes(hashlib.sha256(f'{seed}/{key}/{q}/{r}'.encode()).digest()[:4], 'big') / 2**32
        neighbors = sum((q+dq, r+dr) in occupied for dq, dr in DIRECTIONS)
        return radius*1.2 + noise - .08*neighbors
    q, r = min(candidates, key=score)
    modules.append(Module(key, kind, q, r, candidates[(q, r)]))


def connect(island, start, end):
    """Busca um caminho sobre a terra que contorna as construções."""
    queue = deque([start])
    previous = {start: None}
    while queue:
        point = queue.popleft()
        if point == end:
            while point is not None:
                island.paths.add(point)
                point = previous[point]
            return
        x, y = point
        for next_point in ((x+1,y),(x,y+1),(x-1,y),(x,y-1)):
            if next_point in island.ground and next_point not in island.occupied and next_point not in previous:
                previous[next_point] = point
                queue.append(next_point)
    raise ValueError(f'Caminho desconectado em {island.profile.name}: {start} → {end}')


def build_colony(profile):
    # Composição manual da ilha: casa no centro, floresta à esquerda e
    # poço/horta à direita. q/r são as coordenadas dos honeycombs.
    modules = [
        Module('main-house', 'house', 0, 0),
        # Posições opostas deixam a casa exatamente no meio da composição.
        Module('garden0', 'garden', -1, 1, (0, 0)),
        Module('plaza', 'plaza', 1, -1, (0, 0)),
    ]
    main_district = DirectoryProfile('Projeto', profile.files, profile.max_depth)
    farm = farm_settings(profile)
    terrain = set().union(*(hex_cells(m.q, m.r) for m in modules))
    min_x, min_y = min(x for x,y in terrain), min(y for x,y in terrain)
    shift_x, shift_y = -min_x, -min_y
    ground = {(x+shift_x,y+shift_y) for x,y in terrain}
    island = Island(profile, 0, 0, max(x for x,y in ground)+1, max(y for x,y in ground)+1, modules=modules, ground=ground)
    for m in modules:
        cx, cy = hex_center(m.q, m.r)
        m.center = cx+shift_x, cy+shift_y
        m.cells = {(x+shift_x,y+shift_y) for x,y in hex_cells(m.q,m.r)}
        cx, cy = m.center
        m.anchor = cx, cy+5
        if m.kind == 'house':
            name = f'{house_style(profile)}{main_district.size}'
            if main_district.size == 3:
                name += '_compact'
            tile = assets.get(name)
            bx, by = cx-tile.width//2, cy-4
            if not island.place(name,bx,by,m.cells):
                raise ValueError(f'Casa não cabe no módulo {m.key}')
            island.districts.append((main_district,bx,by+tile.height))
            connect(island,m.anchor,(cx,by+tile.height))
        elif m.kind == 'plaza':
            name = 'm13' if (profile.days_inactive or 0) > 90 else 'm18'
            if profile.days_inactive is None:
                name = 'm18'
            island.place(name,cx-5,cy-2,m.cells)
            if farm['enabled']:
                # A horta divide a praça com o poço. Pedras formam o limite
                # visual e as flores usam uma camada acima dos canteiros.
                bed_xs = list(range(cx+1,cx+4))[:farm['beds']]
                bed_top, bed_bottom = cy-2, cy
                farm_rng = random.Random(f'{profile.name}/farm')
                for x in bed_xs:
                    island.place('h',x,bed_top,m.cells)
                fence_left, fence_right = bed_xs[0]-1, bed_xs[-1]+1
                fence_top, fence_bottom = bed_top-1, bed_bottom+1
                island.place('farm_fence_tl',fence_left,fence_top,m.cells)
                island.place('farm_fence_tr',fence_right,fence_top,m.cells)
                island.place('farm_fence_bl',fence_left,fence_bottom,m.cells)
                island.place('farm_fence_br',fence_right,fence_bottom,m.cells)
                for x in range(fence_left+1,fence_right):
                    island.place('farm_fence_top',x,fence_top,m.cells)
                    island.place('farm_fence_bottom',x,fence_bottom,m.cells)
                for y in range(fence_top+1,fence_bottom):
                    island.place('farm_fence_left',fence_left,y,m.cells)
                    island.place('farm_fence_right',fence_right,y,m.cells)

                # As pedras são sorteadas apenas no anel exterior da cerca.
                outer_rocks = (
                    [(x,fence_top-1) for x in range(fence_left-1,fence_right+2)]
                    + [(x,fence_bottom+1) for x in range(fence_left-1,fence_right+2)]
                    + [(fence_left-1,y) for y in range(fence_top,fence_bottom+1)]
                    + [(fence_right+1,y) for y in range(fence_top,fence_bottom+1)]
                )
                outer_rocks = list(dict.fromkeys(outer_rocks))
                farm_rng.shuffle(outer_rocks)
                placed_rocks = 0
                for x,y in outer_rocks:
                    if island.place(f'r{farm_rng.randint(1,10)}',x,y,m.cells):
                        placed_rocks += 1
                        if placed_rocks >= farm['extra_rocks']:
                            break
                flower_spots = [(x,y) for y in range(bed_top,bed_bottom+1) for x in bed_xs]
                farm_rng.shuffle(flower_spots)
                for x,y in flower_spots[:farm['flowers']]:
                    island.overlay(farm_rng.choice(DECORATION_GROUPS['flowers']),x,y,m.cells)
    lookup = {(m.q,m.r): m for m in modules}
    for m in modules:
        if m.parent is not None:
            connect(island, lookup[m.parent].anchor, m.anchor)
    # Portas nos extremos horizontais: usadas pelas pontes entre colônias.
    reachable = {modules[0].anchor}
    queue = deque(reachable)
    while queue:
        px,py = queue.popleft()
        for point in ((px+1,py),(px-1,py),(px,py+1),(px,py-1)):
            if point in ground-island.occupied and point not in reachable:
                reachable.add(point)
                queue.append(point)
    available = {p for p in reachable if p[1] == modules[0].anchor[1]}
    island.entrance = min(available, key=lambda p: (p[0], abs(p[1]-modules[0].anchor[1])))
    island.exit = min(available, key=lambda p: (-p[0], abs(p[1]-modules[0].anchor[1])))
    connect(island,modules[0].anchor,island.entrance)
    connect(island,modules[0].anchor,island.exit)
    trees = tree_assets_for(profile)
    flowers = flower_assets_for(profile)
    for m in modules:
        rng = random.Random(f'{profile.name}/{m.key}')
        def decorate(names, amount):
            if amount <= 0:
                return
            positions = sorted(m.cells)
            rng.shuffle(positions)
            placed = 0
            for x,y in positions:
                if island.place(rng.choice(names),x,y,m.cells):
                    placed += 1
                    if placed >= amount:
                        break
        def decorate_exact(names):
            positions = sorted(m.cells)
            rng.shuffle(positions)
            for name in names:
                for x,y in positions:
                    if island.place(name,x,y,m.cells):
                        break
        if m.kind == 'house':
            cx, cy = m.center
            # Pátio da casa: posições manuais mantêm a entrada e o caminho
            # livres. Cada tupla contém (asset, deslocamento x, deslocamento y).
            house_decor = [
                ('m21', -6, 3),      # banco à esquerda
                ('m22', 4, 2),       # placa próxima da entrada
                ('m1', -6, -3),      # caixas nas laterais
                ('m2', 5, -3),
                ('r2', -5, -5),      # pedras ao redor da construção
                ('r5', 4, -5),
                ('r8', -6, 0),
                ('r10', 5, 0),
                ('r4', -5, 4),
                ('r7', 4, 3),
                ('f2', -6, -1),      # vegetação discreta no pátio
                ('f6', 5, -1),
                ('flower2', -5, 2),
                ('flower3', 4, -2),
            ]
            for name, dx, dy in house_decor:
                island.place(name, cx+dx, cy+dy, m.cells)
        elif m.kind == 'garden':
            decorate_exact(trees)
            decorate_exact(flowers)
            decorate([f'f{i}' for i in range(1,11)],6 + min(profile.max_depth,3))
        elif m.kind == 'plaza':
            cx,cy = m.center
            # Barris agrupados num pequeno depósito, em vez de espalhados.
            barrel_pattern = [
                ('m9',cx-7,cy-2), ('m9',cx-6,cy-2),
                ('m6',cx-7,cy+1), ('m9',cx-5,cy+2),
            ]
            for name,x,y in barrel_pattern[:farm['barrels']]:
                island.place(name,x,y,m.cells)
            decorate([f'f{i}' for i in range(1,11)],farm['grass'])
            if profile.has_docs:
                decorate(DECORATION_GROUPS['signs'],1)
            if profile.has_tests:
                decorate(['c1','c2','c3'],2)
            if profile.dependencies:
                decorate(['wood2','m5'],1)
        decorate([f'r{i}' for i in range(1,11)],2)
    return island


def translate(island, dx, dy):
    island.x, island.y = dx, dy
    def move(points):
        return {(x+dx,y+dy) for x,y in points}
    island.ground, island.paths, island.occupied = map(move,(island.ground,island.paths,island.occupied))
    island.objects = [(name,x+dx,y+dy) for name,x,y in island.objects]
    island.overlays = [(name,x+dx,y+dy) for name,x,y in island.overlays]
    island.districts = [(d,x+dx,y+dy) for d,x,y in island.districts]
    island.entrance = island.entrance[0]+dx,island.entrance[1]+dy
    island.exit = island.exit[0]+dx,island.exit[1]+dy
    for m in island.modules:
        m.cells = move(m.cells)
        m.center = m.center[0]+dx,m.center[1]+dy
        m.anchor = m.anchor[0]+dx,m.anchor[1]+dy


def build_layout(profiles):
    if not profiles:
        raise ValueError('Nenhum repositório disponível para desenhar.')
    islands = [build_colony(p) for p in profiles]
    x = 3
    plaza_y = max(i.modules[0].anchor[1] for i in islands)
    # Onze tiles reservam 176 px no topo para os painéis e o título.
    for island in islands:
        translate(island,x,11+plaza_y-island.modules[0].anchor[1])
        x += island.width+4
    return islands,(x-1,max(i.y+i.height for i in islands)+3)
