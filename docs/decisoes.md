# Decisões do projeto

## Dashboard em HTML no lugar do Looker Studio (18/11/2026)

**Decisão:** o dashboard é uma página HTML (`docs/index.html`) publicada no GitHub Pages. O Looker Studio não é usado.

**Motivo:** mais controle sobre o visual e a interação (filtros cruzados, mapa de calor, manual em pop-up, visão em tabela) e a demo fica junto do código, acessível por link sem instalação.

**Ligação com a base:** a página lê a aba `ordens` do Google Sheets pelo CSV publicado na web, configurado em `SHEET_CSV_URL` (`dashboard/template.html`). Se a leitura falhar, usa o snapshot de `dados/ordens.csv` embutido na página. A aba publicada fica pública, e os dados são fictícios.

**Consequências:**
- O dashboard calcula a pendência como `qtd_necessaria − qtd_consumida` na própria página, então não depende da coluna H da planilha.
- A coluna de e-mail não é usada em nenhum gráfico.
- Depois de mudar o CSV ou o template, rode `python3 scripts/build_dashboard.py` para regenerar `docs/index.html`.
- O Zapier, o n8n e o Make não mudam. O link do dashboard escrito na aba `resumo` e no e-mail é o endereço do GitHub Pages.

**Verificação:** os números da página (149 ordens com pendência, soma 7.981, maior pendência 174 em OP-0075, top 10 de componentes e totais por área) foram conferidos contra o cálculo de referência em Python.

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
