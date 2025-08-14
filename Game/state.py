
from Game.screens import title
import pygame
from Game.constants import  SCREEN_WIDTH, SCREEN_HEIGHT

class State:

    def __init__(self, ui):
        self.ui = ui # All the UI components in state.
        self.is_active = False

    def draw(self, screen):

        # Cannot just use .draw because the bacground is a pygame image
        # that uses .blit not draw like the other UI components.
        if "background" in self.ui: 
            screen.blit(self.ui["background"], (0,0))

        for key, component in self.ui.items():
            if key != "background":
                component.draw(screen)


    def handle_event(self, event):
        pass

class State_Manager:

    def __init__(self):
        self.states = {
            "title": State(title),
            "battle": State({}),
        }

        self.current_state = "title"

    def switch_states(self, next_state):
        self.current_state = next_state

    
    def check_current_state(self):

        return self.current_state
    

