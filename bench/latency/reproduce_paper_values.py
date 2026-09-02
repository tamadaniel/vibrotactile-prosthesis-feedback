# -*- coding: utf-8 -*-
"""Reproduce the two latency figures reported in the paper.

    onset (5 sigma)   110 ms   95% CI 103-117 ms
    half amplitude    137 ms   95% CI 132-142 ms

Both are means over the five captures that contain complete waveforms, with
Student-t confidence intervals on 4 degrees of freedom. The onset uses the
detector in analisa_tempos.py; the half-amplitude instant is computed here,
since it is the only quantity the original analysis script does not print.

Envelope definition used for the half-amplitude instant, stated explicitly
because the number depends on it: the piezo signal is centred on its
pre-contact mean, rectified, and passed through a centred rolling maximum of
2 ms. Steady state is the median of that envelope over the last 30 ms of the
capture, by which time the motor has spun up. The reported instant is the
first sample after the FSR step at which the envelope reaches half of it.

Usage:  python reproduce_paper_values.py
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from analisa_tempos import BASE_ATE, carrega, degrau_fsr, inicio_piezo

HERE = Path(__file__).resolve().parent
ENVELOPE_MS = 2.0     # rolling-maximum window
STEADY_MS = 30.0      # tail window taken as steady state


def half_amplitude(d, t0):
    """Instant, relative to the FSR step, at which the envelope reaches ss/2."""
    base = d[d.t_ms < BASE_ATE].B_mV.mean()
    rect = (d.B_mV - base).abs()
    win = max(1, int(round(ENVELOPE_MS / np.median(np.diff(d.t_ms.values)))))
    env = rect.rolling(win, center=True, min_periods=1).max().values
    steady = np.median(env[d.t_ms.values > d.t_ms.values.max() - STEADY_MS])
    after = d.t_ms.values > t0
    hit = np.flatnonzero(env[after] >= steady / 2)
    return (float(d.t_ms.values[after][hit[0]]) - t0) if len(hit) else np.nan


def ci95(v):
    m, sd = v.mean(), v.std(ddof=1)
    lo, hi = stats.t.interval(0.95, len(v) - 1, loc=m, scale=sd / np.sqrt(len(v)))
    return m, sd, lo, hi


rows = []
for f in sorted(HERE.glob("*_med*.csv"),
                key=lambda p: int(re.search(r"med(\d+)", p.name).group(1))):
    d = carrega(f)
    if d is None:
        continue                      # metadata-only capture, no waveform
    t0 = degrau_fsr(d)
    if t0 is None:
        continue                      # FSR never stepped in this capture
    onset, _ = inicio_piezo(d, t0, 5)
    rows.append(dict(trial=int(re.search(r"med(\d+)", f.name).group(1)),
                     fsr_step_ms=round(t0, 2),
                     onset_ms=round(onset - t0, 1),
                     half_ms=round(half_amplitude(d, t0), 1)))

t = pd.DataFrame(rows)
print("Per-capture delays, referenced to the FSR step (ms)\n")
print(t.to_string(index=False))
print("\nn = %d captures with complete waveforms" % len(t))
print("The oscilloscope triggered %.1f to %.1f ms AFTER the FSR step began,"
      % (-t.fsr_step_ms.max(), -t.fsr_step_ms.min()))
print("which is why timing is referenced to the step and not to t = 0.\n")

for col, label in [("onset_ms", "onset (5 sigma)"), ("half_ms", "half amplitude")]:
    m, sd, lo, hi = ci95(t[col].values)
    print("%-16s mean %5.1f ms   SD %.1f   95%% CI [%.0f, %.0f] ms"
          % (label, m, sd, lo, hi))

print("\nPaper reports 110 ms [103-117] and 137 ms [132-142].")
