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

def load_tiles(filename: str, width: int, height: int):
    image, rect = load_image(filename, scale=2)
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width//width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height//height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table


class GameSurface():
    def __init__(self, width: int, height: int):
        self.surface = pygame.display.set_mode((width, height), pygame.SCALED)
        self.tilesets = {}

    def load_character_sheet(self, filename):
        self.character_sprites = TileSet(filename)
        pass

    def load_world_tiles(self, filename)
        self.world_tiles = TileSet(filename)

    def load_tile_sheet(self, filename):
        self.tilesets[filename] = TileSet(filename)



class TileSet():
    def __init__(self, filename: str):
        self.sprites = load_tiles(filename, 32, 32)

    def get_tiles(self):
        return self.sprites

class Tile():
    def __init__():
        pass
