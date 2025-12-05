# modules/screens/game_over.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE, COLOR_RED

class GameOver:
    def __init__(self, screen):
        """
        Màn game over: Buttons restart, quit.
        """
        self.screen = screen
        self.buttons = [
            {'text': 'Restart', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 200, 200, 50), 'action': 'restart'},
            {'text': 'Quit', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 50), 'action': 'quit'}
        ]
        self.font = pygame.font.SysFont(None, 40)

    def update(self, events):
        """Handle click return action."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        return button['action']
        return None

    def draw(self):
        """Draw game over."""
        self.screen.fill(COLOR_RED)
        title = self.font.render('Game Over!', True, COLOR_WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - 100, 100))  # Sửa: self.screen.blit
        for button in self.buttons:
            pygame.draw.rect(self.screen, COLOR_BLACK, button['rect'])
            text = self.font.render(button['text'], True, COLOR_WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)