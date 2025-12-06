import math

def calculate_azimuth(x1, y1, x2, y2):
    return math.degrees(math.atan2((y1 + y2), (x1 + x2)))

def calculate_distance(z):
    return z
