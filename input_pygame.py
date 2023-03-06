from __future__ import annotations

import os

from typing import Any, Callable, Optional, Tuple, TypeVar, TYPE_CHECKING, Union

import tcod

import pygame

import actions
from actions import (
    Action, 
    BumpAction, 
    PickupAction,
    WaitAction
)

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item

T = TypeVar("T")

MOVE_KEYS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_HOME: (-1, -1),
    pygame.K_END: (-1, 1),
    pygame.K_PAGEUP: (1, -1),
    pygame.K_PAGEDOWN: (1,1)
}

WAIT_KEYS = {
    pygame.K_PERIOD,
    pygame.K_KP_5,
    pygame.K_CLEAR
}


class BaseEventHandler():
    def handle_events(self, event: pygame.event.Event) -> BaseEventHandler:
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions"
        return self

    def dispatch(self, event: pygame.event.Event) -> Optional[T]:
        if event.type is None:
            return None

        match event.type:
            case pygame.KEYDOWN:
                return self.ev_keydown(event)

    def ev_keydown(self, event: pygame.event.Event) -> Optional[T]:
        """Called when keyboard is pressed down"""        

    def ev_quit(self, event: pygame.event.Event) -> Optional[T]:
        """Called when quit event is called"""

    def ev_mousemotion(self, event: pygame.event.Event) -> Optional[T]:
        """Called when the mouse is moved"""

    def on_render(self, surface: pygame.Surface) -> None:
        raise NotImplementedError()
    
class ActionInputHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle events for input handlers with an engine"""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # A valid action was performed
            # if not self.engine.player.is_alive:
            #     # The player was killed sometime during or after the action
            #     return GameOverEventHandler(self.engine)
            # elif self.engine.player.level.requires_level_up:
            #     return LevelUpEventHandler(self.engine)
            return MainGameHandler(self.engine)
        return self
    
    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods
        
        Returns True if the action will advance a turn
        """

        if action is None:
            return False
        
        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False # Skip enemy turns on exceptions

        self.engine.handle_enemy_turns()
        self.engine.update_fov()
        return True
    
    def on_render(self, surface: pygame.Surface) -> None:
        self.engine.render_pygame(surface)

class MainGameHandler(ActionInputHandler):
    def ev_keydown(self, event: pygame.event) -> Optional[ActionOrHandler]:
        action: Optional[Action] = None

        key = event.key
        modifier = event.mod
        
        
        player = self.engine.player

        if key == pygame.K_PERIOD and modifier & (
             tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT
        ):
            return actions.TakeStairsAction(player)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == pygame.K_ESCAPE:
            raise SystemExit()
        # elif key == tcod.event.K_v:
        #     return HistoryViewer(self.engine)
        elif key == pygame.K_g:
             action = PickupAction(player)
            
        # elif key == tcod.event.K_i:
        #     return InventoryActivateHandler(self.engine)
        # elif key == tcod.event.K_d:
        #     return InventoryDropHandler(self.engine)
        # elif key == tcod.event.K_c:
        #     return CharacterScreenEventHandler(self.engine)   
            
        # elif key == tcod.event.K_SLASH:
        #     return LookHandler(self.engine)

        return action
    
    