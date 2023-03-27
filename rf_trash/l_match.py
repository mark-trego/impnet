import math
from .test import *

def l_match(z, z0=50.0):
    shunt_first = z.real > z0.real

    if not shunt_first:
        z, z0 = z0, z

    y = 1.0 / z

    # Re(z0) = Re(1 / (y + y_shunt))
    # y_shunt is purely imaginary.

    # 1 / (y + y_shunt) = (Re(y) - i(Im(y) + Im(y_shunt))))/|y + y_shunt| ^ 2
    # Re(z0) = Re(1/(y+y_shunt)) = Re(y) / |y + y_shunt| ^ 2
    # |y + y_shunt| ^ 2 = Re(y) / Re(z0)
    # |y + y_shunt| ^ 2 = Re(y)^2 + Im(y + y_shunt)^2

    y_shunt = 1j * (math.sqrt(y.real / z0.real - y.real**2) - y.imag)
    z_shunt = 1 / y_shunt
    z_series = z0 - 1 / (y + y_shunt)

    # Make sure the calculation is accurate.
    assert_almost_zero(z_shunt.real)
    assert_almost_zero(z_series.real)

    # Get rid of the real parts for good.
    z_shunt = complex(0, z_shunt.imag)
    z_series = complex(0, z_series.imag)

    return shunt_first, z_shunt, z_series
