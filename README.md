# Painel de Vendas Porsche

Painel interativo, em uma única página HTML, sobre 100 vendas de carros Porsche. Ele responde três perguntas de negócio, tem filtros e indicadores de topo, e funciona **offline**: os dados estão dentro do próprio arquivo.

![Visão geral](prints/1-visao-geral.png)

## Como abrir

1. Baixe a pasta e dê **dois cliques em `index.html`**. Ele abre no navegador (Chrome, Edge, Firefox, Safari).
2. Não precisa instalar nada, rodar servidor, Python, Excel ou conexão com a internet.

O arquivo não carrega fontes, bibliotecas nem dados externos. A fonte usada é a do próprio sistema (Segoe UI no Windows, San Francisco no Mac), então a aparência varia levemente de um computador para outro.

## O que o painel mostra

### Indicadores de topo

| Indicador | Como é calculado |
|---|---|
| **Vendas** | Quantidade de vendas no recorte atual |
| **Receita** | Soma dos preços de venda (inclui vendas canceladas) |
| **Ticket médio** | Receita ÷ número de vendas |
| **Receita entregue** | Receita das vendas com status "Entregue" ÷ receita total |

Valores em dólares (US$). Números grandes aparecem abreviados ("US$ 12,83 mi", "US$ 128 mil"); o valor exato aparece embaixo ou ao passar o mouse.

### Pergunta 1: Quais famílias de modelo geram mais receita?

Barras horizontais, uma por família (911, 718, Cayenne, Macan, Panamera, Taycan), ordenadas por receita. Cada linha mostra a receita, a participação no total, o número de vendas e o ticket médio. A frase acima do gráfico aponta a família líder e as de maior e menor ticket.

Sem filtro: a **911** lidera com 33% da receita (23 vendas, ticket médio de US$ 186 mil) e a **Macan** tem o menor ticket (US$ 79 mil).

### Pergunta 2: Como o cliente paga e quanto isso rende?

Mesmo formato, por método de pagamento (9 métodos). A frase destaca o método que concentra mais receita e, entre os métodos com **5 vendas ou mais**, o maior e o menor ticket médio. Métodos com menos de 5 vendas ganham a marca "amostra pequena", porque o ticket médio de 4 vendas não é confiável.

Sem filtro: **Wire Transfer** concentra 31% da receita. Entre os métodos com 5+ vendas, Crypto Payment tem o maior ticket (US$ 181 mil) e Bank Transfer o menor (US$ 90 mil).

### Pergunta 3: Quanto da receita já foi entregue?

Uma barra única dividida em quatro partes, proporcional à receita de cada situação, com a legenda embaixo:

| Situação | Status originais agrupados |
|---|---|
| **Entregue** (verde) | Delivered |
| **A caminho** (azul) | In Transit, Shipped, Awaiting Delivery, Awaiting Pickup |
| **Em análise** (amarelo) | Pending, Pending Approval, Pending Review, Awaiting Review |
| **Cancelada** (vermelho) | Cancelled |

Sem filtro: 40% da receita está entregue, 56% depende de entrega ou análise e 5% foi cancelada.

### Tabela de vendas

No fim da página, a lista das vendas do recorte atual (ID, modelo, ano, cidade, UF, pagamento, entrega e preço). Clique no título de uma coluna para ordenar; clique de novo para inverter.

## Filtros

- **Família do modelo**, **Ano do modelo** e **Método de pagamento**: botões que se combinam. Você pode marcar mais de um por grupo (por exemplo 911 e Taycan). Sem nenhum marcado, vale tudo.
- **Estado**: lista com os 33 estados da base.
- **Limpar filtros** volta tudo ao início. A linha acima dele diz quantas vendas estão sendo mostradas.

Os filtros se combinam entre grupos (família **e** ano **e** pagamento **e** estado). Indicadores, gráficos, frases de conclusão e tabela se atualizam juntos.

Exemplo: família 911 + Wire Transfer deixa 7 vendas, US$ 1,67 mi de receita, ticket médio de US$ 238 mil e só 14% da receita entregue.

![Filtro aplicado](prints/2-filtro-911-wire-transfer.png)

Passe o mouse (ou use a tecla Tab) sobre uma barra ou um trecho da barra de entrega para ver os valores completos. A página se adapta ao celular e segue o tema claro ou escuro do aparelho:

![Celular, tema escuro](prints/3-celular-tema-escuro.png)

## Sobre os dados

A base original tinha 100 vendas e colunas já "sanitizadas". O script `tratamento_base.py` gera `base_tratada.csv`, que é a mesma base embutida no HTML:

- Só as colunas sanitizadas, com preço e ano como números.
- **Família do modelo** e **grupo de status** são colunas criadas aqui (os agrupamentos estão na tabela acima).
- **Preços conferidos** contra o texto original: 94 das 100 linhas batem automaticamente, 4 usavam o formato `$89.750,00` (sanitizado correto) e 2 estavam por extenso (`eighty two thousand USD`, `two hundred thousand USD`), conferidos à mão.
- **Nome do cliente e do vendedor não entram** na base do painel.

### Limites e escolhas

- **"Ano" é o ano do modelo**, não o ano da venda. 24 das 100 datas de venda eram inválidas (como 30 de fevereiro) e 21 estavam no futuro, então a base não sustenta uma análise por tempo.
- **O filtro é por estado, não por cidade**: são 74 cidades para 100 vendas, quase todas com 1 ou 2 registros.
- **A receita inclui vendas canceladas**; a pergunta 3 mostra o quanto isso pesa.
- Com 100 vendas, recortes muito estreitos têm poucos registros. Leia percentuais e tickets com cuidado quando o recorte tiver menos de 5 vendas.

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | O painel. É o único arquivo necessário para usar |
| `base_tratada.csv` | A base tratada, a mesma embutida no HTML (sem nomes) |
| `tratamento_base.py` | Gera o CSV a partir da planilha original (precisa de Python com pandas e openpyxl; só para refazer a base) |
| `prints/` | Capturas de tela usadas neste README |

### Para atualizar os dados

O painel lê os dados da linha `const DATA=[...]` dentro do `index.html`. Para usar uma base nova, gere o CSV com o script e substitua esse bloco pelos novos registros (lista de objetos com `id`, `modelo`, `familia`, `ano`, `preco`, `milhas`, `pagamento`, `cidade`, `estado`, `status_original`, `status`).
