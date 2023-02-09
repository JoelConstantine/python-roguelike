"""All of this is based on the TCOD roguelike tutorial (2020) found at http://rogueliketutorials.com"""


import traceback

import tcod

import color
import exceptions
import input_handlers
import setup_game

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it"""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved")

def main() -> None:
    # Setup initial variables for the game
    screen_width = 80
    screen_height = 50

    # Load the provided tileset
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    # Create a new tcod tutorial with our settings and tileset, begin the gameloop
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                """
                This is the basic game engine loop
                
                First the console is cleared,
                then the engine's event_handler render its current state
                
                Afterwards, the engine then waits for and responds to player input
                before updating the loop
                """
                
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except exceptions.QuitWithoutSaving:
                    raise 
                except Exception: # Handle exceptions in game
                    traceback.print_exc() # Print erro to stderr
                    # Then print the error to the message log
                    if isinstance(handler, input_handlers.EventHandler):
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