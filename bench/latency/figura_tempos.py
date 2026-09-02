"""Figure of the five captures containing waveforms: FSR step, manual cursor, thresholds.

Shows at a glance why the measured number depends on the criterion: the piezo
envelope grows over tens of milliseconds, so each threshold lands at a different
point of that rise.
"""

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analisa_tempos import (BASE_ATE, LIMIARES, carrega, degrau_fsr,
                            inicio_piezo, manual)

AQUI = Path(__file__).resolve().parent
CORES = {3: "#2ca02c", 5: "#ff7f0e", 10: "#d62728"}

arquivos = []
for f in sorted(AQUI.glob("*_med*.csv"),
                key=lambda p: int(re.search(r"med(\d+)", p.name).group(1))):
    d = carrega(f)
    if d is not None:
        arquivos.append((int(re.search(r"med(\d+)", f.name).group(1)), d))

fig, axs = plt.subplots(len(arquivos), 1, figsize=(7.0, 1.55 * len(arquivos)),
                        sharex=True)
for ax, (n, d) in zip(np.atleast_1d(axs), arquivos):
    t0 = degrau_fsr(d)
    base = d[d.t_ms < BASE_ATE].B_mV
    mu, sd = base.mean(), base.std()

    # piezo envelope: absolute maximum over sliding 2 ms windows
    jan = max(1, int(2.0 / np.median(np.diff(d.t_ms))))
    env = (d.B_mV - mu).abs().rolling(jan, center=True, min_periods=1).max()

    ax.plot(d.t_ms, env / sd, lw=0.7, color="0.35")
    ax.axvline(t0, color="#1f77b4", lw=1.2)
    ax.axvline(t0 + manual[n], color="k", lw=1.2, ls="--")
    for k in LIMIARES:
        tp, _ = inicio_piezo(d, t0, k)
        ax.axhline(k, color=CORES[k], lw=0.6, ls=":", alpha=.7)
        if tp is not None:
            ax.axvline(tp, color=CORES[k], lw=1.0, alpha=.85)
    ax.set_yscale("log")
    ax.set_ylim(0.5, 200)
    ax.set_ylabel(f"med{n}\n$|B|/\\sigma$", fontsize=7)
    ax.tick_params(labelsize=7)
    ax.grid(alpha=.25, lw=.4)

np.atleast_1d(axs)[-1].set_xlabel("time (ms), zero = oscilloscope trigger",
                                  fontsize=8)
np.atleast_1d(axs)[0].set_title(
    "blue: FSR step   |   black dashed: manual cursor   |   "
    "green/orange/red: 3, 5 and 10 $\\sigma$", fontsize=8)
fig.tight_layout(pad=0.4)
for ext in ("png", "pdf"):
    fig.savefig(AQUI / f"tempos_criterio.{ext}", dpi=600, bbox_inches="tight")
print(f"tempos_criterio.png / .pdf  ({len(arquivos)} capturas)")
