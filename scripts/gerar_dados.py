#!/usr/bin/env python3
"""Gera dados/ordens.csv com 200 ordens fictícias (seed 42).

Colunas: ordem, area, componente, qtd_necessaria, qtd_consumida,
qtd_pendente, email_responsavel.

qtd_pendente = qtd_necessaria - qtd_consumida e pode ser negativa
(consumo acima do necessário). Não há nenhum dado de planta real.

Uso: python3 scripts/gerar_dados.py
"""
import csv
import random
from pathlib import Path

SEED = 42
N_LINHAS = 200
EMAIL_TESTE = "gutenberg.demo.operacoes@gmail.com"
AREAS = ["Área A", "Área B", "Área C"]
COMPONENTES = [
    "Rolamento 6204",
    "Correia dentada",
    "Sensor de pressão",
    "Válvula solenoide",
    "Parafuso M8",
    "Filtro de ar",
    "Motor 1/2 cv",
    "Placa de controle",
    "Vedação de borracha",
    "Cabo de sinal",
    "Engrenagem helicoidal",
    "Mancal de apoio",
]
COLUNAS = [
    "ordem",
    "area",
    "componente",
    "qtd_necessaria",
    "qtd_consumida",
    "qtd_pendente",
    "email_responsavel",
]

SAIDA = Path(__file__).resolve().parent.parent / "dados" / "ordens.csv"


def gerar_linhas():
    rng = random.Random(SEED)
    linhas = []
    for i in range(1, N_LINHAS + 1):
        necessaria = rng.randint(10, 500)
        # Fator de consumo entre 60% e 115% do necessário: gera pendências
        # positivas, zeradas e negativas (consumo a mais).
        consumida = max(0, round(necessaria * rng.uniform(0.60, 1.15)))
        linhas.append(
            {
                "ordem": f"OP-{i:04d}",
                "area": rng.choice(AREAS),
                "componente": rng.choice(COMPONENTES),
                "qtd_necessaria": necessaria,
                "qtd_consumida": consumida,
                "qtd_pendente": necessaria - consumida,
                "email_responsavel": EMAIL_TESTE,
            }
        )
    return linhas


def main():
    linhas = gerar_linhas()
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)
    print(f"{len(linhas)} linhas gravadas em {SAIDA}")


if __name__ == "__main__":
    main()
