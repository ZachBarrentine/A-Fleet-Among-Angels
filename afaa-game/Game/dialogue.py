import pygame
import pygame.font
from typing import Optional, List, Tuple

class DialogueBox:
    def __init__(
        self,
        rect: pygame.Rect,
        font: pygame.font.Font,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        box_color: Tuple[int, int, int] = (0, 0, 0),
        border_color: Tuple[int, int, int] = (255, 255, 255),
        border_width: int = 2,
    ):
        self.rect = rect
        self.font = font
        self.text_color = text_color
        self.box_color = box_color
        self.border_color = border_color
        self.border_width = border_width

        self.dialogues: List[Tuple[str, Optional[pygame.Surface]]] = []
        self.current_index: int = 0

    def add_dialogue(self, text: str, avatar: Optional[pygame.Surface] = None):
        self.dialogues.append((text, avatar))

    def next(self):
        if self.current_index < len(self.dialogues) - 1:
            self.current_index += 1

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.box_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        if not self.dialogues:
            return

        text, avatar = self.dialogues[self.current_index]

        # Sprites will go here eventually
        avatar_space = 0
        if avatar:
            avatar_rect = avatar.get_rect()
            avatar_rect.topleft = (self.rect.x + 10, self.rect.y + 10)
            surface.blit(avatar, avatar_rect)
            avatar_space = avatar_rect.width + 15

        # Should render and draw text
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_surface = self.font.render(test_line, True, self.text_color)
            if test_surface.get_width() <= self.rect.width - 20 - avatar_space:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        y_offset = self.rect.y + 10
        for line in lines:
            line_surface = self.font.render(line, True, self.text_color)
            surface.blit(line_surface, (self.rect.x + 10 + avatar_space, y_offset))
            y_offset += line_surface.get_height() + 5