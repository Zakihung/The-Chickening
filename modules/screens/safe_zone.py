import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE, COLOR_BLUE

class SafeZone:
    def __init__(self, screen, player):
        """
        Chuồng Gà - Safe Zone: Shop, skills, missions.
        """
        self.screen = screen
        self.player = player
        self.buttons = [
            {'text': 'Store Thóc', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 100, 200, 50), 'action': 'store'},
            {'text': 'Shop', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 200, 200, 50), 'action': 'shop'},
            {'text': 'Skills Upgrade', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 50), 'action': 'skills'},
            {'text': 'Missions', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 400, 200, 50), 'action': 'missions'},
            {'text': 'Back', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 500, 200, 50), 'action': 'back'}
        ]
        self.font = pygame.font.SysFont(None, 40)

    def update(self, events):
        """Handle click return action."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        if button['action'] == 'store':
                            self.player.store_thoc()
                        elif button['action'] == 'shop':
                            print("Shop placeholder")  # Open shop UI later
                        elif button['action'] == 'skills':
                            print("Skills upgrade placeholder")  # Call skills.upgrade
                        elif button['action'] == 'missions':
                            print("Missions board placeholder")  # Tasks for thóc
                        return button['action']
        return None

    def draw(self):
        """Draw safe zone."""
        self.screen.fill(COLOR_BLUE)
        for button in self.buttons:
            pygame.draw.rect(self.screen, COLOR_BLACK, button['rect'])
            text = self.font.render(button['text'], True, COLOR_WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)