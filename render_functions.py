from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import color

import pygame
from game_surface import load_image, load_tiles


if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap
    from components.inventory import Inventory
    from game_surface import TileSet

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
    width: int, inventory: Inventory, tile_set: TileSet,
) -> None:
    grid_size: Tuple[int, int] = (4,8)
    
    grid_rect = pygame.Rect((1, 1, 31, 31))

    inventory_surface = pygame.Surface((width, 640))
    inventory_surface.fill((0,0,255))

    grid_boxes: List[Tuple[pygame.Surface, Tuple[int,int]]] = []

    inventory_grid = pygame.Surface((grid_size[0] * 32, grid_size[1] * 32))

    gutter_size = 5

    grid_box = pygame.Surface((32,32))

    item_boxes: List[Tuple[pygame.Surface, Tuple[int,int]]] = []

    grid_box.fill((0,0,0))
    pygame.draw.rect(grid_box, (255,255,255), grid_rect, width=1)

    inventory_index = 0

    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            grid_boxes.append((grid_box, (x * 32 , y * 32)))
            if inventory_index < len(inventory.items):
                item = inventory.items[inventory_index]
                item_img = tile_set.get_sprite(item.sprIdx)
                item_boxes.append((item_img, (x * 32, y * 32)))
                inventory_index += 1

    inventory_grid.blits(grid_boxes)
    inventory_grid.blits(item_boxes)
    inventory_surface.blit(inventory_grid, (50,50))        

    #for idx, item in enumerate(inventory.items):
    #   item_img = tile_set.get_sprite(item.sprIdx)
    # pygame.draw.rect(inventory_surface, (255,255,255), grid_rect, width=1)

    return inventory_surface

def render_mouse(
    filename: str
) -> pygame.Surface:
    global mouse_cursor
    if mouse_cursor is None:
        img, rect = load_image(name=filename, colorkey=(255,0,255), scale=2)
        mouse_cursor = img
    return mouse_cursor