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

- Histórico do cenário no Make (conferido em 18/11/2026, à noite): 7 execuções no total, 6 com sucesso e 1 com erro (`DataError` no mapeamento do top 5, corrigido). Além disso, houve 3 execuções de 2 operações (20:39, 20:40 e 20:43, horário de Brasília) feitas durante os ajustes do filtro. Elas não estão registradas nesta página e não foram analisadas uma a uma; a aba `resumo` foi limpa depois.

## Fase 5: notificação com Zapier (18/11/2026)
- Zap de duas etapas (Google Sheets "New Spreadsheet Row" em `resumo` → Gmail "Send Email" para o endereço de teste). Detalhes em [`zapier/README.md`](../zapier/README.md). O Zapier não agrega nada.
- Execução real: o n8n gravou a linha `18/11/2026 21:04:28 | N8N | 149 | 7981` e o Zap rodou às 21:06:32 (histórico do Zapier: Successful, 1 tarefa), enviando o e-mail `[N8N] Alerta de desvio de consumo: 149 ordens com pendência`.
- O e-mail foi refeito em HTML (v2) e o rótulo da soma passou a "Unidades pendentes (necessárias − consumidas)". Na v3 o top 5 passou a uma linha por componente (`Componente — N un.`): n8n e Make gravam o texto com quebra de linha e o Zap exibe com `white-space:pre-line`.
- Conferência da v3: execução do n8n às 21:16:08 gerou o e-mail `[N8N]` com o top 5 em lista (1205, 966, 904, 863, 737 un.), total 149 e 7981 unidades, iguais à referência em Python.
- Make no formato novo: a primeira execução (21:20:16) gravou `\n` como texto, porque o `join` usava `"\n"` entre aspas. Corrigido conforme a documentação/comunidade do Make para a constante `newline` (`join(...; newline)`). Nova execução (21:23:49) gerou o e-mail `[MAKE]` com o top 5 em lista, idêntico ao do `[N8N]` (149 ordens, 7981 unidades). `make/blueprint.json` e `n8n/workflow.json` refletem o formato novo.
- As linhas antigas de `resumo` (testes anteriores) mantêm o top 5 no formato com ponto e vírgula.

## Fase 6: README final e organização (18/11/2026)
- README reescrito: visão geral, diagrama do fluxo, resultado de referência, estrutura, como reproduzir, decisões e limitações.
- Novo `scripts/calculo_referencia.py` (apenas biblioteca padrão), que reproduz os números de referência: 200 linhas, 149 ordens com pendência, soma 7.981, 49 negativas, 2 zeradas e o mesmo top 5.
- Imagens dos e-mails `[N8N]` e `[MAKE]` em `docs/img/`.
- Limpeza: removidos os `.gitkeep` de pastas que já têm conteúdo e a nota de rascunho do README.
- Limpeza da aba `resumo`: as linhas de teste foram apagadas e ficaram a execução do n8n (21:16:08) e a do Make (21:23:49), ambas no formato novo do top 5.
- Efeito colateral encontrado: depois de apagar linhas, a linha nova do n8n (21:33:58, linha 4) não disparou o Zap em 16 minutos, porque o Zapier já tinha visto linhas até o número 7. Desligar e ligar o Zap resolveu: a linha 5 (n8n, 21:50:24) gerou a execução das 21:52:45 (Successful, 1 tarefa, e-mail `[N8N]`). A linha 4 permanece na aba sem e-mail. Documentado em `zapier/README.md`.
- Dashboard conferido em janela anônima (https://prodigyb0y.github.io/alerta-desvio-consumo/): carrega sem login, com 149 ordens com pendência, 7.981 un. de soma e maior pendência de 174 un. (OP-0075 · Rolamento 6204). Print em `docs/img/dashboard.png`.

## Fase 7: redesenho do dashboard e verificações (19/11/2026)
- Novo layout só para computador, matriz componente × área e indicador "Necessário já consumido" (84,9%, no lugar de 86,7%). Motivos em [`decisoes.md`](decisoes.md).
- **Leitura ao vivo:** testada pelo navegador do app, a partir de https://prodigyb0y.github.io: HTTP 200, 200 linhas, 149 ordens com pendência, soma 7.981, maior pendência 174 e 49 com consumo a mais, iguais ao `dados/ordens.csv`. A planilha publicada tem a coluna extra `qtd_pendente_calc`, que a página ignora.
- **Renderização:** Chrome sem interface em 1280, 1440 e 1920 px, nos temas claro e escuro, sem erro de JavaScript e sem rolagem horizontal. Números do topo conferidos: 149, 7.981, 174, 84,9% e 49.
- **Contraste:** verificação automática de todo o texto visível. Antes do ajuste, 1 célula do mapa ficava em 4,46:1; depois, 0 falhas nos dois temas. As cores das faixas de pendência e os ícones de situação foram ajustados para pelo menos 3:1 contra o fundo.
- **Teclado:** todos os controles têm foco visível; a matriz tem muitas paradas de Tab, por isso há o atalho "Pular para a tabela de ordens" (conferido: o foco vai para a tabela).
- **Árvore de acessibilidade** conferida no Chromium (títulos, nomes dos controles, estado dos filtros). **Não** foi testado com leitor de tela real (NVDA, VoiceOver) nem com pessoas.
- **Daltonismo:** simulação de deuteranopia e protanopia sobre a captura da página; a paleta de um matiz e os números escritos mantêm a leitura. Sem teste com pessoas.
- A captura `docs/img/dashboard.png` foi substituída pela da versão final (card "Ordens com excedente" incluído). Foi tirada com o CSV do repositório servido no lugar da planilha, que tem os mesmos totais, e o texto alternativo da imagem no README descreve o conteúdo da tela.
