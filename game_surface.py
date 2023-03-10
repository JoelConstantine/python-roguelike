from typing import Dict

import os
import pygame


def load_image(name, colorkey=None, scale=1):
    image = pygame.image.load(name).convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

def load_tiles(filename: str, width: int, height: int, colorKey=None, scale: int=1):
    image, rect = load_image(filename, colorKey, scale)
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width//(width * scale)):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height//(height * scale)):
            rect = (tile_x*width*scale, tile_y*height*scale, width*scale, height*scale)
            line.append(image.subsurface(rect))
    return tile_table

class Tile():
    def __init__():
        pass

class TileSet():
    def __init__(
        self, filename: str, tile_size: int=16, scale: int = 1, colorKey=None
    ):
        self.filename = filename
        self.tile_size = tile_size
        self.scale = scale
        self.sprites = load_tiles(filename, tile_size, tile_size, colorKey, scale)

        filepath = os.path.join("images", "not implemented.png")
        self.not_implemented = load_image(filepath, scale=2)
        
    def get_tiles(self):
        return self.sprites
    
    def get_sprite(self, index):
        if index == -1:
            return self.not_implemented[0]
        try:
            sprite = self.sprites[index][0]
        except Exception:
            sprite = self.not_implemented[0]
        return  sprite

class GameSurface():
    def __init__(self, width: int, height: int, base_path: str = "images"):
        self.surface = pygame.display.set_mode((width, height), pygame.SCALED)
        self.tilesets: Dict[TileSet] = {}
        self.base_path = base_path

        filepath = os.path.join(self.base_path, "not implemented.png")
        self.not_implemented = load_image(filepath, scale=2)

    def load_tile_sheet(self, name, filepath, tile_size: int=16, scale: int=1, colorKey=None):
        filepath = os.path.join(self.base_path, filepath)
        self.tilesets[name] = TileSet(filepath, tile_size=tile_size, scale=scale, colorKey=colorKey)

    def get_tileset(self, name) -> TileSet:
        return self.tilesets[name]



