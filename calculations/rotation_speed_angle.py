import math


def calculate(rotation_1, rotation_2):
    rotation_speed_const = 2
    return round((abs(rotation_1) - abs(rotation_2)) * 180 / math.pi / rotation_speed_const, 3)