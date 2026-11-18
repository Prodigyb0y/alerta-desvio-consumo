# Alerta de desvio de consumo

> Rascunho (Fase 0). Será completado ao final do projeto.

Fluxo ponta a ponta para detectar pendências de consumo em ordens de produção: base de ordens, cálculo diário de pendências, notificação por e-mail e dashboard com link público.

**Todos os dados são fictícios.** Empresa fictícia: Gutenberg Systems (Área A, Área B, Área C).

## Arquitetura

1. **Google Sheets, aba `ordens`**: 200 linhas geradas por `scripts/gerar_dados.py` (seed 42). A coluna H `qtd_pendente_calc` = `D − E` (qtd_necessaria − qtd_consumida). Pendente é quando o valor é maior que zero.
2. **Google Sheets, aba `resumo`**: uma linha por execução com `data_execucao`, `ferramenta`, `total_pendentes`, `soma_pendente`, `top5_componentes`, `link_dashboard`.
3. **n8n ou Make** calculam o resumo e escrevem uma linha na aba `resumo`. Nunca os dois ativos ao mesmo tempo.
4. **Zapier** (sempre ligado) é só o notificador, em duas etapas: gatilho "nova linha" na aba `resumo` → Gmail "enviar e-mail". Ele não agrega nada.
5. **Dashboard em HTML** (`dashboard/index.html`), publicado no GitHub Pages. Mostra o total de pendentes, os 10 componentes com maior pendência, a pendência por área e a tabela de ordens. Lê um snapshot de `dados/ordens.csv` embutido na página e, se configurado, o CSV publicado da aba `ordens`.

O assunto de cada e-mail leva o prefixo da ferramenta que escreveu a linha: `[N8N]`, `[MAKE]` ou `[ZAPIER]`.

## Dashboard (HTML)

Página única, sem servidor e sem instalação: [`docs/index.html`](docs/index.html). Ela traz indicadores (ordens com pendência, soma pendente, maior pendência, consumo vs. necessário), Top 10 de componentes, pendência por área, faixas de severidade, mapa de calor área × componente e a tabela de ordens, com filtros por área, componente, situação, pendência mínima e busca por ordem. Clicar num gráfico filtra todos os outros; o recorte fica na URL e pode ser baixado em CSV. Tema claro e escuro, e cada gráfico tem uma visão em tabela.

- Demo pública (GitHub Pages): https://prodigyb0y.github.io/alerta-desvio-consumo/
- Os dados vão embutidos como snapshot. Para ler ao vivo da aba `ordens`, publique a aba como CSV no Google Sheets (Arquivo > Compartilhar > Publicar na web) e cole a URL em `SHEET_CSV_URL` no HTML.
- Para regenerar a página depois de mudar o CSV: `python3 scripts/build_dashboard.py` (usa `dashboard/template.html`).

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `dados/` | CSV gerado |
| `dashboard/` | Template do dashboard HTML |
| `scripts/` | `gerar_dados.py`, `gerar_dashboard.py` e cálculo de referência em Python |
| `dashboard/` | `template.html` e o `index.html` gerado (dashboard) |
| `n8n/` | `workflow.json` exportado |
| `make/` | Blueprint exportado |
| `zapier/` | Descrição do Zap |
| `docs/` | Dashboard publicado (`index.html`), evidências, limitações e decisões |

## Limitações dos planos gratuitos

- Make: 1.000 créditos/mês, 2 cenários ativos, agendamento mínimo de 15 min.
- Zapier: o projeto foi desenhado para o plano gratuito (100 tarefas/mês, Zaps de duas etapas). Na construção, a conta está em teste do plano Pro, que expira em 02/12/2026. O gatilho "nova linha" pode demorar até 15 min.
- n8n: teste gratuito de 14 dias do n8n Cloud, com 1.000 execuções. O fluxo é exportado em `n8n/workflow.json`.

Detalhes em [`docs/planos.md`](docs/planos.md).

## Status

- [x] Fase 0: estrutura do repositório
- [x] Fase 1: dados
- [ ] Fase 2: dashboard em HTML (construído; falta publicar no GitHub Pages)
- [ ] Fase 3: cálculo com n8n
- [ ] Fase 4: cálculo com Make
- [ ] Fase 5: notificação com Zapier
