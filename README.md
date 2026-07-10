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

Each sensor is modeled as a full-bridge strain gauge:

    V_out ≈ V_ex * GF * strain

Where:
- V_ex = excitation voltage
- GF = gauge factor

---

## Force Estimation

Force is estimated using differential sensing:

    F_est ∝ (V1 - V2)

This approach cancels location-dependent effects and isolates the force signal.

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

Not yet modeled:

- ADC quantization and digital filtering
- Temperature drift and long-term stability
- Cross-axis stiffness and mounting compliance
- Dynamic loading and vibration effects

---

## Future Work

Possible extensions include:

- Variable contact location estimation
- ADC and amplifier noise modeling
- Sensor placement optimization
- Dynamic loading and vibration effects

---

## Purpose

This simulation serves as a design exploration tool to understand:

- The impact of geometry on sensitivity
- The relationship between signal and noise
- Practical constraints in force sensor design

---