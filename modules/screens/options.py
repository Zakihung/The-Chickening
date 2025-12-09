import pygame

from modules.utils.constants import SCREEN_WIDTH, COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_BLUE


class Options:
    def __init__(self, screen, sound_manager):
        """
        Options screen: Vol sliders music/sfx, back.
        """
        self.screen = screen
        self.sound_manager = sound_manager
        self.buttons = [
            {'text': 'Back', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 500, 200, 50), 'action': 'back'}
        ]
        self.font = pygame.font.SysFont(None, 40)
        self.music_slider = pygame.Rect(SCREEN_WIDTH//2 - 100, 200, 200, 20)  # Placeholder slider
        self.sfx_slider = pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 20)
        self.dragging_music = False
        self.dragging_sfx = False

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.music_slider.collidepoint(mouse_pos):
                    self.dragging_music = True
                if self.sfx_slider.collidepoint(mouse_pos):
                    self.dragging_sfx = True
                for button in self.buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        return button['action']
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging_music = False
                self.dragging_sfx = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_music:
                    x = min(max(event.pos[0], self.music_slider.x), self.music_slider.x + self.music_slider.width)
                    vol = (x - self.music_slider.x) / self.music_slider.width
                    self.sound_manager.music_volume = vol
                    self.sound_manager.play_music('music_wave.mp3', vol)  # Update
                if self.dragging_sfx:
                    x = min(max(event.pos[0], self.sfx_slider.x), self.sfx_slider.x + self.sfx_slider.width)
                    vol = (x - self.sfx_slider.x) / self.sfx_slider.width
                    self.sound_manager.sfx_volume = vol

        return None

    def draw(self):
        self.screen.fill(COLOR_BLACK)
        # Music slider
        pygame.draw.rect(self.screen, COLOR_WHITE, self.music_slider)
        music_handle_x = self.music_slider.x + (self.sound_manager.music_volume * self.music_slider.width)
        pygame.draw.circle(self.screen, COLOR_RED, (music_handle_x, self.music_slider.centery), 10)
        music_text = self.font.render('Music Volume', True, COLOR_WHITE)
        self.screen.blit(music_text, (self.music_slider.x, self.music_slider.y - 30))
        # SFX slider
        pygame.draw.rect(self.screen, COLOR_WHITE, self.sfx_slider)
        sfx_handle_x = self.sfx_slider.x + (self.sound_manager.sfx_volume * self.sfx_slider.width)
        pygame.draw.circle(self.screen, COLOR_RED, (sfx_handle_x, self.sfx_slider.centery), 10)
        sfx_text = self.font.render('SFX Volume', True, COLOR_WHITE)
        self.screen.blit(sfx_text, (self.sfx_slider.x, self.sfx_slider.y - 30))
        for button in self.buttons:
            pygame.draw.rect(self.screen, COLOR_BLUE, button['rect'])
            text = self.font.render(button['text'], True, COLOR_WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)