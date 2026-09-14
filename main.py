"""
Sistema de Controle Financeiro Pessoal
Autor: Gustavo Gonçalves Martins

Um sistema simples de linha de comando para cadastrar receitas e despesas,
calcular saldo e gerar relatórios. Os dados são salvos em um banco de dados
SQLite (financeiro.db), que é criado automaticamente na primeira execução.

Como rodar:
    python main.py
"""

import sqlite3
from datetime import datetime

NOME_BANCO = "financeiro.db"


def conectar():
    """Abre uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(NOME_BANCO)


def criar_tabela():
    """Cria a tabela de transações, caso ainda não exista."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,          -- 'receita' ou 'despesa'
            categoria TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL,          -- formato AAAA-MM-DD
            descricao TEXT
        )
    """)
    conn.commit()
    conn.close()


def validar_data(texto_data):
    """Valida se a data está no formato AAAA-MM-DD. Retorna True/False."""
    try:
        datetime.strptime(texto_data, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def adicionar_transacao():
    """Pede os dados de uma nova receita ou despesa e salva no banco."""
    print("\n--- Nova transação ---")

    tipo = input("Tipo (1 = Receita, 2 = Despesa): ").strip()
    tipo = "receita" if tipo == "1" else "despesa"

    categoria = input("Categoria (ex: Salário, Alimentação, Transporte): ").strip()

    while True:
        valor_texto = input("Valor (ex: 150.50): ").strip().replace(",", ".")
        try:
            valor = abs(float(valor_texto))
            break
        except ValueError:
            print("Valor inválido. Digite apenas números, ex: 150.50")

    while True:
        data = input("Data (AAAA-MM-DD) ou ENTER para hoje: ").strip()
        if data == "":
            data = datetime.today().strftime("%Y-%m-%d")
            break
        if validar_data(data):
            break
        print("Data inválida. Use o formato AAAA-MM-DD, ex: 2026-09-14")

    descricao = input("Descrição (opcional): ").strip()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transacoes (tipo, categoria, valor, data, descricao) VALUES (?, ?, ?, ?, ?)",
        (tipo, categoria, valor, data, descricao)
    )
    conn.commit()
    conn.close()

    print(f"\n✅ {tipo.capitalize()} de R$ {valor:.2f} adicionada com sucesso!")


def listar_transacoes(filtro_mes=None, filtro_categoria=None):
    """Lista as transações, podendo filtrar por mês (AAAA-MM) e/ou categoria."""
    conn = conectar()
    cursor = conn.cursor()

    query = "SELECT id, tipo, categoria, valor, data, descricao FROM transacoes WHERE 1=1"
    parametros = []

    if filtro_mes:
        query += " AND data LIKE ?"
        parametros.append(f"{filtro_mes}%")

    if filtro_categoria:
        query += " AND categoria LIKE ?"
        parametros.append(f"%{filtro_categoria}%")

    query += " ORDER BY data"

    cursor.execute(query, parametros)
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        print("\nNenhuma transação encontrada.")
        return

    print(f"\n{'ID':<4}{'Tipo':<10}{'Categoria':<18}{'Valor':<12}{'Data':<12}Descrição")
    print("-" * 70)
    for row in resultados:
        id_, tipo, categoria, valor, data, descricao = row
        sinal = "+" if tipo == "receita" else "-"
        print(f"{id_:<4}{tipo:<10}{categoria:<18}{sinal}R$ {valor:<8.2f}{data:<12}{descricao or ''}")


def menu_listar():
    """Menu para listar transações com filtros opcionais."""
    print("\n--- Listar transações ---")
    mes = input("Filtrar por mês (AAAA-MM) ou ENTER para todos: ").strip()
    categoria = input("Filtrar por categoria ou ENTER para todas: ").strip()
    listar_transacoes(filtro_mes=mes or None, filtro_categoria=categoria or None)


def calcular_saldo():
    """Calcula e mostra o saldo total, total de receitas e total de despesas."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM transacoes WHERE tipo = 'receita'")
    total_receitas = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM transacoes WHERE tipo = 'despesa'")
    total_despesas = cursor.fetchone()[0]

    conn.close()

    saldo = total_receitas - total_despesas

    print("\n--- Saldo ---")
    print(f"Total de receitas: R$ {total_receitas:.2f}")
    print(f"Total de despesas: R$ {total_despesas:.2f}")
    print(f"Saldo atual:       R$ {saldo:.2f}")


def relatorio_por_categoria():
    """Mostra o total gasto/recebido em cada categoria."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tipo, categoria, SUM(valor)
        FROM transacoes
        GROUP BY tipo, categoria
        ORDER BY tipo, SUM(valor) DESC
    """)
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        print("\nNenhuma transação cadastrada ainda.")
        return

    print("\n--- Relatório por categoria ---")
    tipo_atual = None
    for tipo, categoria, total in resultados:
        if tipo != tipo_atual:
            print(f"\n{tipo.upper()}S:")
            tipo_atual = tipo
        print(f"  {categoria:<20} R$ {total:.2f}")


def remover_transacao():
    """Remove uma transação pelo ID."""
    listar_transacoes()
    id_texto = input("\nDigite o ID da transação que deseja remover: ").strip()

    if not id_texto.isdigit():
        print("ID inválido.")
        return

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_texto,))
    conn.commit()
    linhas_afetadas = cursor.rowcount
    conn.close()

    if linhas_afetadas:
        print("✅ Transação removida com sucesso.")
    else:
        print("Nenhuma transação encontrada com esse ID.")


def exibir_menu():
    print("\n" + "=" * 40)
    print("   CONTROLE FINANCEIRO PESSOAL")
    print("=" * 40)
    print("1. Adicionar receita/despesa")
    print("2. Listar transações")
    print("3. Ver saldo")
    print("4. Relatório por categoria")
    print("5. Remover transação")
    print("0. Sair")


def main():
    criar_tabela()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_transacao()
        elif opcao == "2":
            menu_listar()
        elif opcao == "3":
            calcular_saldo()
        elif opcao == "4":
            relatorio_por_categoria()
        elif opcao == "5":
            remover_transacao()
        elif opcao == "0":
            print("\nAté logo! 👋")
            break
        else:
            print("\nOpção inválida, tente novamente.")


if __name__ == "__main__":
    main()