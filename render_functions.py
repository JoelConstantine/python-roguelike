from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING, Optional

import color

import pygame
from game_surface import load_image, load_tiles


if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap
    from components.inventory import Inventory
    from game_surface import TileSet
    from entity import Item

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
    surface: pygame.Surface, location: Tuple[int, int], width: int, inventory: Inventory, tile_set: TileSet,
) -> Optional[Tuple[List[pygame.Rect,Item]]]:
    item_size = 64

    grid_size: Tuple[int, int] = (4,8)
    grid_rect = pygame.Rect((0, 0, item_size + 2, item_size + 2))

    location_x, location_y = location
    grid_boxes: List[Tuple[pygame.Surface, Tuple[int,int]]] = []

    gutter_size = 5

    grid_box = pygame.Surface((item_size + 2,item_size + 2))

    item_boxes: List[Tuple[pygame.Surface, Tuple[int,int]]] = []

    grid_box.fill((0,0,0))
    pygame.draw.rect(grid_box, (255,255,255), grid_rect, width=1)

    inventory_index = 0

    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            if inventory_index < len(inventory.items):
                item = inventory.items[inventory_index]
                item_img = tile_set.get_sprite(item.sprIdx)
                item_boxes.append((item_img, (gutter_size * x + location_x + x * item_size + 2 + 1,gutter_size * y + location_y + y * item_size + 2 + 1)))
                inventory_index += 1
            grid_boxes.append((grid_box, (gutter_size * x + location_x + x * item_size + 2,gutter_size* y + location_y + y * item_size + 2)))
            
    
    surface.blits(grid_boxes)
   
    inventory_rects =surface.blits(item_boxes)
    inventory_slots = list(zip(inventory_rects, inventory.items))
    return inventory_slots

def render_mouse(
    filename: str
) -> pygame.Surface:
    global mouse_cursor
    if mouse_cursor is None:
        img, rect = load_image(name=filename, colorkey=(255,0,255), scale=2)
        mouse_cursor = img
    return mouse_cursor

def render_box_at_mouse(
    surface: pygame.Surface,
    locations: List[Tuple[pygame.Rect, Item]],
    engine: Engine
) -> None:
    mouse_x, mouse_y =  pygame.mouse.get_pos()

    if (mouse_x < 0 or mouse_y < 0 or mouse_x > surface.get_width() or mouse_y > surface.get_height()):
        return
    
    for location in locations:
        rect = location[0]
        item = location[1]
        if rect.left <= mouse_x <= rect.right and rect.top <= mouse_y <= rect.bottom:
            print(f"Item: {item.name}")