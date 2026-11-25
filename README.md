# 🚚 FreteLab — conferência automática de fretes

> **Projeto de demonstração com dados 100% fictícios.** Transportadora, hubs, clientes, rotas e valores são inventados (gerados por script com semente fixa). Nada aqui vem de qualquer empresa real.

Mini-sistema que resolve um problema clássico de faturamento em transporte: **conferir, viagem a viagem, se o valor cobrado bate com a tabela de fretes**, e entregar uma lista clara do que precisa de correção.

## O problema
Em operação de fretes, o valor de cada viagem depende de rota × perfil de veículo. Conferir isso à mão, em planilha, é lento e deixa erro passar: valor acima da tabela, viagem sem ID, rota que nem existe na tabela.

## A solução
| Peça | O que faz |
|---|---|
| [`gerar_dados.py`](gerar_dados.py) | Cria a tabela de fretes (280 tarifas) e 240 viagens, com erros plantados |
| [`tabela/index.html`](tabela/index.html) | Página única: busca por origem/destino, filtro por perfil, ordenação, tema claro/escuro, responsiva |
| [`conferir.py`](conferir.py) | Cruza viagens × tabela e gera o relatório de divergências (`.md` e `.csv`) |

### Regras de conferência (do demo)
1. Viagem **sem ID** não entra no pagamento → pendência.
2. Rota/perfil **sem preço na tabela** → pendência.
3. Valor **acima** da tabela → cobrar correção.
4. Valor **abaixo** da tabela → aceito (não se aponta a favor da empresa).

## Como rodar
Só Python 3 (biblioteca padrão), sem instalar nada:

```bash
python gerar_dados.py     # cria dados/
python conferir.py        # gera relatorio_divergencias.md/.csv
python gerar_tabela.py    # gera tabela/index.html (abra com duplo clique)
```

## Resultado (com os dados do demo)
240 viagens conferidas → **21 pendências**: 15 acima da tabela, 5 sem ID, 1 rota sem tabela. Exemplo em [`relatorio_divergencias.md`](relatorio_divergencias.md).

## Stack
Python (csv, pathlib) · HTML/CSS/JS puro · Markdown

## Próximos passos
- Aceitar CSV/Excel real de entrada
- Histórico de alterações da tabela por vigência
- Relatório em PDF
