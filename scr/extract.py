import pandas as pd
from pathlib import Path

RAW_PATH = Path(__file__).parent.parent / "data" / "raw" / "dfp_cia_aberta_DRE_con.csv"

SELECTED_ACCOUNTS = [
    "Receita líquida",
    "Lucro líquido",
    "Caixa e equivalentes",
    "Empréstimos",
    "Patrimônio líquido"
]

YEARS = [2023, 2024]


def load_raw() -> pd.DataFrame:
    """Lê o CSV bruto da CVM."""
    return pd.read_csv(RAW_PATH, sep=";", encoding="latin1")


def filter_petrobras(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra apenas registros da Petrobras."""
    return df[df["DENOM_CIA"].str.contains("PETROBRAS", case=False, na=False)].copy()


def filter_years(df: pd.DataFrame, years: list = YEARS) -> pd.DataFrame:
    """Filtra pelos anos de análise usando conversão segura para datetime."""
    df["DT_REFER"] = pd.to_datetime(df["DT_REFER"])
    return df[df["DT_REFER"].dt.year.isin(years)]


def filter_accounts(df: pd.DataFrame, accounts: list = SELECTED_ACCOUNTS) -> pd.DataFrame:
    """Mantém apenas as contas relevantes para análise."""
    return df[df["DS_CONTA"].isin(accounts)].copy()


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renomeia colunas para nomes padronizados."""
    return df.rename(columns={
        "DT_REFER": "date",
        "DS_CONTA": "account",
        "VL_CONTA": "value"
    })


def run() -> pd.DataFrame:
    """Executa o pipeline completo de extração e retorna o DataFrame limpo."""
    df = load_raw()
    df = filter_petrobras(df)
    df = filter_years(df)
    df = filter_accounts(df)
    df = standardize_columns(df)
    print(f"Extração concluída: {len(df)} registros, {df['account'].nunique()} contas.")
    return df


if __name__ == "__main__":
    df_clean = run()
    print(df_clean.head())