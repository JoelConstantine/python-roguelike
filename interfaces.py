from __future__ import annotations

from typing import Tuple

class Interface(): 
    def __init__(
        self,
        location: Tuple[int, int]
    ):
        self.location = location
    
    def on_render():
        """Call when rendering"""


class InventoryInterface(Interface):
    def __init__(
        self,
        location: Tuple[int, int],
        grid_size: Tuple[int, int]
    ):
        super.__init__(location)
        self.grid_size = grid_size