# Resonance, Q Factor, and Bandwidth in RLC Circuits

Amateur radio operation heavily relies on the understanding and manipulation of various electronic circuits. Among those, the Resistor-Inductor-Capacitor (RLC) circuit is fundamental. This chapter will explore the properties and behaviours of RLC circuits, focusing on the concepts of resonance, quality factor (Q), and half-power bandwidth.

## Resonance in RLC Circuits

**Resonance** is a unique phenomenon that occurs in RLC circuits when the reactive power supplied by the inductor is equal to the reactive power absorbed by the capacitor. In this state, the voltage across the reactances (inductor and capacitor) in a *series RLC circuit* can be higher than the voltage applied to the entire circuit.

In a series RLC circuit at resonance, the circuit's impedance is approximately equal to the circuit resistance. This is because the inductive reactance and capacitive reactance cancel each other out, leaving only the resistance in the circuit. 

In contrast, a *parallel RLC circuit* at resonance exhibits a different behavior. The impedance's magnitude is much larger compared to the circuit resistance. This is due to the inductive and capacitive reactances forming a high impedance path, which reduces the overall current flow, making the circuit's impedance appear large.

## Quality Factor (Q) in RLC Circuits

The **Quality Factor** or **Q** of an RLC circuit is a dimensionless parameter that indicates the energy losses within the circuit. It is a measure of how much energy is lost (dissipated as heat) compared to how much energy is stored in the circuit. A high Q value means less energy loss, thus a more efficient circuit.

Increasing the Q of an impedance-matching circuit will decrease the matching bandwidth. This is because a high Q value signifies a narrow bandwidth and a low loss circuit. Conversely, a low Q value signifies a wide bandwidth and a high loss circuit.

The Q of a parallel RLC circuit can be calculated by dividing the reactance of either the inductance or capacitance by the resistance. For a series RLC circuit, Q is calculated by dividing the circuit's resonant frequency by the difference between its upper and lower half-power frequencies (also known as the bandwidth).

## Half-Power Bandwidth and Resonant Frequency

The **half-power bandwidth** of a resonant circuit refers to the range of frequencies over which the power in the circuit is at least half of its maximum value. This concept is closely related to the Q of the circuit and the resonant frequency.

The **resonant frequency** of an RLC circuit is the frequency at which the circuit reaches resonance. It can be calculated using the values of resistance (R), inductance (L), and capacitance (C) in the circuit.

## Current and Voltage in RLC Circuits

In an RLC circuit, the relationship between current and voltage can tell us a lot about the circuit's operation state. At the resonance of a series RLC circuit, the voltage and current are in phase. This means they reach their maximum and minimum values simultaneously.

In a parallel RLC circuit at resonance, the magnitude of the circulating current within the components (inductor and capacitor) is at a maximum, while the current at the circuit's input is at a minimum.

## Impact of Increasing Q in RLC Circuits

Increasing the Q of a series resonant circuit has several effects. One of these is an increase in internal voltages. This is because a higher Q means less energy is lost in each cycle, so more energy is available to be stored in the circuit's reactive elements, leading to higher voltages.