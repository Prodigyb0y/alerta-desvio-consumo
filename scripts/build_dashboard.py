#!/usr/bin/env python3
"""Gera docs/index.html (dashboard HTML autocontido) a partir de
dashboard/template-bi.html + dados/ordens.csv.

O CSV vai embutido no HTML como snapshot, então a página funciona sem
servidor e sem instalação. Para dados ao vivo, preencha SHEET_CSV_URL no
HTML com o CSV publicado da aba "ordens" do Google Sheets.

Uso: python3 scripts/build_dashboard.py
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATE = RAIZ / "dashboard" / "template-bi.html"
CSV = RAIZ / "dados" / "ordens.csv"
SAIDA = RAIZ / "docs" / "index.html"


def main():
    csv = CSV.read_text(encoding="utf-8").strip()
    if "`" in csv or "${" in csv:
        raise SystemExit("O CSV contém caracteres que quebram o template (` ou ${).")
    html = TEMPLATE.read_text(encoding="utf-8")
    if "__CSV__" not in html:
        raise SystemExit("Marcador __CSV__ não encontrado no template.")
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(html.replace("__CSV__", csv), encoding="utf-8")
    print(f"Dashboard gravado em {SAIDA} ({len(csv.splitlines()) - 1} linhas de dados)")


if __name__ == "__main__":
    main()
