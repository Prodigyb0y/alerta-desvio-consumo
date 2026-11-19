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

## Fase 4: cálculo com Make (18/11/2026)
- Cenário `alerta-desvio-consumo` (Search Rows → Array aggregator com filtro `qtd_pendente_calc` > 0 → Iterator → Array aggregator → Add a Row em `resumo`). Detalhes e como importar: [`make/README.md`](../make/README.md).
- Gatilho manual e cenário inativo. O n8n permanece inativo.
- Execução bem-sucedida gravou em `resumo`: `18/11/2026 20:45:21 | MAKE | 149 | 7981 | Válvula solenoide (1205); Vedação de borracha (966); Mancal de apoio (904); Parafuso M8 (863); Rolamento 6204 (737)`. Igual à referência em Python e à linha do n8n.
- Consumo da execução: 5 operações (5 créditos).
- Correção feita no caminho: o filtro tinha sido salvo com o texto `qtd_pendente_calc` e operador de tempo, e por isso não bloqueava nenhuma linha. Foi refeito com a coluna H e operador numérico.
- `make/blueprint.json` foi montado a partir da configuração aplicada no cenário e pode diferir em metadados do que o botão "Export Blueprint" gera.

## Fase 5: notificação com Zapier (18/11/2026)
- Zap de duas etapas (Google Sheets "New Spreadsheet Row" em `resumo` → Gmail "Send Email" para o endereço de teste). Detalhes em [`zapier/README.md`](../zapier/README.md). O Zapier não agrega nada.
- Execução real: o n8n gravou a linha `18/11/2026 21:04:28 | N8N | 149 | 7981` e o Zap rodou às 21:06:32 (histórico do Zapier: Successful, 1 tarefa), enviando o e-mail `[N8N] Alerta de desvio de consumo: 149 ordens com pendência`.
- O e-mail foi refeito em HTML (v2) e o rótulo da soma passou a "Unidades pendentes (necessárias − consumidas)". Na v3 o top 5 passou a uma linha por componente (`Componente — N un.`): n8n e Make gravam o texto com quebra de linha e o Zap exibe com `white-space:pre-line`.
- Conferência da v3: execução do n8n às 21:16:08 gerou o e-mail `[N8N]` com o top 5 em lista (1205, 966, 904, 863, 737 un.), total 149 e 7981 unidades, iguais à referência em Python.
- Make no formato novo: a primeira execução (21:20:16) gravou `\n` como texto, porque o `join` usava `"\n"` entre aspas. Corrigido conforme a documentação/comunidade do Make para a constante `newline` (`join(...; newline)`). Nova execução (21:23:49) gerou o e-mail `[MAKE]` com o top 5 em lista, idêntico ao do `[N8N]` (149 ordens, 7981 unidades). `make/blueprint.json` e `n8n/workflow.json` refletem o formato novo.
- As linhas antigas de `resumo` (testes anteriores) mantêm o top 5 no formato com ponto e vírgula.
