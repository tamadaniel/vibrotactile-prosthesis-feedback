# Bench measurement protocol (frequency, voltage, latency)

> **Latency (§3) has since been measured** — 110 ms to onset, 137 ms to half amplitude. The captures, analysis and figure are in [`bench/latency/`](../bench/latency/); §3 below is kept as the procedure that was followed. Frequency (§1) and motor voltage (§2) remain open.

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

**As executed:** a PicoScope 2204A recorded the FSR step directly (rather than the collector edge) on CH1 and a piezo element on the motor housing on CH2. Timing was referenced to the FSR step located by its mid-level crossing, because the scope trigger fired 2–7 ms after the step began. Five of ten captures contained complete waveforms. Because the ERM builds up gradually, two instants are reported instead of one: see [`bench/latency/`](../bench/latency/).

## Suggested reporting sentence

> "Vibration frequency at the operating voltage was measured with a piezoelectric disc coupled to the prosthetic tube and a digital oscilloscope (<model>): f = XX Hz at 4.0 V."

The latency sentence is no longer a template; the measured wording is in the manuscript and in [`bench/latency/README.md`](../bench/latency/README.md).
