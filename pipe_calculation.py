import math


def pipe_calculation(diameter, thickness):
    diameter = float(diameter)
    thickness = float(thickness)
    meter_weight = (math.pi / 4 * 10 ** (-6)) * (diameter ** 2 - (diameter - 2 * thickness) ** 2) * 7850
    return meter_weight
