"""All of this is based on the TCOD roguelike tutorial (2020) found at http://rogueliketutorials.com"""


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

    screen.load_tile_sheet(
        name="characters", 
        filepath="character sprite sheet.png", 
        tile_size=16, 
        scale=2
        )
    screen.load_tile_sheet(
        name="basic_floor", 
        filepath="basic tilesheet.png", 
        tile_size=16, 
        scale=2)
    screen.load_tile_sheet(
        name="inventory",
        filepath="items sheet.png",
        tile_size=16,
        scale=2
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

if __name__ == "__main__":
    main()