import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "processed" / "petrobras.db"
TABLE_NAME = "financial_statements"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Abre e retorna conexão com o banco SQLite."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def load(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """Carrega o DataFrame na tabela SQLite, substituindo dados anteriores."""
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    print(f"Tabela '{TABLE_NAME}' carregada com {len(df)} registros.")


def validate_load(conn: sqlite3.Connection) -> None:
    """Verifica se a carga foi bem-sucedida consultando contagens por conta."""
    query = f"""
    SELECT account, COUNT(*) AS n_periodos
    FROM {TABLE_NAME}
    GROUP BY account
    ORDER BY account
    """
    result = pd.read_sql(query, conn)
    print("\nRegistros por conta no banco:")
    print(result.to_string(index=False))


def run(df: pd.DataFrame) -> sqlite3.Connection:
    """Executa carga completa e retorna conexão aberta para uso posterior."""
    conn = get_connection()
    load(df, conn)
    validate_load(conn)
    return conn


if __name__ == "__main__":
    from extract import run as extract
    df_clean = extract()
    conn = run(df_clean)
    conn.close()
    print("Conexão encerrada.")