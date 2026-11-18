# Planos das ferramentas (evidência da Fase 0)

Conferido nos painéis de cada ferramenta em 18/11/2026.

| Ferramenta | Plano | Limite | Observação |
|---|---|---|---|
| Make | Free | 1.000 créditos/mês (0 usados) | Renovação em 18/12/2026. 2 cenários ativos, agendamento mínimo de 15 min. |
| Zapier | **Pro, em período de teste** | 1.000 tarefas no teste (1 usada) | O teste expira em 02/12/2026. Depois disso, o plano gratuito tem 100 tarefas/mês e Zaps de duas etapas. |
| n8n Cloud | **Teste de 14 dias** | 1.000 execuções (0 usadas) | Workspace Gutenberg Systems, n8n 3.3.0, online. Teste expira em cerca de 14 dias. |

## Limitações registradas

- **Zapier:** o projeto foi desenhado para caber no plano gratuito (um Zap de duas etapas, 100 tarefas/mês). Durante o teste, o painel mostra o plano Pro. Isso é um período de teste, não o plano gratuito.
- **n8n:** o plano de teste permite executar o fluxo (gatilho manual, poucas execuções). Ao fim do teste, a instância na nuvem pode ser bloqueada. Por isso o fluxo é exportado em `n8n/workflow.json`, e o resultado da execução fica registrado em `docs/`.
- **Make e n8n nunca ficam ativos ao mesmo tempo.** O Zapier notifica as linhas da aba `resumo`, então só uma das duas ferramentas escreve por rodada de teste.
