# Zap de notificação (Zapier)

O Zapier é só o **notificador**. Ele não agrega, não filtra e não calcula nada: os números já vêm prontos na linha da aba `resumo`, gravada pelo n8n ou pelo Make.

Zap: `alerta-desvio-consumo (resumo para Gmail)`, duas etapas, sempre ligado.

| Etapa | App | Evento | Configuração |
|---|---|---|---|
| 1 | Google Sheets | New Spreadsheet Row | Planilha `alerta-desvio-consumo`, aba `resumo` |
| 2 | Gmail | Send Email | Para: `gutenberg.demo.operacoes@gmail.com` (único destinatário de teste). Tipo do corpo: HTML |

## Assunto
`[<ferramenta>] Alerta de desvio de consumo: <total_pendentes> ordens com pendência`

O prefixo (`[N8N]` ou `[MAKE]`) vem da coluna `ferramenta` da linha. Por isso só uma das duas ferramentas deve estar ativa em cada rodada de teste.

## Corpo (HTML)
Cabeçalho, "Execução em `data_execucao` · via `ferramenta`", dois cartões (Ordens com pendência = `total_pendentes`; Unidades pendentes (necessárias − consumidas) = `soma_pendente`), Top 5 componentes (`top5_componentes`, uma linha por componente via `white-space:pre-line`), botão "Abrir dashboard" (`link_dashboard`) e nota de que os dados são fictícios e o Zapier não agrega nada. Os campos são mapeados direto das colunas, sem etapa de formatação.

## Observações
- Plano: desenhado para o gratuito (100 tarefas/mês, Zaps de duas etapas). Cada linha nova em `resumo` consome 1 tarefa. Na construção a conta estava em teste do plano Pro (expira em 02/12/2026).
- O gatilho detectou a linha gravada por API (n8n) em cerca de 2 minutos. O Zapier pode levar até 15 min.
- **Se apagar linhas da aba `resumo`, desligue e ligue o Zap.** Ele acompanha as linhas pelo número: depois de apagar linhas, a próxima linha nova (com número já visto) não dispara o e-mail. Ao religar o Zap, o gatilho volta a detectar as linhas novas (testado em 18/11/2026).
- Zap antigo da conta ("Alerta desvio de consumo - Gutenberg - pendentes para e-mail") não faz parte deste projeto e não foi alterado.
- Versões publicadas: v1 (texto simples), v2 (HTML), v3 (top 5 em lista).
