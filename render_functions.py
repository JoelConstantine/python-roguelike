from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

import color

import pygame

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap
    from components.inventory import Inventory



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



def render_inventory(
    surface: pygame.Surface, width: int, location: Tuple[int, int], inventory: Inventory = None
) -> None:
    inventory_surface = pygame.Surface((width, 640))
    inventory_surface.fill((0,0,255))
    surface.blit(inventory_surface, location)

def render_mouse(
    surface: pygame.Surface,  filename: str = "",
) -> None:
    mouse_cursor, rect = load_image(name="mouse cursor.png", colorkey=(255,0,255), scale=2)
    mouse_pos = pygame.mouse.get_pos()
    surface.blit(mouse_cursor, mouse_pos)