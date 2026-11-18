# Evidências por fase

## Fase 0: preparação (18/11/2026)
Planos conferidos nos painéis de Make, Zapier e n8n. Detalhes em [`planos.md`](planos.md).

## Fase 1: dados (18/11/2026)
- `scripts/gerar_dados.py` (seed 42) gera `dados/ordens.csv`: 200 linhas e 7 colunas.
- Referência em Python: 149 ordens com pendência (qtd_pendente maior que zero), soma 7.981, 49 negativas e 2 zeradas.
- Planilha Google `alerta-desvio-consumo`, aba `ordens` (A1:H201, coluna H = `D − E`) e aba `resumo` (cabeçalhos).

## Fase 2: dashboard (18/11/2026)
- Página em HTML publicada no GitHub Pages (pasta `docs/`, branch `main`): https://prodigyb0y.github.io/alerta-desvio-consumo/
- A página lê a aba `ordens` publicada como CSV. Rodapé confirmado como "Fonte: Google Sheets ao vivo", com 200 ordens e 149 com pendência, iguais à referência em Python.
- Decisão de usar HTML no lugar do Looker Studio: [`decisoes.md`](decisoes.md).
