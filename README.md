# 💰 Controle Financeiro Pessoal

Sistema simples de linha de comando (CLI) para controlar receitas e despesas pessoais, feito em **Python** com banco de dados **SQLite**.

Este projeto nasceu da minha experiência prática como auxiliar administrativo, trabalhando com faturamento e controle financeiro — a ideia foi aplicar esse conhecimento construindo uma ferramenta própria do zero.

## ✨ Funcionalidades

- Cadastrar receitas e despesas (categoria, valor, data e descrição)
- Listar transações, com filtro por mês e/ou categoria
- Calcular saldo total (receitas − despesas)
- Gerar relatório de totais por categoria
- Remover uma transação pelo ID
- Dados salvos automaticamente em banco de dados SQLite (`financeiro.db`)

## 🛠️ Tecnologias

- Python 3
- SQLite3 (biblioteca nativa do Python — não precisa instalar nada)

## ▶️ Como rodar

Pré-requisito: ter o Python 3 instalado.

```bash
git clone https://github.com/SEU-USUARIO/controle-financeiro-python.git
cd controle-financeiro-python
python main.py
```

Na primeira execução, o arquivo `financeiro.db` é criado automaticamente na mesma pasta.

## 📋 Exemplo de uso
========================================
CONTROLE FINANCEIRO PESSOAL
Adicionar receita/despesa
Listar transações
Ver saldo
Relatório por categoria
Remover transação
Sair
Escolha uma opção: 1
--- Nova transação ---
Tipo (1 = Receita, 2 = Despesa): 1
Categoria (ex: Salário, Alimentação, Transporte): Salário
Valor (ex: 150.50): 3000
Data (AAAA-MM-DD) ou ENTER para hoje:
Descrição (opcional): Salário mensal
✅ Receita de R$ 3000.00 adicionada com sucesso!

## 🚀 Próximas melhorias (ideias para evoluir o projeto)

- [ ] Interface web com Flask
- [ ] Exportar relatórios para CSV/Excel
- [ ] Gráficos de gastos por categoria (matplotlib)
- [ ] Editar uma transação existente
- [ ] Metas de gastos por categoria com alerta

## 👤 Autor

Gustavo Gonçalves Martins — Estudante de Ciência da Computação