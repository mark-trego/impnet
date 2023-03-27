import cmath
def read_s2p(f):
    points = []
    scale = None

    for line in f:
        line = line.strip()

        if not line or line.startswith("!"):
            continue

        if line.startswith("#"):
            print(f"Parameter line: {line}")
            if "MHz" in line:
                scale = 1e6
            elif "GHz" in line:
                scale = 1e9
            else:
                raise ValueError("Incorrect scale")

            continue

        parts = line.split()

        freq = float(parts[0]) * scale
        s11 = float(parts[1]) * cmath.exp(1j * float(parts[2]))
        s21 = float(parts[3]) * cmath.exp(1j * float(parts[4]))
        s12 = float(parts[5]) * cmath.exp(1j * float(parts[6]))
        s22 = float(parts[7]) * cmath.exp(1j * float(parts[8]))

        points.append((freq, [s11, s21, s12, s22]))

    print(f"{len(points)} points loaded.")
    return points

def nearest_point(points, target):
    best_error = None
    best_point = None

    for point in points:
        freq, s = point
        error = abs(freq - target)
        if best_error is None or error < best_error:
            best_error = error
            best_point = point

    return best_point

class S2PData(object):
    def __init__(self, points):
        self.points = points

    @classmethod
    def load(cls, filename):
        with open(filename) as f:
            return S2PData(read_s2p(f))

    def get(self, freq):
        _, s = nearest_point(self.points, freq)
        return s
