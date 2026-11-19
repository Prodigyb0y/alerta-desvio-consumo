# Alerta de desvio de consumo

Fluxo ponta a ponta que detecta ordens de produção com consumo abaixo do necessário e avisa por e-mail: uma base no Google Sheets, um cálculo de pendências feito por **n8n ou Make**, uma notificação feita pelo **Zapier** e um **dashboard em HTML** com link público.

**Todos os dados são fictícios** (empresa Gutenberg Systems, Áreas A, B e C). O único destinatário de e-mail é um endereço de teste. O projeto não usa LLM nem chamadas de modelo.

- **Demo do dashboard (sem instalação):** https://prodigyb0y.github.io/alerta-desvio-consumo/
- **Repositório:** https://github.com/Prodigyb0y/alerta-desvio-consumo

![Dashboard publicado no GitHub Pages](docs/img/dashboard.png)

## Como funciona

```
dados/ordens.csv ──► Google Sheets, aba "ordens"  (coluna H = D − E)
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
        n8n (manual)                  Make (manual)        nunca os dois ativos
                └─────────────┬─────────────┘
                              ▼
              Google Sheets, aba "resumo"  (1 linha por execução)
                              │  nova linha
                              ▼
                  Zapier (2 etapas, sempre ligado)
                  Sheets "New Spreadsheet Row" ──► Gmail "Send Email"
                              │
                              ▼
                     e-mail HTML [N8N] ou [MAKE]

Dashboard HTML (GitHub Pages) ◄── lê a aba "ordens" publicada como CSV
```

1. **Base:** `scripts/gerar_dados.py` (seed 42) gera 200 ordens com `ordem, area, componente, qtd_necessaria, qtd_consumida, qtd_pendente, email_responsavel`. Na planilha, a coluna H `qtd_pendente_calc` é `qtd_necessaria − qtd_consumida`. Pendente é quando o valor é maior que zero.
2. **Cálculo:** n8n **ou** Make leem `ordens`, filtram `H > 0`, calculam total de ordens com pendência, soma da pendência e os 5 componentes com maior pendência, e gravam uma linha em `resumo` (`data_execucao, ferramenta, total_pendentes, soma_pendente, top5_componentes, link_dashboard`). O gatilho é manual, por ser uma demonstração.
3. **Notificação:** o Zapier detecta a linha nova e envia o e-mail. **Ele não agrega, não filtra e não calcula nada**: só repassa os campos da linha. O assunto leva o prefixo da ferramenta que escreveu a linha (`[N8N]` ou `[MAKE]`).
4. **Dashboard:** página HTML única com indicadores, Top 10 de componentes, pendência por área, faixas de severidade, mapa de calor área × componente e tabela de ordens, com filtros cruzados, tema claro e escuro e visão em tabela de cada gráfico.

## Resultado de referência

Cálculo independente em Python (`python3 scripts/calculo_referencia.py`), igual ao que n8n, Make, e-mail e dashboard mostram:

| Indicador | Valor |
|---|---|
| Linhas / colunas do CSV | 200 / 7 |
| Ordens com pendência (> 0) | 149 |
| Soma da pendência | 7.981 un. |
| Negativas / zeradas | 49 / 2 |
| Top 5 | Válvula solenoide 1205 · Vedação de borracha 966 · Mancal de apoio 904 · Parafuso M8 863 · Rolamento 6204 737 |

O e-mail recebido (execução real, n8n):

![E-mail gerado pelo Zapier a partir da linha do n8n](docs/img/email-n8n.png)

O mesmo resultado vindo do Make (assunto `[MAKE]`): [`docs/img/email-make.png`](docs/img/email-make.png).

## Estrutura do repositório

| Caminho | Conteúdo |
|---|---|
| `dados/ordens.csv` | Base fictícia gerada com seed 42 |
| `scripts/gerar_dados.py` | Gera o CSV |
| `scripts/calculo_referencia.py` | Cálculo de referência (total, soma, top 5) |
| `scripts/build_dashboard.py` | Embute o CSV em `dashboard/template.html` e gera `docs/index.html` |
| `dashboard/template.html` | Modelo do dashboard |
| `n8n/workflow.json` | Fluxo n8n exportado |
| `make/` | Blueprint do cenário Make e como importar |
| `zapier/README.md` | Descrição do Zap (etapas, campos, assunto, corpo) |
| `docs/` | Dashboard publicado, [evidências](docs/evidencias.md), [decisões](docs/decisoes.md), [planos](docs/planos.md) e imagens |

## Como reproduzir

1. `python3 scripts/gerar_dados.py` gera `dados/ordens.csv`.
2. Importe o CSV na aba `ordens` de uma planilha do Google, crie a aba `resumo` com os seis cabeçalhos e a coluna H com a fórmula `=D2-E2`.
3. **n8n:** importe `n8n/workflow.json`, refaça a credencial do Google Sheets e aponte para a sua planilha. **Make:** siga [`make/README.md`](make/README.md). Use só um dos dois por rodada.
4. **Zapier:** crie o Zap descrito em [`zapier/README.md`](zapier/README.md), com o seu endereço de teste.
5. **Dashboard:** publique a aba `ordens` como CSV na web, ajuste `SHEET_CSV_URL` em `dashboard/template.html` e rode `python3 scripts/build_dashboard.py`. Ative o GitHub Pages na pasta `docs/`.

## Decisões e limitações

- **Dashboard em HTML no lugar do Looker Studio**, para ter mais controle e a demo junto do código. Ver [`docs/decisoes.md`](docs/decisoes.md).
- **Gatilho manual** em n8n e Make: é uma demonstração, sem agendamento. Em produção, bastaria trocar por um agendamento diário.
- **Prefixo `[ZAPIER]`:** o assunto usa o prefixo da ferramenta que calculou (`[N8N]` ou `[MAKE]`), porque o Zapier só notifica e nunca aparece como autor do cálculo.
- **Planos gratuitos:** Make com 1.000 créditos/mês e agendamento mínimo de 15 min; Zapier desenhado para 100 tarefas/mês, com Zaps de duas etapas e gatilho "nova linha" que pode levar até 15 min (na construção a conta estava em teste do Pro, até 02/12/2026); n8n Cloud em teste de 14 dias. Por isso o fluxo do n8n está exportado em `n8n/workflow.json`. Detalhes em [`docs/planos.md`](docs/planos.md).
- **Número sem separador de milhar** no e-mail (7981): formatá-lo exigiria uma etapa extra no Zapier, e o Zap tem só duas.
- **Dados publicados:** a aba `ordens` fica pública como CSV para o dashboard ler. É seguro porque os dados são fictícios.
- A aba `resumo` guarda as execuções de teste. Ao apagar linhas dela, desligue e ligue o Zap, senão a próxima linha nova pode não disparar o e-mail (ver `zapier/README.md`).

## Status

- [x] Fase 0: estrutura e planos conferidos
- [x] Fase 1: dados
- [x] Fase 2: dashboard em HTML (GitHub Pages)
- [x] Fase 3: cálculo com n8n
- [x] Fase 4: cálculo com Make
- [x] Fase 5: notificação com Zapier
- [x] Fase 6: README final e organização do repositório
