from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

import color

import pygame

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap
    from components.inventory import Inventory

mouse_cursor: pygame.Surface = None

def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()

def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.bar_empty)
    
    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )

def render_dungeon_level(
    console: Console, dungeon_level: int, location: Tuple[int, int]
) -> None:
    """Render the level the player is currently on, at a given location"""
    x, y = location
    console.print(x=x, y=y,string=f"Dungeon level: {dungeon_level}")

def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)



####### PYGAME

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

## Renders
def render_healthbar(
        currentValue: int, totalValue: int, width: int, height: int, 
) -> pygame.Surface:
    hb_srf = pygame.Surface((width, 75))

    hb_rect = pygame.Rect(1,1,width-2, height-2)
    black=(0,0,0)
    off_white=(255,225,225)

    percent = currentValue / totalValue
    hb_width = (width-6) * percent

    hb_srf.fill(black)
    hb_srf.fill(off_white, hb_rect)

    hb_srf.fill(black, pygame.Rect(2,2,width-4,height-4))

    hb_srf.fill(off_white, pygame.Rect(3,3, hb_width, height-6))
    return hb_srf
   
def render_inventory(
    width: int, inventory: Inventory = None
) -> None:
    inventory_surface = pygame.Surface((width, 640))
    inventory_surface.fill((0,0,255))
    return inventory_surface

def render_mouse(
    filename: str
) -> pygame.Surface:
    global mouse_cursor
    if mouse_cursor is None:
        img, rect = load_image(name=filename, colorkey=(255,0,255), scale=2)
        mouse_cursor = img
    return mouse_cursor