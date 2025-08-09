from Game.ui import PastelButton, PastelText, PastelTextBox
from Game.constants import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame

button_width = 150

title = {
    "background": pygame.transform.scale(pygame.image.load("Game/Assets/Background/title.png"), (1280, 720)),
    "title": PastelText(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 250, text="A Fleet Among Angles", font_size=50, center=True),
    "start": PastelButton(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2, width=button_width, height=50, text="Start"),
    "load": PastelButton(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + 100, width=button_width, height=50, text="Load"),
    "exit": PastelButton(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + 200, width=button_width, height=50, text="Exit")

} 