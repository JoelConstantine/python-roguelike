from typing import Tuple

import numpy as np # type: ignore

from pygame.sprite import Sprite

# Tile graphics structurede type compatible with Console.tiles_rgb
graphic_dt = np.dtype(
    [
        ("ch", np.int32), # Unicode codepoint
        ("fg", "3B"), # 3 unsigned bytes, for RGB colors
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data
tile_dt = np.dtype(
    [
        ("walkable", bool), # True if this tile can be walked over
        ("transparent", bool), # True if this tile doesn't block FOV
        ("dark", graphic_dt), # Graphics for when the tile is not in FOV
        ("light", graphic_dt),
        ("filepath", 'S30'), # Graphics for when the tile is in FOV
        ("sprite", int)
    ]
)

def new_tile(
    *, # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int],  Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    filepath: str,
    sprite: int = -1
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light, filepath, sprite), dtype=tile_dt)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255,255,255), (0,0,0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True, 
    transparent=True, 
    dark=(ord(" "), (255,255,255), (50,50,150)),
    light=(ord(" "), (255,255,255), (200,100,50)),
    filepath="ground tile.png",
    sprite=1
)

wall = new_tile(
    walkable=False, 
    transparent=False, 
    dark=(ord(" "), (255,255,255), (0,0,100)),
    light=(ord(" "), (255,255,255), (130,110,50)),
    filepath="dungeon wall.png",
    sprite=0
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50,50,150)),
    light=(ord(">"), (255,255,255), (200,180,50)),
    filepath=""
)