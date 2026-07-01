import numpy as np
L = 0.02
E = 200e9
b = 0.008
t = 0.002
I = b * t**3 / 12
c = t / 2
x_force=0.018
x1=0.003
x2=0.006
R0=350
GF=2.0
Vex=3.3
G=20
h_mem=50e-6
forces=np.linspace(0.5,10,40)

def beam_strain(F,x):
    return (F*(x_force-x))*c/(E*I)

def mems_bridge_output(eps, G=G, h_mem=h_mem, y=np.array([-0.5,0.5,0.5,-0.5])*h_mem):
    eps0=G*eps
    kappa=eps0/max(h_mem,1e-12)
    eps_local=eps0+kappa*y
    R1=R0*(1+GF*eps_local[0]); R2=R0*(1+GF*eps_local[1]); R3=R0*(1+GF*eps_local[2]); R4=R0*(1+GF*eps_local[3])
    return Vex*((R2/(R1+R2))-(R4/(R3+R4)))

Vdiff=[]
for F in forces:
    eps1=beam_strain(F,x1)
    eps2=beam_strain(F,x2)
    V1=mems_bridge_output(eps1)
    V2=mems_bridge_output(eps2)
    Vdiff.append(V1-V2)
Vdiff=np.array(Vdiff)
print('min,max',Vdiff.min(),Vdiff.max())
print('unique', np.unique(np.round(Vdiff,15)).size)
print('polyfit1', np.polyfit(Vdiff, forces, 1))
print('polyfit3', np.polyfit(Vdiff, forces, 3))
