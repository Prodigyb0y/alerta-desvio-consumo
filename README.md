# Alerta de desvio de consumo

Fluxo ponta a ponta que detecta ordens de produção com consumo abaixo do necessário e avisa por e-mail: uma base no Google Sheets, um cálculo de pendências feito por **n8n ou Make**, uma notificação feita pelo **Zapier** e um **dashboard em HTML** com link público.

**Todos os dados são fictícios** (empresa Gutenberg Systems, Áreas A, B e C). O único destinatário de e-mail é um endereço de teste. O projeto não usa LLM nem chamadas de modelo.

- **Demo do dashboard (sem instalação):** https://prodigyb0y.github.io/alerta-desvio-consumo/

![Dashboard publicado no GitHub Pages](docs/img/dashboard.png)

## Tecnologias

| Camada | Tecnologia | Papel |
|---|---|---|
| Base de dados | Google Sheets | Abas `ordens` (200 linhas) e `resumo` (uma linha por execução) |
| Geração de dados | Python 3 (biblioteca padrão) | `gerar_dados.py` (seed 42), cálculo de referência e build do dashboard |
| Automação (cálculo) | n8n Cloud | Lê `ordens`, filtra, agrega e grava em `resumo` |
| Automação (cálculo) | Make | Mesmo cálculo, como alternativa ao n8n |
| Notificação | Zapier + Gmail | Zap de duas etapas: nova linha em `resumo` → e-mail HTML |
| Dashboard | HTML, CSS e JavaScript puros | Página única, publicada no GitHub Pages |
| Hospedagem e versionamento | GitHub e GitHub Pages | Repositório público e demo acessível por link |

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

1. **Base:** 200 ordens com `ordem, area, componente, qtd_necessaria, qtd_consumida, qtd_pendente, email_responsavel`. Na planilha, a coluna H `qtd_pendente_calc` é `qtd_necessaria − qtd_consumida`. Pendente é quando o valor é maior que zero.
2. **Cálculo:** n8n **ou** Make leem `ordens`, filtram `H > 0` e gravam uma linha em `resumo` com `data_execucao, ferramenta, total_pendentes, soma_pendente, top5_componentes, link_dashboard`. O gatilho é manual, por ser uma demonstração.
3. **Notificação:** o Zapier detecta a linha nova e envia o e-mail. Ele não agrega, não filtra e não calcula nada: só repassa os campos da linha. O assunto leva o prefixo da ferramenta que calculou (`[N8N]` ou `[MAKE]`).
4. **Dashboard:** indicadores, Top 10 de componentes, pendência por área, mapa de calor área × componente e tabela de ordens, com filtros cruzados, tema claro e escuro e visão em tabela de cada gráfico.

## Resultado de referência

Cálculo independente em Python (`python3 scripts/calculo_referencia.py`), igual ao que n8n, Make, e-mail e dashboard mostram:

| Indicador | Valor |
|---|---|
| Ordens com pendência (> 0) | 149 de 200 |
| Soma da pendência | 7.981 un. |
| Top 5 | Válvula solenoide 1205 · Vedação de borracha 966 · Mancal de apoio 904 · Parafuso M8 863 · Rolamento 6204 737 |

E-mail recebido numa execução real (n8n):

![E-mail gerado pelo Zapier a partir da linha do n8n](docs/img/email-n8n.png)

## Resultados medidos

| Medida | Resultado | Como foi medida |
|---|---|---|
| Acerto das linhas gravadas em `resumo` | 4 de 4 linhas atuais iguais à referência (149 pendentes, 7.981 un., mesmo top 5): 3 do n8n e 1 do Make | Comparação linha a linha com `scripts/calculo_referencia.py` |
| E-mails disparados pelas linhas atuais | 3 de 4. A linha de 21:33 não disparou (ver Limitações) | Conferência da caixa de teste contra a aba `resumo` |
| Atraso entre a linha gravada e o e-mail | 2 medições: cerca de 2 min 04 s e 2 min 21 s | Horário gravado na linha de `resumo` vs. horário da execução no histórico do Zapier |
| Execuções do cenário Make | 7 no histórico: 6 com sucesso e 1 com erro, já corrigido (chave `{empty}` no mapeamento do top 5) | Histórico de execuções do Make |
| Duração de cada execução do Make | 0,4 s a 1,1 s | Duração registrada no histórico do Make |
| Tempo do processo manual | Não medido. Há apenas uma estimativa do autor, de 3 a 10 minutos por pessoa | Não se aplica |

**Por que isso importa para um time de negócio:** em vez de montar o recorte à mão, quem acompanha os desvios recebe, a cada execução, o total de ordens com consumo abaixo do necessário, o volume pendente e os componentes que mais pesam, com link para o dashboard.

## Estrutura do repositório

| Caminho | Conteúdo |
|---|---|
| `dados/` | `ordens.csv`, a base fictícia |
| `scripts/` | Geração dos dados, cálculo de referência e build do dashboard |
| `dashboard/` | `template.html`, o modelo do dashboard |
| `n8n/` | `workflow.json`, o fluxo exportado |
| `make/` | Blueprint do cenário Make e como importar |
| `zapier/` | Descrição do Zap (etapas, campos, assunto e corpo) |
| `docs/` | Dashboard publicado, [evidências](docs/evidencias.md), [decisões](docs/decisoes.md), [planos](docs/planos.md) e imagens |

## Como reproduzir

1. `python3 scripts/gerar_dados.py` gera `dados/ordens.csv`.
2. Importe o CSV na aba `ordens` de uma planilha do Google, crie a aba `resumo` com os seis cabeçalhos e a coluna H com a fórmula `=D2-E2`.
3. **n8n:** importe `n8n/workflow.json` e refaça a credencial do Google Sheets. **Make:** siga [`make/README.md`](make/README.md). Use só um dos dois por rodada.
4. **Zapier:** crie o Zap descrito em [`zapier/README.md`](zapier/README.md), com o seu endereço de teste.
5. **Dashboard:** publique a aba `ordens` como CSV na web, ajuste `SHEET_CSV_URL` em `dashboard/template.html`, rode `python3 scripts/build_dashboard.py` e ative o GitHub Pages na pasta `docs/`.

## Limitações

- **Planos gratuitos:** Make com 1.000 créditos/mês; Zapier desenhado para 100 tarefas/mês e Zaps de duas etapas (o gatilho pode levar até 15 min); n8n Cloud em teste de 14 dias, por isso o fluxo está exportado em `n8n/workflow.json`. Detalhes em [`docs/planos.md`](docs/planos.md).
- **Gatilho manual:** não há agendamento. Em produção, bastaria um agendamento diário.
- **Aba `resumo`:** ao apagar linhas dela, desligue e ligue o Zap, senão a próxima linha nova pode não disparar o e-mail (ver [`zapier/README.md`](zapier/README.md)).
- **Amostra pequena:** 4 linhas em `resumo` e 2 medições de atraso. Os números acima servem para validar o fluxo, não para estimar desempenho.
- **Dados públicos:** a aba `ordens` é publicada como CSV para o dashboard ler. É seguro porque os dados são fictícios.

Decisões de projeto (por que HTML no lugar do Looker Studio, gatilho manual e prefixo do assunto) em [`docs/decisoes.md`](docs/decisoes.md).
