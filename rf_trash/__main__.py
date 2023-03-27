from matplotlib import pyplot as plt
from sys import argv

from .impedance import *
from .twoport import *
from .units import *
from .network import *
from .s2p import *

def sweep(elements, data, f0, f1, steps, z0):
    increment = (f1 - f0) / steps
    pf = []
    ps11, ps21, ps12, ps22 = [], [], [], []

    for i in range(steps):
        f = f0 + i * increment
        s11, s21, s12, s22 = network_evaluate(elements, data, f, z0)
        ps11.append(s11)
        ps21.append(s21)
        ps12.append(s12)
        ps22.append(s22)
        pf.append(f)

    return pf, ps11, ps21, ps12, ps22

if not len(argv) == 2:
    print(f"Usage: {argv[0]} <script>")

with open(argv[1]) as script:
    lines = script.readlines()

elements = []
data = {}
caption = argv[1]
z0 = 50.0
for line in lines:
    line = line.strip()

    # Skip empty lines and comments.
    if not line or line.startswith("#"):
        continue

    parts = line.split()
    remainder = line[line.index(parts[0]) + len(parts[0]) + 1:]

    if parts[0] == "element":
        connection = parts[1]
        kind = parts[2]

        if len(parts) > 4:
            value = list(map(float, parts[3:]))
        else:
            value = float(parts[3])

        if connection in ["series", "shunt"]:
            elements.append((connection == "series", kind, value))
        else:
            raise ValueError("Connection type must be either series or shunt")

    elif parts[0] == "s":
        elements.append((None, "S", list(map(complex, parts[1:5]))))

    elif parts[0] == "load_s2p":
        print(f"Loading S2P data from {parts[2]}")
        data[parts[1]] = S2PData.load(parts[2])

    elif parts[0] == "s_data":
        if not z0 == 50:
            raise ValueError("The system impedance is different, can't use this data")

        elements.append((None, "data", parts[1]))

    elif parts[0] == "z0":
        z0 = float(parts[1])

    elif parts[0] == "caption":
        caption = remainder

    elif parts[0] == "empty":
        elements = []

    elif parts[0] == "sweep":
        f0 = float(parts[1])
        f1 = float(parts[2])
        steps = int(parts[3])
        f, s11, s21, s12, s22 = sweep(elements, data, f0, f1, steps, z0)

        plt.figure(f"{caption} - S-parameters")
        plt.plot(f, list(map(decibels, s11)), label="S11")
        plt.plot(f, list(map(decibels, s21)), label="S21")
        plt.plot(f, list(map(decibels, s12)), label="S12")
        plt.plot(f, list(map(decibels, s22)), label="S22")
        plt.legend()
        break

    else:
        raise ValueError(f"Incorrect command {parts[0]}")

plt.show()
