from typing import Dict, List, Tuple, Union

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

def load_tiles(filename: str, width: int, height: int, colorKey=None, scale: int=1) -> List[pygame.Surface]: 
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

def load_defined_tiles(
    filename: str, tiles: Dict[str, Tuple[int, int, int, int]], colorKey=None, scale: int=1
    ) -> Dict[str, pygame.Surface]:
        image, rect = load_image(filename, colorKey, scale)
        tile_dict: Dict[str, pygame.Surface] = {}
        for key, value  in tiles.items():
            scaled_value = (value[0] * scale, value[1] * scale, value[2] * scale, value[3] * scale)
            tile_dict[key] = image.subsurface(scaled_value)
            
        return tile_dict

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

class DefinedTileSet(TileSet):
    def __init__(
        self, filename: str, tiles: Dict[str, Tuple[int, int, int, int]], scale: int = 1, colorKey=None
    ):
        self.filename = filename
        self.tiles = tiles
        self.scale = scale
        self.sprites = load_defined_tiles(
            filename=filename, tiles=tiles,  colorKey=colorKey, scale=scale)
        
        filepath = os.path.join("images", "not implemented.png")
        self.not_implemented = load_image(filepath, scale=2)
        
    def get_sprite(self, name: str) -> pygame.Surface:
        if not name:
            return self.not_implemented[0]
        return self.sprites[name]

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
        
    def load_defined_tile_sheet(self, name: str, filepath: str, tiles: Dict[str, Tuple[int,int,int,int]], scale: int=1, colorKey=None):
        filepath = os.path.join(self.base_path, filepath)
        self.tilesets[name] = DefinedTileSet(filepath, tiles=tiles, scale=scale, colorKey=colorKey)

    def get_tileset(self, name) -> Union[TileSet, DefinedTileSet]:
        return self.tilesets[name]

    def get_sprite_from_tilesheet(self, tilesheet: str, name: str) -> pygame.Surface:
        if not tilesheet or not name:
            return self.not_implemented[0]
        try:
            sprite = self.get_tileset(tilesheet).get_sprite(name)
        except Exception:
            sprite = self.not_implemented[0]
        return sprite