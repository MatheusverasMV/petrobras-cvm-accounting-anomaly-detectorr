import sqlite3
import pandas as pd

EXPECTED_DRE_ACCOUNTS = [
    "Receita de Venda de Bens e/ou Serviços",
    "Lucro/Prejuízo Consolidado do Período",
    "Resultado Bruto",
    "Resultado Financeiro",
    "Resultado Antes dos Tributos sobre o Lucro",
]

EXPECTED_BPP_ACCOUNTS = [
    "Empréstimos e Financiamentos",
    "Patrimônio Líquido",
]

EXPECTED_YEARS = [2023, 2024]


def check_nulls(conn: sqlite3.Connection, table: str) -> bool:
    """Verifica se há nulos nas colunas críticas."""
    query = f"""
    SELECT
        SUM(CASE WHEN date    IS NULL THEN 1 ELSE 0 END) AS nulls_date,
        SUM(CASE WHEN account IS NULL THEN 1 ELSE 0 END) AS nulls_account,
        SUM(CASE WHEN value   IS NULL THEN 1 ELSE 0 END) AS nulls_value
    FROM {table}
    """
    result = pd.read_sql(query, conn).iloc[0]
    total  = result.sum()
    if total == 0:
        print(f"✓ [{table}] Nulos: nenhum valor nulo encontrado.")
        return True
    print(f"✗ [{table}] Nulos: {total} valor(es) nulo(s).")
    print(result)
    return False


def check_accounts(conn: sqlite3.Connection, table: str, expected: list) -> bool:
    """Verifica se todas as contas esperadas estão presentes."""
    query  = f"SELECT DISTINCT account FROM {table}"
    found  = pd.read_sql(query, conn)["account"].tolist()
    missing = [a for a in expected if a not in found]
    if not missing:
        print(f"✓ [{table}] Contas: todas as {len(expected)} contas esperadas presentes.")
        return True
    print(f"✗ [{table}] Contas ausentes: {missing}")
    return False


def check_years(conn: sqlite3.Connection, table: str) -> bool:
    """Verifica cobertura temporal."""
    query  = f"SELECT DISTINCT SUBSTR(date, 1, 4) AS year FROM {table} ORDER BY year"
    found  = [int(y) for y in pd.read_sql(query, conn)["year"].tolist()]
    missing = [y for y in EXPECTED_YEARS if y not in found]
    if not missing:
        print(f"✓ [{table}] Anos: {found} — cobertura correta.")
        return True
    print(f"✗ [{table}] Anos ausentes: {missing}")
    return False


def check_value_types(conn: sqlite3.Connection, table: str) -> bool:
    """Verifica se value contém apenas números válidos."""
    query = f"""
    SELECT COUNT(*) AS non_numeric
    FROM {table}
    WHERE TYPEOF(value) NOT IN ('integer', 'real')
    """
    non_numeric = pd.read_sql(query, conn).iloc[0, 0]
    if non_numeric == 0:
        print(f"✓ [{table}] Tipos: todos os valores são numéricos.")
        return True
    print(f"✗ [{table}] Tipos: {non_numeric} valor(es) não numérico(s).")
    return False


def run(conn: sqlite3.Connection) -> bool:
    """Executa todas as validações nas duas tabelas."""
    SEP = "─" * 56
    print(SEP)
    print("  RELATÓRIO DE VALIDAÇÃO")
    print(SEP)

    results = [
        check_nulls(conn, "financial_statements"),
        check_accounts(conn, "financial_statements", EXPECTED_DRE_ACCOUNTS),
        check_years(conn, "financial_statements"),
        check_value_types(conn, "financial_statements"),
        check_nulls(conn, "balance_sheet"),
        check_accounts(conn, "balance_sheet", EXPECTED_BPP_ACCOUNTS),
        check_years(conn, "balance_sheet"),
        check_value_types(conn, "balance_sheet"),
    ]

    print(SEP)
    if all(results):
        print("  STATUS FINAL: APROVADO — dados prontos para análise.")
    else:
        print(f"  STATUS FINAL: {results.count(False)} verificação(ões) falharam.")
    print(SEP)
    return all(results)


if __name__ == "__main__":
    from load_sqlite import get_connection, run as load
    from extract import run_dre, run_bpp

    df_dre = run_dre()
    df_bpp = run_bpp()
    conn   = load(df_dre, df_bpp)
    run(conn)
    conn.close()