# modules/utils/constants.py
# Các hằng số chung cho game "The Chickening"

# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Màu sắc (RGB tuples)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)  # Cho thóc hoặc items

# Thuộc tính player mặc định
PLAYER_HP_DEFAULT = 100
PLAYER_SPEED_DEFAULT = 5  # pixels per frame
PLAYER_DAMAGE_DEFAULT = 10
EGGNERGY_MAX = 50
DODGE_COOLDOWN = 1000  # milliseconds (1 giây)

# Tấn công player
MELEE_RANGE = 50  # pixels
RANGED_RANGE = 300
BOMB_DAMAGE = 50
BOMB_AOE_RADIUS = 100
BOMB_LIMIT = 3

# Enemies
ENEMY_HP_BASE = 50
ENEMY_SPEED_BASE = 4
DROP_THO_RATE = 0.5  # Xác suất drop thóc (50%)

# Game settings
THOC_LOSS_ON_DEATH = 0.5  # Mất 50% thóc khi chết
WAVE_COUNT_PER_LEVEL = 5  # Số wave tối thiểu mỗi màn

# Paths (cho assets, sẽ dùng sau)
ASSETS_PATH = "assets/"
IMAGES_PATH = ASSETS_PATH + "images/"
SOUNDS_PATH = ASSETS_PATH + "sounds/"