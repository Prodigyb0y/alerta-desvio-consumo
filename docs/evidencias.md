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

## Fase 3: cálculo com n8n (18/11/2026)
- Fluxo: gatilho manual → Google Sheets (ler linhas de `ordens`) → Filter (`qtd_pendente_calc` > 0) → Aggregate → Code → Google Sheets (append em `resumo`, `ferramenta` = "N8N"). Sem nó de Gmail: o e-mail é do Zapier.
- Exportado sem alterações em [`n8n/workflow.json`](../n8n/workflow.json) (fluxo inativo, só execução manual).
- Resultado gravado em `resumo`: total_pendentes 149, soma_pendente 7.981, top 5 = Válvula solenoide (1205), Vedação de borracha (966), Mancal de apoio (904), Parafuso M8 (863), Rolamento 6204 (737). Igual à referência em Python.
- O código do nó Code foi reexecutado fora do n8n sobre `dados/ordens.csv` e deu o mesmo resultado.
- Ajuste posterior: `data_execucao` passou a sair como `dd/mm/aaaa hh:mm:ss` (fuso America/Sao_Paulo). Execução de conferência gravou `18/11/2026 20:07:31 | N8N | 149 | 7981` com o mesmo top 5. O `n8n/workflow.json` reflete esse código.
