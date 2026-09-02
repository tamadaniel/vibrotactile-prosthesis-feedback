# Latency measurement: foot loading to vibration

How long the device takes to respond, from the moment the FSR is loaded to the
moment the motor is actually vibrating. This folder holds the raw oscilloscope
captures, the analysis code, and a script that reproduces the two numbers
reported in the paper.

## Result

| Instant | Definition | Mean (n = 5) | 95% CI |
|---|---|---|---|
| Onset | first sustained excursion beyond 5 SD of the pre-contact noise | 110 ms | 103–117 ms |
| Half amplitude | envelope reaches half of its steady-state value | 137 ms | 132–142 ms |

Two instants are reported because the eccentric-mass motor accelerates
progressively: the vibration builds up over tens of milliseconds instead of
starting abruptly, so any single number depends on the threshold chosen.
`tempos_criterio.pdf` makes that dependence visible — it plots the piezo
envelope for all five captures with the 3, 5 and 10 σ criteria marked, and the
three land at visibly different points on the same rise.

Almost all of this delay is mechanical, not electronic. The analog circuit
switches the motor within microseconds; the rest is the motor spinning up.
Shortening it would require a faster actuator, such as a linear resonant
actuator, not a redesign of the circuit.

## Setup

Two-channel oscilloscope (PicoScope 2204A, 6.1 kHz per channel) recording
simultaneously:

- **Channel A** — the FSR, which steps from about 3.75 V to about 3.02 V when
  loaded.
- **Channel B** — a piezoelectric element on the motor housing, picking up the
  vibration itself rather than the drive signal.

## Two corrections the raw cursor readings do not make

The manual cursor readings in `tempo.xlsx` (mean 93.8 ms over 10 trials)
**understate** the delay, for two reasons that the analysis code handles:

1. **The oscilloscope trigger is not the FSR step.** The scope fired 2.2 to
   6.8 ms *after* the step had already begun, so taking t = 0 as the start
   loses those milliseconds. `degrau_fsr()` locates the real step by its
   mid-level crossing, which is immune both to the transition spreading across
   two or three samples and to noise spikes of up to 0.18 V.
2. **The piezo has no clean edge.** Its amplitude grows slowly, so the instant
   read off the screen depends entirely on where the eye places the threshold.
   The code reports several thresholds instead of one, so the sensitivity is
   visible rather than hidden.

All timing here is therefore referenced to the FSR step itself, not to the
oscilloscope trigger.

## Data

Ten captures were taken. **Five contain complete waveforms** (`med3`, `med7`,
`med8`, `med9`, `med10`) and are the five kept here and analysed; the other
five held only acquisition metadata, with no waveform to measure, and are not
included.

- `*_med*.csv` — raw captures, semicolon-separated, comma decimal, latin-1.
  Columns: time (ms), channel A (V), channel B (mV).
- `*_med*.png` — PicoScope screenshots of the same captures.
- `tempo.xlsx` still lists all ten trials, since the manual cursor readings
  were taken on screen before the discard.

## Code

Requires `numpy`, `pandas`, `scipy`, `matplotlib`, `openpyxl`.

```bash
python reproduce_paper_values.py   # the two numbers in the paper, with CIs
python analisa_tempos.py           # full per-trial table, 3/5/10 sigma
python figura_tempos.py            # regenerates tempos_criterio.pdf/.png
```

`reproduce_paper_values.py` is the entry point if you only want to check the
published values. `analisa_tempos.py` is the original analysis, kept verbatim
except that its report was moved inside a `__main__` guard so it can be
imported quietly; its comments are in Portuguese. The half-amplitude instant is
computed in `reproduce_paper_values.py`, which states its envelope definition
explicitly, since that number depends on it.

## Limitation

Five valid captures is a small sample, and the measurement was made on the
bench with the FSR pressed by hand, not under a walking load. Absolute timing
under gait may differ.
