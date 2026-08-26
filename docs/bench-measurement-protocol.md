# Bench measurement protocol (frequency, voltage, latency)

Simple procedures to characterize the quantities that the current publication reports as "not measured". None of them requires certified/calibrated instrumentation: frequency and latency depend only on the instrument's crystal time base, and voltage needs an ordinary multimeter. Report instrument models and the method; traceable calibration is only required in regulatory/compliance contexts, not for research characterization.

## 1. Vibration frequency at operating voltage

**Recommended: piezo disc + oscilloscope.** Tape a piezoelectric buzzer disc to the prosthetic tube near the motor and connect it directly to one scope channel. Run the motor from the battery rail (as in the device). The period of the displayed oscillation is the mechanical vibration frequency at the actual mounting point. Read at full charge (4.2 V) and near-empty (≈3.5 V).

*Alternative (zero cost):* record the motor tone with a smartphone **microphone** spectrum-analyzer app (48 kHz sampling); the fundamental peak is the rotation frequency. Do **not** use the phone's accelerometer (100–400 Hz sampling — below Nyquist for a ~150–200 Hz signal).

*Cross-check (electrical):* commutation ripple across the motor terminals or a 1 Ω series resistor; rotation frequency = ripple frequency ÷ number of commutator segments (typically 3).

## 2. Motor terminal voltage

Multimeter across the motor terminals while running, at full and near-empty battery. Report the range (battery rail minus the transistor saturation drop).

## 3. Sensor-to-vibration latency

Two-channel oscilloscope, single-trigger:
- CH1 on the transistor collector (electrical switching instant);
- CH2 on the piezo disc on the tube (first mechanical oscillation).

Press the FSR; measure the interval from the collector edge to the first oscillation exceeding a small threshold. Repeat 10 times; report the median and range. This captures the full electromechanical spin-up latency of the ERM motor as mounted.

## Suggested reporting sentence

> "Vibration frequency at the operating voltage was measured with a piezoelectric disc coupled to the prosthetic tube and a digital oscilloscope (<model>): f = XX Hz at 4.0 V. The sensor-to-vibration latency, from transistor switching to the first detectable oscillation, was XX ms (median of 10 trials)."
