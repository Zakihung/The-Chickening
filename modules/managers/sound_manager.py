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

    def play_sfx(self, sfx_name, volume=1.0):
        """Play SFX với volume (0-1)."""
        if sfx_name in self.sounds:
            self.sounds[sfx_name].set_volume(volume)
            self.sounds[sfx_name].play()

    def play_music(self, loop=-1):
        """Play music loop (-1 infinite)."""
        if self.music:
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(loop)