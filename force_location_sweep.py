import numpy as np
import matplotlib.pyplot as plt

L = 0.02
E = 200e9
b = 0.008
t = 0.002
I = b * t**3 / 12
c = t / 2

x1 = 0.003
x2 = 0.006
x_force = 0.018

R0 = 350
GF = 2.0
Vex = 3.3
G = 20
h_mem = 50e-6

forces = np.linspace(0.5, 10, 25)
locations = np.linspace(0.002, 0.018, 25)


def beam_strain(F, x):
    return (F * (x_force - x)) * c / (E * I)


def mems_bridge_output(eps, G=G, h_mem=h_mem):
    eps0 = G * eps
    y = np.array([-0.5, 0.5, 0.5, -0.5]) * h_mem
    kappa = eps0 / max(h_mem, 1e-12)
    eps_local = eps0 + kappa * y

    R1 = R0 * (1 + GF * eps_local[0])
    R2 = R0 * (1 + GF * eps_local[1])
    R3 = R0 * (1 + GF * eps_local[2])
    R4 = R0 * (1 + GF * eps_local[3])

    return Vex * ((R2 / (R1 + R2)) - (R4 / (R3 + R4)))

# Differential output using the two-sensor setup
Vmap = np.zeros((len(forces), len(locations)))
for i, F in enumerate(forces):
    for j, x_loc in enumerate(locations):
        eps1 = beam_strain(F, x1)
        eps2 = beam_strain(F, x_loc)
        V1 = mems_bridge_output(eps1)
        V2 = mems_bridge_output(eps2)
        Vmap[i, j] = V1 - V2

plt.figure(figsize=(7, 5))
plt.imshow(
    Vmap,
    aspect='auto',
    origin='lower',
    extent=[locations[0]*1000, locations[-1]*1000, forces[0], forces[-1]],
    cmap='viridis',
)
plt.colorbar(label='Differential bridge output (V)')
plt.xlabel('Contact location along beam (mm)')
plt.ylabel('Applied force (N)')
plt.title('Two-sensor differential output vs force and location')
plt.show()
