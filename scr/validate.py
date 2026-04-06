import pandas as pd
import sqlite3
from pathlib import Path

EXPECTED_ACCOUNTS = [
    "Receita líquida",
    "Lucro líquido",
    "Caixa e equivalentes",
    "Empréstimos",
    "Patrimônio líquido"
]

EXPECTED_YEARS = [2023, 2024]


def check_nulls(conn: sqlite3.Connection) -> bool:
    """Verifica se há valores nulos nas colunas críticas."""
    query = """
    SELECT
        SUM(CASE WHEN date    IS NULL THEN 1 ELSE 0 END) AS nulls_date,
        SUM(CASE WHEN account IS NULL THEN 1 ELSE 0 END) AS nulls_account,
        SUM(CASE WHEN value   IS NULL THEN 1 ELSE 0 END) AS nulls_value
    FROM financial_statements
    """
    result = pd.read_sql(query, conn).iloc[0]
    total_nulls = result.sum()

    if total_nulls == 0:
        print("✓ Nulos: nenhum valor nulo encontrado.")
        return True
    else:
        print(f"✗ Nulos: {total_nulls} valor(es) nulo(s) encontrado(s).")
        print(result)
        return False


def check_accounts(conn: sqlite3.Connection) -> bool:
    """Verifica se todas as contas esperadas estão presentes."""
    query = "SELECT DISTINCT account FROM financial_statements"
    found = pd.read_sql(query, conn)["account"].tolist()
    missing = [a for a in EXPECTED_ACCOUNTS if a not in found]

    if not missing:
        print(f"✓ Contas: todas as {len(EXPECTED_ACCOUNTS)} contas esperadas presentes.")
        return True
    else:
        print(f"✗ Contas ausentes: {missing}")
        return False


def check_years(conn: sqlite3.Connection) -> bool:
    """Verifica se os anos esperados estão presentes na série."""
    query = """
    SELECT DISTINCT SUBSTR(date, 1, 4) AS year
    FROM financial_statements
    ORDER BY year
    """
    found = [int(y) for y in pd.read_sql(query, conn)["year"].tolist()]
    missing = [y for y in EXPECTED_YEARS if y not in found]

    if not missing:
        print(f"✓ Anos: {found} — cobertura temporal correta.")
        return True
    else:
        print(f"✗ Anos ausentes: {missing}")
        return False


def check_value_types(conn: sqlite3.Connection) -> bool:
    """Verifica se a coluna value contém apenas números válidos."""
    query = """
    SELECT COUNT(*) AS non_numeric
    FROM financial_statements
    WHERE TYPEOF(value) NOT IN ('integer', 'real')
    """
    non_numeric = pd.read_sql(query, conn).iloc[0, 0]

    if non_numeric == 0:
        print("✓ Tipos: todos os valores são numéricos.")
        return True
    else:
        print(f"✗ Tipos: {non_numeric} valor(es) não numérico(s) encontrado(s).")
        return False


def run(conn: sqlite3.Connection) -> bool:
    """Executa todas as validações e retorna True se aprovado."""
    SEP = "─" * 48
    print(SEP)
    print("  RELATÓRIO DE VALIDAÇÃO — financial_statements")
    print(SEP)

    results = [
        check_nulls(conn),
        check_accounts(conn),
        check_years(conn),
        check_value_types(conn)
    ]

    print(SEP)
    if all(results):
        print("  STATUS FINAL: APROVADO — dados prontos para análise.")
    else:
        n_falhas = results.count(False)
        print(f"  STATUS FINAL: {n_falhas} verificação(ões) falharam.")
    print(SEP)

    return all(results)


if __name__ == "__main__":
    from load_sqlite import get_connection
    from extract import run as extract
    from load_sqlite import run as load

    df_clean = extract()
    conn     = load(df_clean)
    run(conn)
    conn.close()