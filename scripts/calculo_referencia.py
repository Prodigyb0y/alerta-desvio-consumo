#!/usr/bin/env python3
"""Cálculo de referência do resumo, feito só com a biblioteca padrão.

Lê dados/ordens.csv, calcula a pendência como qtd_necessaria - qtd_consumida
e imprime o que n8n e Make devem gravar na aba "resumo": total de ordens com
pendência (> 0), soma da pendência e os 5 componentes com maior pendência.

Uso: python3 scripts/calculo_referencia.py
"""
import csv
from collections import defaultdict
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "dados" / "ordens.csv"


def main():
    with CSV.open(encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))

    pendencias = [(l["componente"], int(l["qtd_necessaria"]) - int(l["qtd_consumida"])) for l in linhas]
    positivas = [(c, p) for c, p in pendencias if p > 0]

    por_componente = defaultdict(int)
    for c, p in positivas:
        por_componente[c] += p
    top5 = sorted(por_componente.items(), key=lambda x: x[1], reverse=True)[:5]

    print(f"Linhas: {len(linhas)}")
    print(f"Ordens com pendência (> 0): {len(positivas)}")
    print(f"Soma da pendência: {sum(p for _, p in positivas)}")
    print(f"Negativas: {sum(1 for _, p in pendencias if p < 0)} | Zeradas: {sum(1 for _, p in pendencias if p == 0)}")
    print("Top 5 componentes:")
    for c, v in top5:
        print(f"  {c} — {v} un.")


if __name__ == "__main__":
    main()
