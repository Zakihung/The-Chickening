# modules/screens/game_over.py
import pygame
import json
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE, COLOR_RED

class GameOver:
    def __init__(self, screen, score=0):
        """
        Màn game over: Buttons restart, quit, highscore.
        """
        self.screen = screen
        self.score = score
        self.buttons = [
            {'text': 'Restart', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 200, 200, 50), 'action': 'restart'},
            {'text': 'Quit', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 50), 'action': 'quit'}
        ]
        self.font = pygame.font.SysFont(None, 40)
        self.highscores = self.load_highscores()
        self.update_highscores()

    def load_highscores(self):
        try:
            with open('highscores.json', 'r', encoding="utf8") as f:
                return json.load(f).get('highscores', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def update_highscores(self):
        self.highscores.append(self.score)
        self.highscores = sorted(self.highscores, reverse=True)[:5]  # Top 5
        with open('highscores.json', 'w') as f:
            json.dump({'highscores': self.highscores}, f)

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
        self.screen.blit(title, (SCREEN_WIDTH//2 - 100, 100))
        score_text = self.font.render(f'Score: {self.score}', True, COLOR_WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - 100, 150))
        for button in self.buttons:
            pygame.draw.rect(self.screen, COLOR_BLACK, button['rect'])
            text = self.font.render(button['text'], True, COLOR_WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        # Highscores
        hs_title = self.font.render('Highscores:', True, COLOR_WHITE)
        self.screen.blit(hs_title, (SCREEN_WIDTH//2 - 100, 400))
        for i, hs in enumerate(self.highscores):
            hs_text = self.font.render(f'{i+1}. {hs}', True, COLOR_WHITE)
            self.screen.blit(hs_text, (SCREEN_WIDTH//2 - 100, 450 + i*30))