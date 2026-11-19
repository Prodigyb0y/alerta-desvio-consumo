# Comparação: n8n × Make × Zapier neste projeto

As três ferramentas rodaram o mesmo fluxo, com os mesmos dados fictícios, em 18/11/2026. Quando um número não foi medido, a célula diz isso.

| Critério | n8n | Make | Zapier |
|---|---|---|---|
| Papel no fluxo | Calcula o resumo: filtra, agrega e grava em `resumo` | Calcula o resumo com a mesma lógica | Envia o e-mail a partir da linha de `resumo`. Não calcula |
| Plano usado | Cloud em teste de 14 dias (1.000 execuções) | Free (1.000 créditos por mês) | Pro em teste até 02/12/2026. O desenho cabe no gratuito: 100 tarefas por mês e Zaps de duas etapas |
| Estrutura | 6 nós, com um nó de código JavaScript | 5 módulos, com agregadores e iterador | 2 etapas: gatilho de nova linha e envio de e-mail |
| Consumo por execução | Não registrado | 5 operações (5 créditos) | 1 tarefa por e-mail enviado |
| Acerto das linhas gravadas | 3 de 3 linhas iguais à referência | 1 de 1 linha igual à referência | Não se aplica: o Zapier não grava dados |
| Duração da execução | Não medida | 0,4 s a 1,1 s (histórico do Make) | Não se aplica |
| Atraso até o e-mail | Não se aplica | Não medido | 2 medições: 2 min 04 s e 2 min 21 s, no plano de teste. No gratuito, o gatilho pode levar até 15 min |
| Problemas encontrados | Formato da data de execução (corrigido no nó de código) | Filtro salvo com texto literal (corrigido); quebra de linha gravada como texto (corrigida); erro na chave do mapeamento do top 5 (corrigido) | Gatilho deixa de detectar linhas depois que linhas da planilha são apagadas; desligar e ligar o Zap resolve |
| Limitação para a demonstração | Teste expira; o fluxo está exportado em JSON | Gatilho manual; créditos limitados por mês | Só notifica; não agrega nem filtra |

**Leitura:** para o cálculo, n8n e Make entregam o mesmo resultado. A escolha entre eles depende de custo de execução e de quanto a equipe já usa cada uma. O Zapier serve para notificar, porque o plano gratuito limita o fluxo a duas etapas.

Metodologia e números de origem: [`resultados.md`](resultados.md) e [`evidencias.md`](evidencias.md).
