# Alerta de desvio de consumo

> Rascunho (Fase 0). Será completado ao final do projeto.

Fluxo ponta a ponta para detectar pendências de consumo em ordens de produção: base de ordens, cálculo diário de pendências, notificação por e-mail e dashboard com link público.

**Todos os dados são fictícios.** Empresa fictícia: Gutenberg Systems (Área A, Área B, Área C).

## Arquitetura

1. **Google Sheets, aba `ordens`**: 200 linhas geradas por `scripts/gerar_dados.py` (seed 42). A coluna H `qtd_pendente_calc` = `D − E` (qtd_necessaria − qtd_consumida). Pendente é quando o valor é maior que zero.
2. **Google Sheets, aba `resumo`**: uma linha por execução com `data_execucao`, `ferramenta`, `total_pendentes`, `soma_pendente`, `top5_componentes`, `link_dashboard`.
3. **n8n ou Make** calculam o resumo e escrevem uma linha na aba `resumo`. Nunca os dois ativos ao mesmo tempo.
4. **Zapier** (sempre ligado) é só o notificador, em duas etapas: gatilho "nova linha" na aba `resumo` → Gmail "enviar e-mail". Ele não agrega nada.
5. **Looker Studio** conectado à aba `ordens`.

O assunto de cada e-mail leva o prefixo da ferramenta que escreveu a linha: `[N8N]`, `[MAKE]` ou `[ZAPIER]`.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `dados/` | CSV gerado |
| `scripts/` | `gerar_dados.py` e cálculo de referência em Python |
| `n8n/` | `workflow.json` exportado |
| `make/` | Blueprint exportado |
| `zapier/` | Descrição do Zap |
| `docs/` | Evidências, limitações e decisões |

## Limitações dos planos gratuitos

- Make: 1.000 créditos/mês, 2 cenários ativos, agendamento mínimo de 15 min.
- Zapier: o projeto foi desenhado para o plano gratuito (100 tarefas/mês, Zaps de duas etapas). Na construção, a conta está em teste do plano Pro, que expira em 02/12/2026. O gatilho "nova linha" pode demorar até 15 min.
- n8n: teste gratuito de 14 dias do n8n Cloud, com 1.000 execuções. O fluxo é exportado em `n8n/workflow.json`.

Detalhes em [`docs/planos.md`](docs/planos.md).

## Status

- [x] Fase 0: estrutura do repositório
- [ ] Fase 1: dados
- [ ] Fase 2: dashboard
- [ ] Fase 3: cálculo com n8n
- [ ] Fase 4: cálculo com Make
- [ ] Fase 5: notificação com Zapier
