target_drift_angle_const = 1.3


def calculate(drift_angle, rotation_speed_angle, target_drift_angle, steering=0):
    if target_drift_angle < drift_angle and rotation_speed_angle < 0:
        steering -= (abs(rotation_speed_angle) + 0.001) * target_drift_angle_const
        if steering - (abs(rotation_speed_angle) + 0.001) * target_drift_angle_const <= -1:
            steering = -1
    elif target_drift_angle > drift_angle and rotation_speed_angle > 0:
        steering += (abs(rotation_speed_angle) + 0.001) * target_drift_angle_const
        if steering + (abs(rotation_speed_angle) + 0.001) * target_drift_angle_const >= 1:
            steering = 1

    return steering