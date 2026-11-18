# Cenário do Make

`blueprint.json` descreve o cenário `alerta-desvio-consumo`:

1. Google Sheets "Search Rows" na aba `ordens` (colunas A a Z, limite 300).
2. Array aggregator com filtro `qtd_pendente_calc` maior que zero (operador numérico). Junta componente e pendência das ordens com pendência.
3. Iterator sobre os componentes distintos.
4. Array aggregator que calcula a soma da pendência por componente (estrutura de dados `soma_por_componente`: componente, soma, texto).
5. Google Sheets "Add a Row" na aba `resumo`, com `ferramenta` = "MAKE", total de pendentes, soma, top 5 (ordenado pela soma, os cinco maiores) e o link do dashboard.

O gatilho é manual (Run once), e o cenário fica inativo. Só um entre n8n e Make deve estar ativo por vez.

Para importar: no Make, crie um cenário, abra o menu "..." e escolha "Import Blueprint". Será preciso refazer a conexão do Google e recriar a estrutura de dados `soma_por_componente` (campos `componente` texto, `soma` número, `texto` texto), porque os identificadores numéricos do blueprint são da conta original.
