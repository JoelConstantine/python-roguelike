from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov


import pygame



import exceptions
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld
    from game_surface import GameSurface


class Engine:
    game_map: GameMap
    game_world: GameWorld
    
    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass # Ignore impossible actions from AI

    def update_fov(self) -> None:
        """Recompute the visible area based ont he players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )

        # If a tile is "visible" it should be added to "explored"
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20
        )

        render_functions.render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
        
        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0,47)
        )
        
    def render_pygame(self, screen: GameSurface) -> None:
        camera = self.game_map.render_window(screen)
        

        inventory_locations = render_functions.render_inventory(
            surface=screen.surface,
            location=(screen.surface.get_width() - 350, 150),
            width=350, 
            inventory=self.player.inventory,
            tile_set=screen.get_tileset("inventory")
        )

        render_functions.render_box_at_mouse(
            surface=screen.surface,
            locations=inventory_locations,
            engine=self
        )

        health_bar = render_functions.render_healthbar(
            currentValue=self.player.fighter.hp,
            totalValue=self.player.fighter.max_hp,
            width=250,
            height=35,
        )
        
        mouse_cursor = render_functions.render_mouse(filename="mouse cursor.png")

        screen.surface.blits([
            (camera, (0,0)),
            (health_bar, (3,643)),
            (mouse_cursor, pygame.mouse.get_pos())
        ])        

    def save_as(self, filename: str) -> None:
        """Save this engine instance as a compressed file"""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
