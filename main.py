"""All of this is based on the TCOD roguelike tutorial (2020) found at http://rogueliketutorials.com"""

from typing import Dict, Tuple

import traceback

import os, pygame

import color
import exceptions

import setup_game

import event_handlers.base_event_handler

from game_surface import GameSurface

def save_game(handler: event_handlers.base_event_handler.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it"""
    if isinstance(handler, event_handlers.base_event_handler.ActionInputHandler):
        handler.engine.save_as(filename)
        print("Game saved")



def main() -> None:
    pygame.init()
    #screen = pygame.display.set_mode((1280,800), pygame.SCALED)
   # pygame.display.set_caption("TESTING")

    # Setup initial variables for the game
    screen_width = 80
    screen_height = 50

    # tiles x = 40, y = 30

    screen = GameSurface(
        width=1280,
        height=800,
        base_path="images"
    )

    first_floor_tiles: Dict[str, Tuple[int,int,int,int]] = {
        "wall_se": (0,0,32,32),
        "wall_s": (32,0,32,32),
        "wall_sw": (64,0,32,32),
        "wall_nw_c": (96,0,32,32),
        "wall_ne_c": (128,0,32,32), 

        "wall_n": (32,64,32,32),
        
        "wall_e": (0,32,32,32),
        "wall_w": (64,32,32,32),
        
        
        "wall_sw_c": (96,32,32,32),
        "wall_se_c": (128,32,32,32),
        "wall_ne": (64,64,32,32),
        "wall_nw": (0,64,32,32),
        
        "floor": (32,32,32,32),
    }

    character_sheet: Dict[str, Tuple[int,int,int,int]] = {
        "player": (0,0,32,32),
        "tombstone": (32,0,32,32),
        "wretched": (64,0,32,32)
    }

    screen.load_defined_tile_sheet(
        name="character_sheet",
        filepath="dc character sheet.png",
        tiles=character_sheet,
        colorKey=-1,
        scale=2
    )

    screen.load_defined_tile_sheet(
        name="first_floor_sheet",
        filepath="floor_01_sheet.png",
        tiles=first_floor_tiles,
        scale=2
    )

    screen.load_tile_sheet(
        name="characters", 
        filepath="character sprite sheet.png", 
        tile_size=16, 
        scale=4,
        colorKey=-1
        )
    screen.load_tile_sheet(
        name="inventory",
        filepath="items sheet.png",
        tile_size=16,
        scale=4,
        colorKey=-1
    )
    
    handler: event_handlers.base_event_handler = setup_game.MainMenu()

    # screen = pygame.display.set_mode((1280,800), pygame.SCALED)
    pygame.display.set_caption("DATA CRAWLERS")
    pygame.mouse.set_visible(False)
    try:
        while True:
            """
            This is the basic game engine loop
            
            First the console is cleared,
            then the engine's event_handler render its current state
            
            Afterwards, the engine then waits for and responds to player input
            before updating the loop
            """
            screen.surface.fill((0,0,0))
            handler.on_render(screen)
            pygame.display.flip()

            try:
                for event in pygame.event.get():
                    handler = handler.handle_events(event)
            except exceptions.QuitWithoutSaving:
                raise 
            except Exception: # Handle exceptions in game
                traceback.print_exc() # Print erro to stderr
                # Then print the error to the message log
                if isinstance(handler, event_handlers.base_event_handler.ActionInputHandler):
                    handler.engine.message_log.add_message(traceback.format_exc(), color.error)

    except exceptions.QuitWithoutSaving:
        print("System exit")
        raise 
    except SystemExit: # Save and quit
        save_game(handler, "savegame.sav")
        raise 
    except BaseException:
        save_game(handler, "savegame.sav")
        raise 

    pygame.quit()

if __name__ == "__main__":
    main()