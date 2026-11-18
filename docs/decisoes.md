# Decisões do projeto

## Dashboard em HTML no lugar do Looker Studio (18/11/2026)

**Decisão:** o dashboard é uma página HTML (`dashboard/index.html`) publicada no GitHub Pages. O Looker Studio não é usado.

**Motivo:** mais controle sobre o visual e a interação (filtro por área, busca, visão em tabela) e a demo fica junto do código, acessível por link sem instalação.

**Consequências:**
- A página não lê a planilha privada. Ela embute um snapshot de `dados/ordens.csv`, gerado por `scripts/gerar_dashboard.py`. Depois de regenerar os dados, rode o script de novo.
- Para ler a aba `ordens` ao vivo, publique a aba na web como CSV (Arquivo > Compartilhar > Publicar na Web) e coloque o link em `CONFIG.CSV_URL` no `template.html`. A aba passa a ser pública. Os dados são fictícios.
- O dashboard calcula a pendência como `qtd_necessaria − qtd_consumida` na própria página, então não depende da coluna H da planilha.
- O Zapier, o n8n e o Make não mudam. O link do dashboard escrito na aba `resumo` e no e-mail passa a ser o endereço do GitHub Pages.

**Verificação:** os números da página (149 ordens com pendência, soma 7.981, maior pendência 174 em OP-0075, top 10 de componentes e totais por área) foram conferidos contra o cálculo de referência em Python.
