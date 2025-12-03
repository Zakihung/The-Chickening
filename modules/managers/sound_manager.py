# modules/managers/sound_manager.py
import pygame
from modules.utils.constants import SOUNDS_PATH  # Cho assets/sounds/

class SoundManager:
    def __init__(self):
        """
        Quản lý âm thanh: Load SFX/music.
        """
        pygame.mixer.init()  # Init mixer
        self.sounds = {}  # Dict SFX: 'cluck': sound obj
        self.music = None  # Current music
        self.load_sounds()
        self.music_volume = 0.5  # Default music vol
        self.sfx_volume = 1.0  # Default SFX vol

    def load_sounds(self):
        """Load all sounds từ assets."""
        try:
            self.sounds['cluck'] = pygame.mixer.Sound(SOUNDS_PATH + 'cluck.wav')  # Kỹ năng gà
            self.sounds['auu'] = pygame.mixer.Sound(SOUNDS_PATH + 'auu.wav')  # Cáo trúng
            self.sounds['explosion'] = pygame.mixer.Sound(SOUNDS_PATH + 'explosion.wav')  # Trứng nổ
            # Add more: music_wave.mp3 etc.
            self.music = SOUNDS_PATH + 'music_wave.mp3'  # Nhạc nền wave
        except pygame.error as e:
            print(f"Error loading sounds: {e}")

    def play_sfx(self, name, volume=None):
        if name in self.sounds:
            if volume is None:
                volume = self.sfx_volume
            self.sounds[name].set_volume(volume)
            self.sounds[name].play()

    def stop_music(self, fade_ms=500):
        pygame.mixer.music.fadeout(fade_ms)

    def play_music(self, file, volume=None, loop=-1, fade_ms=500):
        """Play music loop with fade."""
        if volume is None:
            volume = self.music_volume
        pygame.mixer.music.fadeout(fade_ms)  # Fade out current
        pygame.mixer.music.load(SOUNDS_PATH + file)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop, fade_ms=fade_ms)