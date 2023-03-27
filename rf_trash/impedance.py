import math

def z_inductor(l, f):
    return 1j * math.tau * f * l

def z_capacitor(c, f):
    return -1j / (math.tau * f * c)

def reflection_coefficient(z, z0=50.0):
    return (z - z0) / (z + z0)

def reflection_to_impedance(g, z0=50.0):
    # (z - z0) / (z + z0) = g
    # 1 + g = (z + z0 + z - z0)/(z + z0) = 2z  / (z + z0)
    # 1 - g = (z + z0 - z + z0)/(z + z0) = 2z0 / (z + z0)
    # z/z0 = (1 + g) / (1 - g)
    return z0 * (1 + g) / (1 - g)

def synthesize_reactance(x, f):
    if x >= 0.0:
        return "L", x / (math.tau * f)
    else:
        return "C", -1 / (x * math.tau * f)
