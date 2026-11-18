#!/usr/bin/env python3
"""Gera dashboard/index.html a partir de dashboard/template.html e dados/ordens.csv.

Embute os dados como snapshot (ordem, area, componente, qtd_necessaria,
qtd_consumida). A coluna de e-mail não entra no HTML.

Uso: python3 scripts/gerar_dashboard.py
"""
import csv
import json
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV_ENTRADA = RAIZ / "dados" / "ordens.csv"
TEMPLATE = RAIZ / "dashboard" / "template.html"
SAIDA = RAIZ / "dashboard" / "index.html"


def main():
    with CSV_ENTRADA.open(encoding="utf-8", newline="") as f:
        linhas = [
            [r["ordem"], r["area"], r["componente"], int(r["qtd_necessaria"]), int(r["qtd_consumida"])]
            for r in csv.DictReader(f)
        ]
    dados = json.dumps(linhas, ensure_ascii=False, separators=(",", ":"))
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__DATA__", dados).replace("__DATE__", date.today().strftime("%d/%m/%Y"))
    SAIDA.write_text(html, encoding="utf-8")
    print(f"{len(linhas)} linhas embutidas em {SAIDA}")


if __name__ == "__main__":
    main()
