from .impedance import reflection_coefficient
from .test import *

def gamma_in(s, gamma_load):
    s11, s21, s12, s22 = s
    return s11 + (s12 * s21 * gamma_load) / (1 - s22 * gamma_load)

def gamma_out(s, gamma_source):
    s11, s21, s12, s22 = s
    return s22 + (s12 * s21 * gamma_source) / (1 - s11 * gamma_source)

# Find the correct load impedance gamma so that the input presents a perfect
#  match (i.e. gamma_in is zero).
def load_match(s):
    s11, s21, s12, s22 = s
    return -s11 / (s12 * s21 - s11 * s22)

s = [0.3+0.2j, 0.1+0.5j, 5+2j, 0.1-0.4j]

assert_almost_zero(gamma_in(s, load_match(s)))

# S <-> T parameter conversion.
def t_to_s(t):
    t11, t21, t12, t22 = t
    det = t11 * t22 - t12 * t21
    return t12/t22, 1/t22, det/t22, -t21/t22

def s_to_t(s):
    s11, s21, s12, s22 = s
    det = s11 * s22 - s12 * s21
    return -det/s21, -s22/s21, s11/s21, 1/s21

assert_lists_almost_equal(
    [0.3+0.1j, 0.2-0.7j, -0.4+0.5j, -0.9j],
    t_to_s(s_to_t([0.3+0.1j, 0.2-0.7j, -0.4+0.5j, -0.9j]))
)

assert_lists_almost_equal(
    [0.3+0.1j, 0.2-0.7j, -0.4+0.5j, -0.9j],
    s_to_t(t_to_s([0.3+0.1j, 0.2-0.7j, -0.4+0.5j, -0.9j]))
)

def t_series_impedance(z, z0=50.0):
    # Derived by viewing the circuit as a voltage divider with Vs=2.
    sab = 2 * z0 / (2 * z0 + z)
    saa = reflection_coefficient(z + z0, z0)
    return s_to_t((saa, sab, sab, saa))

def t_shunt_impedance(z, z0=50.0):
    z_p = 1/(1/z + 1/z0)
    sab = 2 * z_p / (z0 + z_p)
    saa = reflection_coefficient(z_p, z0)
    return s_to_t((saa, sab, sab, saa))


def identity_2x2():
    return [1, 0, 0, 1]

def mul_2x2(u, v):
    u11, u21, u12, u22 = u
    v11, v21, v12, v22 = v

    return [
        u11*v11 + u12*v21,
        u21*v11 + u22*v21,

        u11*v12 + u12*v22,
        u21*v12 + u22*v22
    ]

s30 = t_series_impedance(30+7j)
s80 = t_series_impedance(80+3j)
s110 = t_series_impedance(110+10j)
assert_lists_almost_equal(s110, mul_2x2(s30, s80))
assert_lists_almost_equal(s110, mul_2x2(s80, s30))

p75 = t_shunt_impedance(75+75j)
p300 = t_shunt_impedance(300+300j)
p60 = t_shunt_impedance(60+60j)
assert_lists_almost_equal(p60, mul_2x2(p75, p300))
assert_lists_almost_equal(p60, mul_2x2(p300, p75))

# Rollett stability factor
def rollett(s):
    s11, s21, s12, s22 = s
    det = s11*s22 - s12*s21
    return (1 - abs(s11)**2-abs(s22)**2+abs(det)**2) / (2 * abs(s12*s21))
