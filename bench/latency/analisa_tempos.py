"""Mede o atraso FSR -> piezoeletrico direto das ondas e compara com a planilha.

Montagem, lida dos dados e confirmada nos PNG: o canal A e o FSR, que faz um
degrau de ~3,75 V para ~3,02 V no acionamento; o canal B e o piezoeletrico, cuja
oscilacao cresce a partir de algumas dezenas de milissegundos depois. O tempo em
tempo.xlsx e essa diferenca, lida a mao com os cursores do PicoScope.

Duas coisas que a leitura manual nao captura, e que este script separa:

1. O degrau do FSR NAO cai em t = 0. O osciloscopio dispara alguns milissegundos
   depois do degrau comecar (aqui, de 2 a 7 ms), de modo que usar t = 0 como
   inicio subestima o atraso. O script acha o degrau de verdade, exigindo uma
   queda maior que QUEDA_MIN para que picos de ruido (ate 0,18 V) nao vencam.

2. O piezo nao tem borda: a amplitude cresce devagar, e o instante lido depende
   do limiar. Por isso o script reporta o inicio em varios limiares em vez de um
   so, para que a sensibilidade fique visivel.

Uso:  python analisa_tempos.py
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
QUEDA_MIN = 0.30     # V: degrau real do FSR e ~0,63 V; ruido chega a 0,18 V
LIMIARES = (3, 5, 10)  # desvios-padrao do ruido do piezo
PERSISTENCIA = 3     # amostras consecutivas acima do limiar
BASE_ATE = -20.0     # ms: janela de ruido, bem antes do degrau


def carrega(caminho):
    """(t_ms, A_V, B_mV) ou None se o arquivo nao contiver ondas."""
    with open(caminho, encoding="latin-1") as f:
        if not f.readline().startswith("Tempo"):
            return None
    d = pd.read_csv(caminho, sep=";", skiprows=[1], decimal=",",
                    encoding="latin-1")
    d.columns = ["t_ms", "A_V", "B_mV"]
    return d.dropna().astype(float)


def degrau_fsr(d):
    """Instante do degrau, pelo cruzamento do ponto medio entre os patamares.

    A diferenca entre amostras consecutivas nao serve: em algumas capturas a
    transicao se espalha por duas ou tres amostras e a maior queda isolada
    (0,27 V) fica abaixo dos picos de ruido de outras capturas (0,18 V). O
    cruzamento do meio-nivel e imune as duas coisas.
    """
    alto = d[d.t_ms < BASE_ATE].A_V.median()
    baixo = d[d.t_ms > 20].A_V.median()
    if alto - baixo < QUEDA_MIN:
        return None
    meio = (alto + baixo) / 2
    abaixo = (d.A_V.values < meio).astype(int)
    # PRIMEIRA travessia sustentada, nao a ultima: o FSR volta a subir no fim de
    # varias capturas (o dedo sai do sensor), e procurar o ultimo ponto acima do
    # meio-nivel encontrava esse retorno em vez do acionamento.
    n = 30                                   # ~5 ms de permanencia
    corrida = np.convolve(abaixo, np.ones(n, int), mode="valid")
    idx = np.flatnonzero(corrida == n)
    return float(d.t_ms.values[idx[0]]) if len(idx) else None


def inicio_piezo(d, t0, k):
    """Primeiro instante apos t0 com PERSISTENCIA amostras acima de k sigma."""
    base = d[d.t_ms < BASE_ATE].B_mV.values
    mu, sd = base.mean(), base.std()
    dep = d[d.t_ms > t0]
    acima = (np.abs(dep.B_mV.values - mu) > k * sd).astype(int)
    corrida = np.convolve(acima, np.ones(PERSISTENCIA, int), mode="valid")
    idx = np.flatnonzero(corrida == PERSISTENCIA)
    return (float(dep.t_ms.values[idx[0]]) if len(idx) else None), sd


planilha = pd.read_excel(AQUI / "tempo.xlsx")
planilha.columns = ["trial", "manual_ms"]
manual = dict(zip(planilha.trial, planilha.manual_ms))


if __name__ == "__main__":
    linhas = []
    for f in sorted(AQUI.glob("*_med*.csv"),
                    key=lambda p: int(re.search(r"med(\d+)", p.name).group(1))):
        n = int(re.search(r"med(\d+)", f.name).group(1))
        d = carrega(f)
        if d is None:
            linhas.append(dict(trial=n, manual=manual.get(n), t_fsr=None,
                               **{f"lim{k}": None for k in LIMIARES}))
            continue
        t0 = degrau_fsr(d)
        if t0 is None:
            # nenhuma queda maior que QUEDA_MIN: o FSR nao acionou nessa captura
            linhas.append(dict(trial=n, manual=manual.get(n), t_fsr=None,
                               **{f"lim{k}": None for k in LIMIARES}))
            continue
        lin = dict(trial=n, manual=manual.get(n), t_fsr=round(t0, 2))
        for k in LIMIARES:
            tp, sd = inicio_piezo(d, t0, k)
            lin[f"lim{k}"] = None if tp is None else round(tp - t0, 1)
        linhas.append(lin)

    t = pd.DataFrame(linhas)

    print("Atraso FSR -> piezo (ms), por criterio de inicio do piezo\n")
    print(t.rename(columns={"t_fsr": "degrau FSR (ms)",
                            **{f"lim{k}": f"{k} sigma" for k in LIMIARES}})
           .to_string(index=False, na_rep="  --"))

    comp = t.dropna(subset=[f"lim{LIMIARES[0]}"])
    if len(comp):
        print(f"\ncapturas com ondas: {len(comp)} de {len(t)} arquivos")
        print(f"  degrau do FSR ocorre {comp.t_fsr.min():.1f} a "
              f"{comp.t_fsr.max():.1f} ms ANTES do gatilho do osciloscopio")
        for k in LIMIARES:
            dif = (comp[f"lim{k}"] - comp.manual)
            print(f"  {k:2d} sigma: mediana {comp[f'lim{k}'].median():6.1f} ms   "
                  f"vs manual: {dif.median():+6.1f} ms "
                  f"({dif.min():+.1f} a {dif.max():+.1f})")

    v = planilha.manual_ms
    print(f"\nPlanilha, 10 tentativas: media {v.mean():.2f} ms, "
          f"DP {v.std(ddof=1):.2f} ms, mediana {v.median():.2f} ms")
    print(f"  faixa {v.min():.2f}-{v.max():.2f} ms | "
          f"CV {100 * v.std(ddof=1) / v.mean():.1f}%")
    print(f"  IC95% da media: [{v.mean() - 2.262 * v.sem():.2f}, "
          f"{v.mean() + 2.262 * v.sem():.2f}] ms  (t de Student, 9 gl)")
