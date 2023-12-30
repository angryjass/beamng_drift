import math


def calculate(vel_x, vel_y, dir_x, dir_y):
    angle = (math.atan2(vel_y, vel_x)) * 180 / math.pi
    angle2 = (math.atan2(dir_y, dir_x)) * 180 / math.pi
    return round(angle) - round(angle2)