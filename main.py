"""All of this is based on the TCOD roguelike tutorial (2020) found at http://rogueliketutorials.com"""


import copy
import traceback

import tcod

import color
from engine import Engine
import entity_factories
from procgen import generate_dungeon

def main():
    # Setup initial variables for the game
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 2
    max_items_per_room = 2

    # Load the provided tileset
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # Create the player
    player = copy.deepcopy(entity_factories.player)

    # Initialize the engine, passing in the player
    engine = Engine(player=player)

    # Create the dungeon map for the engine
    engine.game_map = generate_dungeon(
        max_rooms=max_rooms, 
        room_min_size=room_min_size, 
        room_max_size=room_max_size, 
        map_width=map_width, 
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        max_items_per_room=max_items_per_room,
        engine=engine
    )

    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    # Create a new tcod tutorial with our settings and tileset, begin the gameloop
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            """
            This is the basic game engine loop
            
            First the console is cleared,
            then the engine's event_handler render its current state
            
            Afterwards, the engine then waits for and responds to player input
            before updating the loop
            """
            
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)

            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception: # Handle exceptions in game
                traceback.print_exc() # Print erro to stderr
                # The print the error to the message log
                engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == "__main__":
    main()