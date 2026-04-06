import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "processed" / "petrobras.db"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Abre e retorna conexão com o banco SQLite."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def load_dre(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Carrega DRE na tabela financial_statements."""
    df.to_sql("financial_statements", conn, if_exists="replace", index=False)
    print(f"Tabela 'financial_statements' carregada com {len(df)} registros.")


def load_bpp(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Carrega BPP na tabela balance_sheet."""
    df.to_sql("balance_sheet", conn, if_exists="replace", index=False)
    print(f"Tabela 'balance_sheet' carregada com {len(df)} registros.")


def validate_load(conn: sqlite3.Connection) -> None:
    """Verifica contagens por conta nas duas tabelas."""
    for table in ["financial_statements", "balance_sheet"]:
        query = f"""
        SELECT account, COUNT(*) AS n_periodos
        FROM {table}
        GROUP BY account
        ORDER BY account
        """
        result = pd.read_sql(query, conn)
        print(f"\nTabela '{table}':")
        print(result.to_string(index=False))


def run(df_dre: pd.DataFrame, df_bpp: pd.DataFrame) -> sqlite3.Connection:
    """Executa carga completa e retorna conexão aberta."""
    conn = get_connection()
    load_dre(df_dre, conn)
    load_bpp(df_bpp, conn)
    validate_load(conn)
    return conn


if __name__ == "__main__":
    from extract import run_dre, run_bpp

    df_dre = run_dre()
    df_bpp = run_bpp()
    conn   = run(df_dre, df_bpp)
    conn.close()
    print("\nConexão encerrada.")