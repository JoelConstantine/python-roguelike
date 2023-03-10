from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING, Tuple, List

import numpy as np # type: ignore
from tcod.console import Console

import pygame

from entity import Actor, Item
import tile_types

from render_functions import load_image

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_surface import GameSurface
    

class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities =set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        ) # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False,order="F"
            ) # Tiles the player has seen before
        
        self.downstairs_location = (0,0)

    @property
    def gamemap(self) -> GameMap:
        return self



    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors"""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )
        
    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x 
                and entity.y == location_y
            ):
                return entity
            
        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map

        If a tile is in the "visible" array, then draw it with the "light" colors
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors
        Otherwise, default to "SHROUD"
        """

        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            # Only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )

    def render_window(self, screen: GameSurface) -> pygame.Surface:
        floor_tileset = screen.get_tileset("basic_floor")
        character_sprites = screen.get_tileset("characters")
        inventory_sprites = screen.get_tileset("inventory")
        floor_sprites = floor_tileset.get_tiles()
        
        scale = floor_tileset.scale
        tile_size = floor_tileset.tile_size * scale

        player_x = self.engine.player.x
        player_y = self.engine.player.y

        camera_width = 930
        camera_height = 640


        game_map = pygame.Surface((1280 * scale, 800 * scale))
        camera = pygame.Surface((camera_width,camera_height))

        window_tile_height = 30
        window_tile_width = 50

        # window_visible = visible_tiles[x-10:y-10:x+10:y+10]
        
        starting_x_index = min([0,  player_x - (window_tile_width // 2)])
        starting_y_index = min([0, player_y - (window_tile_height // 2)])
        
        black = 0, 0, 0
        game_map.fill(black)

        tile_sprites: List[Tuple[pygame.Surface, Tuple[int, int]]] = []

        with np.nditer(self.tiles, flags=["multi_index"]) as row:
            for tile in row:
                tile_x, tile_y = row.multi_index[0], row.multi_index[1]
                if self.explored[tile_x, tile_y]:
                    tile_img: pygame.Surface = floor_sprites[tile["sprite"]][0]

                    if not self.visible[tile_x, tile_y]:
                       tile_img.set_alpha(95)
                    else:
                       tile_img.set_alpha()
                    game_map.blit(tile_img, (tile_x * tile_size, tile_y * tile_size))
                    

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        entity_sprites: List[Tuple[pygame.Surface, Tuple[int, int]]] = []

        for entity in entities_sorted_for_rendering:
            # Only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                if entity.sprIdx != -1:
                    if entity.sprite_sheet == "characters":
                        img = character_sprites.get_sprite(entity.sprIdx)
                    elif entity.sprite_sheet == "inventory":
                        img = inventory_sprites.get_sprite(entity.sprIdx)
                    else:
                        img = screen.not_implemented[0]
                    entity_sprites.append((img, (entity.x * tile_size, entity.y * tile_size)))
                    # game_map.blit(img, (entity.x * tile_size, entity.y * tile_size))
        
        game_map.blits(tile_sprites)
        game_map.blits(entity_sprites)
  
        camera.fill(black)
        camera.blit(
            game_map, 
            (0,0), 
            (player_x * tile_size - camera_width // 2, player_y * tile_size - camera_height // 2, camera_width, camera_height)
        )
        return camera
        


class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down stairs
    """
    
    def __init__(
        self,
        *,
        engine: Engine,
        map_width: int,
        map_height: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        current_floor: int = 0
    ):
        self.engine = engine
        
        self.map_width = map_width
        self.map_height = map_height
        
        self.max_rooms = max_rooms
        
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        
        
        self.current_floor = current_floor
        
    def generate_floor(self) -> None:
        from procgen import generate_dungeon
        
        self.current_floor += 1
        
        self.engine.game_map = generate_dungeon(
            max_rooms = self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=self.map_width,
            map_height=self.map_height,
            engine=self.engine
        )