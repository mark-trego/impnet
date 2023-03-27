import math

POWERS = [
    ("M", 6),
    ("k", 3),
    ("", 1),
    ("m", -3),
    ("u", -6),
    ("n", -9),
    ("p", -12),
    ("f", -15)
]

def format_units(x, unit=""):
    for prefix, power in POWERS:
        t = x / 10**power
        if abs(t) < 1000.0 and abs(t) >= 0.1:
            return "{:.3f} {}{}".format(t, prefix, unit)
    else:
        return "{:.3f} {}".format(x, unit)

assert format_units(1234, "unit") == "1.234 kunit"
assert format_units(0.000567, "ohm") == "0.567 mohm"
assert format_units(-5e-11, "F") == "-50.000 pF"

COMPONENT_UNITS = {
    "L": "H",
    "C": "F",
    "R": "ohm"
}
def display_component(component):
    type, value = component
    return format_units(value, COMPONENT_UNITS[type])

def decibels(x):
    try:
        return 20.0 * math.log10(abs(x))
    except:
        return -150.0
