import math
import cmath
from sys import argv
from rf_trash.l_match import l_match
from rf_trash.impedance import reflection_to_impedance, synthesize_reactance
from rf_trash.dec_units import display_component

if not "--complex" in argv:
    mag = float(input("Magnitude: "))
    angle = math.radians(float(input("Angle: ")))
    gamma = mag * cmath.exp(1j * angle)
else:
    gamma = complex(input("Complex gamma: "))

z = reflection_to_impedance(gamma)
print(f"Z={z}")

f = float(input("Frequency: "))

shunt_first, shunt, series = l_match(z)
print("Shunt first" if shunt_first else "Series first")
print("Shunt: {}".format(display_component(synthesize_reactance(shunt.imag, f))))
print("Series: {}".format(display_component(synthesize_reactance(series.imag, f))))
