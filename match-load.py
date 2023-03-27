import math
import cmath
from sys import argv
from rf_trash.l_match import l_match
from rf_trash.impedance import reflection_to_impedance, synthesize_reactance
from rf_trash.dec_units import display_component
from rf_trash.s2p import read_s2p, nearest_point
from rf_trash.twoport import load_match, gamma_in

if not len(argv) == 3:
    print(f"Usage: {argv[0]} <s2p> <freq>")
    exit(1)

with open(argv[1]) as f:
    points = read_s2p(f)

freq = float(argv[2])
nearest_freq, s = nearest_point(points, freq)
print(f"The nearest point is {(nearest_freq - freq) / 1e6} MHz away.")

matched_gamma = load_match(s)
print(f"Matched gamma: {matched_gamma}")

if abs(matched_gamma) >= 1.0:
    print("Impossible to realize.")
    exit(1)

matched_load = reflection_to_impedance(matched_gamma)
print(f"Matched load impedance: {matched_load}")

assert abs(gamma_in(s, matched_gamma)) < 1e-9

shunt_first, shunt, series = l_match(matched_load)
print(f"L-match result: shunt first: {shunt_first}, shunt Z: {shunt}, series Z: {series}")
print(f"Shunt: {display_component(synthesize_reactance(shunt.imag, freq))}")
print(f"Series: {display_component(synthesize_reactance(series.imag, freq))}")
