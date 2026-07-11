# StrainSimTesting
a simple strain sensor understanding model
# Strain Gauge Force Simulation (Cantilever Beam Model)

## Overview

This project simulates a strain-gauge-based force sensing system using a cantilever beam model. The simulation explores how sensor placement, noise, and beam parameters affect force estimation performance.

The model is intended to approximate force sensing in applications such as robotic grippers or load cells, where strain is measured using full Wheatstone bridge configurations.

---

## System Description

The system consists of:

- A cantilever beam with known geometry and material properties
- Two strain sensor locations placed near the fixed end of the beam
- Each sensor approximated as a full Wheatstone bridge
- A force applied at a fixed position along the beam (near the tip)

The strain at each sensor location is computed based on beam bending theory:

    strain = (F * (x_force - x_sensor)) * c / (E * I)

Where:
- F = applied force
- x_force = force application location
- x_sensor = sensor position
- E = Young’s modulus
- I = moment of inertia
- c = distance to beam surface

---

## Signal Model

Two bridge models are used in the notebook:

### Simple linear model

    V_out ≈ V_ex * GF * strain

This is a first-order approximation. It is useful for intuition and fast inverse fits, but it ignores the real bridge topology, the Poisson coupling, and the MEMS flexure gain `G`.

### 4-resistor MEMS model

Each arm is computed from the local strain tensor and the gauge orientation:

    R_i = R_0 * (1 + GF * G * gauge_strain(theta_i))

    V_out = V_ex * (R_2 / (R_1 + R_2) - R_4 / (R_3 + R_4))

This captures the actual Wheatstone bridge behavior, including the `0/90°` and `45/45°` gauge layouts, the `G` amplification, and the sign convention of the bridge wiring. It is the model used for the final force+torque and force+torsion estimates.

---

## Force Estimation

### Force from a single force location

A simple differential estimate cancels part of the location dependence:

    F_est ∝ (V1 - V2)

### Force + prying torque from two 0/90 bridges

Two 0/90 sensors at different positions see different bending moments from a normal force `F_n` and a prying moment `M_p`:

    M_i = F_n * (x_i - x_pivot) + M_p

Because the moment is linear in `x`, the two bridge outputs give two equations for the two unknowns. A grid search over `F_n` and `M_p` using the 4-resistor bridge model recovers both accurately.

### Force + torsion from a 0/90 + 45/45 pair

A 0/90 bridge is sensitive to bending but blind to shear. A 45/45 bridge (with `+45/−45/−45/+45` arms) is shear/torsion-sensitive and rejects pure bending. The two outputs decouple `F_n` and torsional torque `T`.

---

## Noise Model

The simulation includes two types of noise:

1. Absolute noise (dominant at low signal)
   - Represents amplifier and thermal noise
   - Independent of signal magnitude

2. Proportional noise
   - Scales with signal
   - Represents gain variation and other effects

Total noise:
    noise = constant + proportional

This enables simulation of realistic system behavior, including minimum detectable force.

---

## Key Findings

- Sensor spacing significantly affects force estimation accuracy
- Differential sensing (V1 − V2) removes dependency on force location
- The 4-resistor MEMS bridge model is needed for accurate multi-axis force/torque estimation; the simple linear `V ≈ V_ex * GF * strain` model underestimates force
- Two replicated 0/90° bridges can decouple normal force and prying torque because each sensor sees a different bending moment
- A dual-beam gripper with two 0/90° sensors per beam turns normal force into a common-mode signal and prying torque into a differential signal, improving force estimation under noise
- Different bridge configurations (0/90, 45/45, half, quarter) produce distinct voltage and total-resistance signatures, which can be used to reverse-engineer the sensor wiring
- Noise limits system performance more than ADC resolution
- At small signal levels, absolute noise dominates and degrades accuracy

---

## Assumptions & Limitations

This model assumes:

- Linear elastic beam behavior
- Force applied at a fixed location
- Isotropic material response
- Small strains and linear bridge behavior

What is now modeled:

- Normal force and prying/offset moment (bending)
- Torsional torque (shear strain $\gamma_{xy}$)
- 0/90° and 45/45° Wheatstone bridge orientations
- Poisson coupling in the gauge rosette
- Two-bridge decoupling of force and torque
- Two replicated 0/90° bridges resolving normal force and prying torque (Section 3.2)
- Dual-beam gripper with two 0/90° sensors per beam resolving normal force and prying torque (Section 3.3)
- Reverse-engineering candidate bridge configurations (0/90, 45/45, half, quarter) with output voltage and total resistance (Section 5)

Not yet modeled:

- ADC quantization and digital filtering
- Temperature drift and long-term stability
- Cross-axis stiffness and mounting compliance
- Dynamic loading and vibration effects

---

## Future Work

Possible extensions include:

- ADC and amplifier noise modeling
- Sensor placement optimization
- Multi-axis calibration and temperature compensation
- Dynamic loading and vibration effects

---

## Purpose

This simulation serves as a design exploration tool to understand:

- The impact of geometry on sensitivity
- The relationship between signal and noise
- Practical constraints in force sensor design

---