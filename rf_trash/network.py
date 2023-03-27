from .impedance import *
from .twoport import *
from .test import *

# The parallel operator.
def parallel(*args):
    return 1 / sum(1/x for x in args)

assert_almost_zero(parallel(50, 75) - 30)

def network_evaluate(elements, data, freq, z0=50.0):
    network_t = identity_2x2()
    for series, kind, value in elements:
        if kind == "R":
            z = value
        elif kind == "L":
            z = z_inductor(value, freq)
        elif kind == "C":
            z = z_capacitor(value, freq)
        elif kind == "LCR_series":  # Series LCR circuit.
            l, c, r = value
            z = z_inductor(l, freq) + z_capacitor(c, freq) + r
        elif kind == "LCR_parallel": # Parallel LCR circuit.
            l, c, r = value
            z = parallel(z_inductor(l, freq), z_capacitor(c, freq), r)
        elif kind == "resonator": # Quartz or ceramic resonator
            l_m, c_m, r_m, c_p = value
            z = parallel(
                z_inductor(l_m, freq) + z_capacitor(c_m, freq) + r_m,
                z_capacitor(c_p, freq)
            )

        elif kind in ["S", "data"]:
            # Raw S-parameters, special case.
            s = s_to_t(value if kind == "S" else data[value].get(freq))
            network_t = mul_2x2(network_t, s)
            continue
        else:
            raise ValueError(f"Component {kind} not implemented")

        network_t = mul_2x2(network_t,
            t_series_impedance(z, z0) if series else t_shunt_impedance(z, z0))

    return t_to_s(network_t)
