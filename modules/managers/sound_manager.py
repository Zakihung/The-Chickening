# modules/managers/sound_manager.py
import pygame
from modules.utils.constants import SOUNDS_PATH

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 1.0
        self.load_sounds()

    def load_sounds(self):
        try:
            self.sounds['cluck'] = pygame.mixer.Sound(SOUNDS_PATH + 'cluck.wav')
            # self.sounds['auu'] = pygame.mixer.Sound(SOUNDS_PATH + 'auu.wav')
            # self.sounds['explosion'] = pygame.mixer.Sound(SOUNDS_PATH + 'explosion.wav')
        except pygame.error as e:
            print(f"Error loading sounds: {e}")

    def play_sfx(self, name, volume=None):
        if name in self.sounds:
            if volume is None:
                volume = self.sfx_volume
            self.sounds[name].set_volume(volume)
            self.sounds[name].play()

    def play_music(self, file, volume=None, loop=-1, fade_ms=500):
        if volume is None:
            volume = self.music_volume
        pygame.mixer.music.fadeout(fade_ms)
        pygame.mixer.music.load(SOUNDS_PATH + file)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop, fade_ms=fade_ms)

    def stop_music(self, fade_ms=500):
        pygame.mixer.music.fadeout(fade_ms)