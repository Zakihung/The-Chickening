# modules/screens/main_menu.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE, COLOR_BLUE

class MainMenu:
    def __init__(self, screen):
        """
        Màn menu chính: Buttons start, options, quit.
        """
        self.screen = screen
        self.buttons = [
            {'text': 'Start', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 200, 200, 50), 'action': 'start'},
            {'text': 'Options', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 50), 'action': 'options'},
            {'text': 'Quit', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 400, 200, 50), 'action': 'quit'}
        ]
        self.font = pygame.font.SysFont(None, 40)  # Font text

    def update(self, events):
        """Handle events (mouse click). Return action if clicked."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        return button['action']
        return None

    def draw(self):
        """Draw menu background/buttons."""
        self.screen.fill(COLOR_BLACK)
        for button in self.buttons:
            pygame.draw.rect(self.screen, COLOR_BLUE, button['rect'])
            text = self.font.render(button['text'], True, COLOR_WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)