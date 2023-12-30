def calculate(rotation_speed_angle, steering=0):
    if rotation_speed_angle > 0:
        steering += rotation_speed_angle
        if steering + rotation_speed_angle >= 1:
            steering = 1
    elif rotation_speed_angle < 0:
        steering += rotation_speed_angle
        if steering + rotation_speed_angle <= -1:
            steering = -1
    return steering