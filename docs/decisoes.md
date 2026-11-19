# Decisões do projeto

## Dashboard em HTML no lugar do Looker Studio (18/11/2026)

**Decisão:** o dashboard é uma página HTML (`docs/index.html`) publicada no GitHub Pages. O Looker Studio não é usado.

**Motivo:** mais controle sobre o visual e a interação (filtros cruzados, matriz com mapa de calor, manual em pop-up, visão em tabela) e a demo fica junto do código, acessível por link sem instalação.

**Ligação com a base:** a página lê a aba `ordens` do Google Sheets pelo CSV publicado na web, configurado em `SHEET_CSV_URL` (`dashboard/template.html`). Se a leitura falhar, usa o snapshot de `dados/ordens.csv` embutido na página. A aba publicada fica pública, e os dados são fictícios.

**Consequências:**
- O dashboard calcula a pendência como `qtd_necessaria − qtd_consumida` na própria página, então não depende da coluna H da planilha.
- A coluna de e-mail não é usada em nenhum gráfico.
- Depois de mudar o CSV ou o template, rode `python3 scripts/build_dashboard.py` para regenerar `docs/index.html`.
- O Zapier, o n8n e o Make não mudam. O link do dashboard escrito na aba `resumo` e no e-mail é o endereço do GitHub Pages.

**Verificação:** os números da página (149 ordens com pendência, soma 7.981, maior pendência 174 em OP-0075, totais por componente e por área) foram conferidos contra o cálculo de referência em Python.

## Gatilho manual no n8n e no Make (18/11/2026)

**Decisão:** o cálculo é disparado manualmente (n8n: "Execute workflow"; Make: "Run once"). Não há agendamento ativo.

**Motivo:** o projeto é uma demonstração. Um agendamento diário aumentaria o consumo de créditos do Make e de tarefas do Zapier sem agregar valor, e faria o Zapier enviar e-mails fora da demonstração.

**Consequências:**
- Em produção, o gatilho natural seria um agendamento diário (por exemplo, 07:00 em America/Sao_Paulo). Basta trocar o gatilho manual por um Schedule Trigger no n8n ou um agendamento no Make (mínimo de 15 minutos no plano gratuito).
- Apenas uma das duas ferramentas (n8n ou Make) deve estar ativa por vez, porque o Zapier notifica toda linha nova em `resumo`.
- O Zap do Zapier continua ligado e envia um e-mail por linha nova.

## Prefixo do assunto: [N8N] e [MAKE], sem [ZAPIER] (18/11/2026)

**Decisão:** o assunto do e-mail leva o prefixo da ferramenta que escreveu a linha em `resumo` (coluna `ferramenta`): `[N8N]` ou `[MAKE]`. O prefixo `[ZAPIER]` não é usado.

**Motivo:** o Zapier só notifica, em duas etapas, e não calcula nada. Marcar o e-mail como `[ZAPIER]` esconderia qual ferramenta fez o cálculo, que é a informação útil para quem lê.

---

## Redesenho do dashboard: só computador, matriz única e indicador corrigido (19/11/2026)

**Decisão:** o dashboard passou a ter uma barra lateral (marca e filtros, sempre visível), uma faixa única de indicadores e uma matriz componente × área que une o antigo Top 10 e o mapa de calor. Não há versão para tablet ou celular (largura mínima de 1280 px).

**Motivo:**
- Os filtros ficavam numa faixa no topo que saía da tela ao rolar, e o texto de apresentação empurrava os indicadores para baixo. A barra lateral mantém o recorte sempre visível, e o texto virou a seção recolhida "Sobre o projeto".
- O Top 10 e o mapa de calor repetiam os totais por componente, e o mapa só mostrava números nas 3 maiores células. A matriz mostra os 12 componentes, o total e o valor de cada área, todos com número.
- O público do dashboard (operação e logística, no computador) não usa tablet ou celular, então manter essas versões só gerava código e testes a mais.

**Indicador corrigido:** "Consumo vs. necessário" (86,7%) somava todo o consumo contra todo o necessário, e os 944 un consumidos a mais compensavam parte das pendências. Passou a se chamar "Necessário já consumido" e usa Σ mín(consumida, necessária) ÷ Σ necessária: 44.995 de 52.976 un, ou 84,9%. O consumo a mais continua no indicador próprio "Consumo acima do necessário".

**Consequências:**
- A marca (logo e ícone) fica em `dashboard/assets/` e é embutida no HTML pelo `scripts/build_dashboard.py`, que remove o bloco de metadados C2PA dos SVG ao embutir. O favicon vem do ícone.
- A origem dos dados (Google Sheets ao vivo ou snapshot) aparece no topo da página, e a falha de leitura é sinalizada com texto, não só com cor.
- As cores do dashboard continuam sem laranja da marca nos gráficos, para não se confundir com as cores de alerta.
