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
        ("name", 'U15'),
        ("sprite", int),

    ]
)

def new_tile(
    *, # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    name: str,
    sprite: int = -1,
    
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, name, sprite), dtype=tile_dt)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255,255,255), (0,0,0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True, 
    transparent=True, 
    name="floor",
    sprite=1,
)

wall = new_tile(
    walkable=False, 
    transparent=False, 

    name="wall",
    sprite=0,
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    name=""
)