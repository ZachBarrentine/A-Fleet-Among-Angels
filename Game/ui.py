import pygame
import pygame.font
from typing import Callable, Optional

# Initialize pygame font system
pygame.font.init()

class PastelColors:
    """Color palette matching the sci-fi pastel aesthetic"""
    # Base colors from the artwork
    LIGHT_LAVENDER = (230, 220, 240)
    MEDIUM_LAVENDER = (200, 180, 220)
    DARK_LAVENDER = (150, 130, 180)
    DEEP_PURPLE = (120, 80, 140)
    SOFT_WHITE = (245, 240, 250)
    
    # Interactive states
    HOVER_GLOW = (180, 160, 200)
    ACTIVE_GLOW = (160, 140, 190)
    TEXT_DARK = (80, 60, 100)
    TEXT_LIGHT = (240, 235, 245)
    
    # Special effects
    BORDER_LIGHT = (210, 190, 230)
    SHADOW = (140, 120, 160, 100)  # With alpha

class PastelButton:
    """A button with pastel styling and hover effects"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 font_size: int = 24, callback: Optional[Callable] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, font_size)
        
        # State management
        self.is_hovered = False
        self.is_pressed = False
        self.hover_animation = 0.0  # 0.0 to 1.0 for smooth transitions
        
        # Style properties
        self.corner_radius = 12
        self.border_width = 2
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events. Returns True if button was clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.rect.collidepoint(event.pos) and self.callback:
                    self.callback()
                    return True
        
        elif event.type == pygame.MOUSEMOTION:
            was_hovered = self.is_hovered
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        return False
    
    def update(self, dt: float):
        """Update hover animation"""
        target = 1.0 if self.is_hovered else 0.0
        self.hover_animation += (target - self.hover_animation) * min(dt * 8, 1.0)
    
    def draw(self, surface: pygame.Surface):
        """Draw the button with hover effects"""
        # Calculate colors based on state
        base_color = PastelColors.MEDIUM_LAVENDER
        hover_blend = self.hover_animation
        
        if self.is_pressed:
            bg_color = PastelColors.DARK_LAVENDER
            border_color = PastelColors.DEEP_PURPLE
        else:
            # Blend between base and hover colors
            bg_color = tuple(
                int(base_color[i] + (PastelColors.HOVER_GLOW[i] - base_color[i]) * hover_blend)
                for i in range(3)
            )
            border_color = PastelColors.BORDER_LIGHT
        
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, PastelColors.SHADOW, 
                        (0, 0, shadow_rect.width, shadow_rect.height), 
                        border_radius=self.corner_radius)
        surface.blit(shadow_surface, shadow_rect)
        
        # Draw main button
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=self.corner_radius)
        pygame.draw.rect(surface, border_color, self.rect, 
                        width=self.border_width, border_radius=self.corner_radius)
        
        # Add inner glow effect when hovered
        if hover_blend > 0:
            glow_rect = self.rect.inflate(-4, -4)
            glow_alpha = int(30 * hover_blend)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*PastelColors.SOFT_WHITE, glow_alpha), 
                           (0, 0, glow_rect.width, glow_rect.height), 
                           border_radius=self.corner_radius-2)
            surface.blit(glow_surface, glow_rect)
        
        # Draw text
        text_color = PastelColors.TEXT_DARK
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class PastelTextBox:
    """A text input box with pastel styling"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 font_size: int = 24, placeholder: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.placeholder = placeholder
        
        # Text properties
        self.text = ""
        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_timer = 0
        
        # State management
        self.is_focused = False
        self.is_hovered = False
        self.focus_animation = 0.0
        
        # Style properties
        self.corner_radius = 8
        self.padding = 12
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events. Returns True if text changed."""
        text_changed = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                was_focused = self.is_focused
                self.is_focused = self.rect.collidepoint(event.pos)
                if self.is_focused and not was_focused:
                    self.cursor_pos = len(self.text)
        
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.KEYDOWN and self.is_focused:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    text_changed = True
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                    text_changed = True
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
            elif event.unicode and event.unicode.isprintable():
                self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                self.cursor_pos += 1
                text_changed = True
        
        return text_changed
    
    def update(self, dt: float):
        """Update animations and cursor blinking"""
        # Focus animation
        target = 1.0 if self.is_focused else 0.0
        self.focus_animation += (target - self.focus_animation) * min(dt * 6, 1.0)
        
        # Cursor blinking
        if self.is_focused:
            self.cursor_timer += dt
            self.cursor_visible = (self.cursor_timer % 1.0) < 0.5
    
    def draw(self, surface: pygame.Surface):
        """Draw the text box"""
        # Background color based on state
        if self.is_focused:
            bg_color = PastelColors.SOFT_WHITE
            border_color = PastelColors.DEEP_PURPLE
            border_width = 2
        else:
            bg_color = PastelColors.LIGHT_LAVENDER
            border_color = PastelColors.HOVER_GLOW if self.is_hovered else PastelColors.BORDER_LIGHT
            border_width = 1
        
        # Draw background
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=self.corner_radius)
        pygame.draw.rect(surface, border_color, self.rect, 
                        width=border_width, border_radius=self.corner_radius)
        
        # Add focus glow
        if self.focus_animation > 0:
            glow_rect = self.rect.inflate(4, 4)
            glow_alpha = int(20 * self.focus_animation)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*PastelColors.DEEP_PURPLE, glow_alpha), 
                           (0, 0, glow_rect.width, glow_rect.height), 
                           border_radius=self.corner_radius+2)
            surface.blit(glow_surface, glow_rect)
        
        # Prepare text rendering area
        text_rect = pygame.Rect(self.rect.x + self.padding, self.rect.y, 
                               self.rect.width - 2*self.padding, self.rect.height)
        
        # Draw text or placeholder
        display_text = self.text if self.text else self.placeholder
        text_color = PastelColors.TEXT_DARK if self.text else PastelColors.DARK_LAVENDER
        
        if display_text:
            text_surface = self.font.render(display_text, True, text_color)
            text_y = self.rect.centery - text_surface.get_height() // 2
            
            # Clip text to fit in box
            clip_rect = pygame.Rect(text_rect.x, text_y, text_rect.width, text_surface.get_height())
            surface.set_clip(clip_rect)
            surface.blit(text_surface, (text_rect.x, text_y))
            surface.set_clip(None)
        
        # Draw cursor
        if self.is_focused and self.cursor_visible and self.text:
            cursor_text = self.text[:self.cursor_pos]
            cursor_width = self.font.size(cursor_text)[0] if cursor_text else 0
            cursor_x = text_rect.x + cursor_width
            cursor_y1 = self.rect.y + 6
            cursor_y2 = self.rect.y + self.rect.height - 6
            pygame.draw.line(surface, PastelColors.DEEP_PURPLE, 
                           (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

class PastelText:
    """Static text with pastel styling options"""
    
    def __init__(self, x: int, y: int, text: str, font_size: int = 24, 
                 color: tuple = PastelColors.TEXT_DARK, center: bool = False):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.center = center
        
        # Animation properties
        self.fade_animation = 1.0
        self.glow_animation = 0.0
        
        # Cache text dimensions
        self._update_dimensions()
    
    @property
    def width(self) -> int:
        """Get the width of the rendered text"""
        return self._text_width
    
    @property
    def height(self) -> int:
        """Get the height of the rendered text"""
        return self._text_height
    
    @property 
    def size(self) -> tuple:
        """Get the (width, height) of the rendered text"""
        return (self._text_width, self._text_height)
    
    def _update_dimensions(self):
        """Update cached text dimensions"""
        if self.text:
            self._text_width, self._text_height = self.font.size(self.text)
        else:
            self._text_width, self._text_height = 0, self.font.get_height()
        
    def set_text(self, text: str):
        """Update the text content"""
        self.text = text
        self._update_dimensions()  # Update dimensions when text changes
    
    def set_glow(self, intensity: float):
        """Set glow effect intensity (0.0 to 1.0)"""
        self.glow_animation = max(0.0, min(1.0, intensity))
    
    def fade_in(self, dt: float, speed: float = 4.0):
        """Animate fade in effect"""
        self.fade_animation = min(1.0, self.fade_animation + dt * speed)
    
    def fade_out(self, dt: float, speed: float = 4.0):
        """Animate fade out effect"""
        self.fade_animation = max(0.0, self.fade_animation - dt * speed)
    
    def draw(self, surface: pygame.Surface):
        """Draw the text with effects"""
        if self.fade_animation <= 0:
            return
            
        # Create text surface
        alpha = int(255 * self.fade_animation)
        text_color = (*self.color[:3], alpha) if len(self.color) == 4 else (*self.color, alpha)
        
        text_surface = self.font.render(self.text, True, text_color[:3])
        if alpha < 255:
            text_surface.set_alpha(alpha)
        
        # Calculate position
        if self.center:
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            pos = text_rect.topleft
        else:
            pos = (self.x, self.y)
        
        # Draw glow effect
        if self.glow_animation > 0:
            glow_surface = text_surface.copy()
            glow_alpha = int(100 * self.glow_animation * self.fade_animation)
            glow_surface.set_alpha(glow_alpha)
            
            # Draw glow in multiple positions for blur effect
            for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
                glow_pos = (pos[0] + offset[0], pos[1] + offset[1])
                surface.blit(glow_surface, glow_pos)
        
        # Draw main text
        surface.blit(text_surface, pos)

# Example usage and demo
def create_demo():
    """Creates a demo showing all UI components"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pastel Sci-Fi UI Demo")
    clock = pygame.time.Clock()
    
    # Create UI components
    button1 = PastelButton(50, 100, 200, 50, "Launch Sequence", callback=lambda: print("Launch initiated!"))
    button2 = PastelButton(300, 100, 150, 50, "Settings")
    
    textbox = PastelTextBox(50, 200, 300, 40, placeholder="Enter coordinates...")
    
    title = PastelText(400, 50, "STARSHIP CONTROL", 36, PastelColors.DEEP_PURPLE, center=True)
    status = PastelText(50, 300, "System Status: Ready", 20, PastelColors.TEXT_DARK)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle UI events
            button1.handle_event(event)
            button2.handle_event(event)
            if textbox.handle_event(event):
                status.set_text(f"Input: {textbox.text}")
        
        # Update components
        button1.update(dt)
        button2.update(dt)
        textbox.update(dt)
        title.set_glow(0.3)  # Constant subtle glow
        
        # Draw everything
        screen.fill(PastelColors.LIGHT_LAVENDER)
        
        button1.draw(screen)
        button2.draw(screen)
        textbox.draw(screen)
        title.draw(screen)
        status.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    create_demo()