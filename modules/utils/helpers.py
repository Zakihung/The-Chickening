# modules/utils/helpers.py
# Các hàm tiện ích chung: collision, math helpers cho game

import pygame
import math
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def rect_collision(rect1, rect2):
    """Kiểm tra va chạm giữa 2 Pygame Rect."""
    return rect1.colliderect(rect2)

def circle_collision(pos1, pos2, radius1, radius2):
    """Kiểm tra va chạm giữa 2 vòng tròn (dùng cho AoE, projectiles)."""
    dist = distance(pos1, pos2)
    return dist < (radius1 + radius2)

def distance(pos1, pos2):
    """Khoảng cách Euclidean giữa 2 điểm (x, y)."""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return math.sqrt(dx**2 + dy**2)

def clamp(value, min_val, max_val):
    """Giới hạn giá trị trong khoảng [min, max]."""
    return max(min_val, min(value, max_val))

def clamp_pos(pos):
    """Giới hạn vị trí trong màn hình."""
    x, y = pos
    return (clamp(x, 0, SCREEN_WIDTH), clamp(y, 0, SCREEN_HEIGHT))

def lerp(start, end, t):
    """Linear interpolation cho smooth movement/animation (t từ 0-1)."""
    return start + (end - start) * t