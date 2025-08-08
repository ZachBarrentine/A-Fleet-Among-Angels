import pygame
from Game.unit import Unit
from Game.grid import Grid

from Game.constants import GridState


class FireEmblemGame:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Fire Emblem like game")
        
        self.clock = pygame.time.Clock()

        self.tilemap = type('Tilemap', (), {
            'tilemap': {},  # Would contain your actual tilemap data
            'tile_size': 16
        })()

        self.grid = Grid(self.tilemap, tile_size=64)

        self.setup_test_units()

        self.camera_offset = [0,0]
        

        self.camera_speed = 5

    def setup_test_units(self):

        player1 = Unit("Hero", (5, 5), movement_range=3, team="player", attack_range=1, sprite_path="Game/Assets/Unit/test.png")
        player2 = Unit("Mage", (6,5), movement_range=2, team="player", attack_range=2, sprite_path="Game/Assets/Unit/test2.png")

        enemy1 = Unit("Orc", (10,8), movement_range=2, team="enemy", attack_range=1, sprite_path="Game/Assets/Unit/test3.png")
        enemy2 = Unit("Goblin", (12, 9), movement_range=4, team="enemy", attack_range=1, sprite_path="Game/Assets/Unit/test4.png")

        self.grid.add_unit(player1)
        self.grid.add_unit(player2)

        self.grid.add_unit(enemy1)
        self.grid.add_unit(enemy2)

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    grid_pos = self.grid.world_to_grid(mouse_pos, tuple(self.camera_offset))

                    self.grid.handle_click(grid_pos=grid_pos, mouse_pos=mouse_pos)

            elif event.type == pygame.MOUSEMOTION:

                mouse_pos = pygame.mouse.get_pos()
                self.grid.update_hover(mouse_pos=mouse_pos)
                

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    if self.grid.current_phase == "player":
                        self.grid.start_new_turn("enemy")
                        print(f"Switched to enemy phase")
                    
                    elif self.grid.current_phase == "enemy":
                        self.grid.start_new_turn("player")
                        print(f"Switched to player")


                elif event.key == pygame.K_ESCAPE:


                    if self.grid.state == GridState.TARGETING:
                        self.grid.state = GridState.DECISION
                        self.grid.valid_attack_targets = set()


                    elif self.grid.state == GridState.DECISION:
                        self.grid.state = GridState.UNIT_SELECT

                   
                    elif self.grid.state == GridState.UNIT_SELECT:

                        self.grid.state = GridState.IDLE

                        if self.grid.history:

                            print(f"The length of grid history is {len(self.grid.history)}")
                            original_pos = self.grid.history.pop()
                            current_pos = self.grid.selected_unit.grid_pos
                            
                            self.grid.selected_unit.grid_pos = original_pos

                            del self.grid.unit_positions[current_pos]

                            self.grid.unit_positions[original_pos] = self.grid.selected_unit

                            print(f"Undid move")
                        
                        self.grid.deselect_unit(undo=True)

                    # else:
                    #     self.grid.deselect_unit()
                        

        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.camera_offset[0] -= self.camera_speed

        if keys[pygame.K_RIGHT]:
            self.camera_offset[0] += self.camera_speed

        if keys[pygame.K_UP]:
            self.camera_offset[1] -= self.camera_speed
        
        if keys[pygame.K_DOWN]:
            self.camera_offset[1] += self.camera_speed
        
        return True
    

    def render(self):

        self.screen.fill((50, 50, 50))

        # Render tilemap here
        # self.tilemap.render(self.screen, offset=self.camera_offset)

        self.grid.render(self.screen, tuple(self.camera_offset))

        self.render_ui()

        # Update screen.
        pygame.display.flip()

    def render_ui(self):

        font = pygame.font.Font(None, 36)

        instruction = [
            "Click unit to select",
            "Click highlighted tile to move",
            "SPACE: New turn",
            "ESC: Deselect",
            "Arrows: Move camera"
        ]

        for i, instruction in enumerate(instruction):
            text = font.render(instruction, True, (255, 255, 255))
            
            # Blitting the instructions under each other through each iteration
            self.screen.blit(text, (10, 10 + i * 30))


        state_text =f"State: {self.grid.state.value}"

        if self.grid.selected_unit:
            state_text += f" - {self.grid.selected_unit.name}"

        text = font.render(state_text, True, (255, 255, 0))
        self.screen.blit(text, (10, 200))

    def run(self):

        running = True
        while running:
            running = self.handle_input()

            # Where to implement enemy AI.
            # if self.grid.current_phase == "enemy":


            self.render()
            self.clock.tick(60)

        pygame.quit()

        

if __name__ == "__main__":
    game = FireEmblemGame()
    game.run()

            

