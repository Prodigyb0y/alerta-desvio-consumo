#!/usr/bin/env python3
"""Gera docs/index.html (dashboard HTML autocontido) a partir de
dashboard/template.html + dados/ordens.csv + marca em dashboard/assets/.

O CSV vai embutido no HTML como snapshot, então a página funciona sem
servidor e sem instalação. Logo e ícone também vão embutidos (SVG inline e
favicon), sem arquivos externos. Para dados ao vivo, preencha SHEET_CSV_URL
no HTML com o CSV publicado da aba "ordens" do Google Sheets.

Uso: python3 scripts/build_dashboard.py
"""
import re
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATE = RAIZ / "dashboard" / "template.html"
CSV = RAIZ / "dados" / "ordens.csv"
LOGO = RAIZ / "dashboard" / "assets" / "logo-gutenberg.svg"
ICONE = RAIZ / "dashboard" / "assets" / "icone-gutenberg.svg"
SAIDA = RAIZ / "docs" / "index.html"


def svg_limpo(caminho):
    """Lê o SVG sem o bloco <metadata> (manifesto C2PA), que não serve para embutir."""
    txt = caminho.read_text(encoding="utf-8")
    txt = re.sub(r"<metadata>.*?</metadata>\s*", "", txt, flags=re.S)
    txt = txt.replace(' xmlns:c2pa="http://c2pa.org/manifest"', "")
    return txt.strip()


def svg_inline(caminho, classe):
    """SVG para uso inline: decorativo, o nome acessível fica no elemento pai."""
    return svg_limpo(caminho).replace(
        "<svg ", f'<svg class="{classe}" aria-hidden="true" focusable="false" ', 1)


def main():
    csv = CSV.read_text(encoding="utf-8").strip()
    if "`" in csv or "${" in csv:
        raise SystemExit("O CSV contém caracteres que quebram o template (` ou ${).")
    html = TEMPLATE.read_text(encoding="utf-8")
    trocas = {
        "__CSV__": csv,
        "__LOGO__": svg_inline(LOGO, "logo-full"),
        "__FAVICON__": "data:image/svg+xml," + quote(svg_limpo(ICONE)),
    }
    for marcador in trocas:
        if marcador not in html:
            raise SystemExit(f"Marcador {marcador} não encontrado no template.")
    for marcador, valor in trocas.items():
        html = html.replace(marcador, valor)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(html, encoding="utf-8")
    print(f"Dashboard gravado em {SAIDA} ({len(csv.splitlines()) - 1} linhas de dados)")


if __name__ == "__main__":
    main()
