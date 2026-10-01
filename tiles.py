from PIL import Image


class Tile:

    def __init__(
        self,
        name,
        tileset,
        col,
        row,
        width=1,
        height=1,
        tile_size=16
    ):

        self.name = name
        self.tileset = tileset

        self.col = col
        self.row = row

        self.width = width
        self.height = height

        self.tile_size = tile_size

        self.image = self.extract()


    def extract(self):

        x = self.col * self.tile_size
        y = self.row * self.tile_size

        w = self.width * self.tile_size
        h = self.height * self.tile_size

        return self.tileset.crop((
            x,
            y,
            x + w,
            y + h
        ))


    def show(self):
        self.image.show()


    def save(self, path):
        self.image.save(path)



class AssetManager:

    def __init__(self):
        self.assets = {}

    def add(self, tile):
        self.assets[tile.name] = tile

    def get(self, name):
        return self.assets[name]

    def list(self):
        return list(self.assets.keys())
