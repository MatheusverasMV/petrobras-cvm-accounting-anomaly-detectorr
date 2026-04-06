import pandas as pd
from pathlib import Path

RAW_PATH_DRE = Path(__file__).parent.parent / "data" / "raw" / "dfp_cia_aberta_DRE_con.csv"
RAW_PATH_BPP = Path(__file__).parent.parent / "data" / "raw" / "dfp_cia_aberta_BPP_con.csv"

SELECTED_DRE = [
    "Receita de Venda de Bens e/ou Serviços",
    "Lucro/Prejuízo Consolidado do Período",
    "Resultado Bruto",
    "Resultado Financeiro",
    "Resultado Antes dos Tributos sobre o Lucro",
]

SELECTED_BPP = [
    "Empréstimos e Financiamentos",
    "Patrimônio Líquido",
]

YEARS = [2023, 2024]


def load_raw(path: Path) -> pd.DataFrame:
    """Lê CSV bruto da CVM."""
    return pd.read_csv(path, sep=";", encoding="latin1")


def filter_petrobras(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra apenas registros da Petrobras."""
    return df[df["DENOM_CIA"].str.contains("PETROBRAS", case=False, na=False)].copy()


def filter_years(df: pd.DataFrame, years: list = YEARS) -> pd.DataFrame:
    """Filtra pelos anos de análise."""
    df["DT_REFER"] = pd.to_datetime(df["DT_REFER"])
    return df[df["DT_REFER"].dt.year.isin(years)]


def filter_ultimo_exercicio(df: pd.DataFrame) -> pd.DataFrame:
    """Mantém apenas o exercício ÚLTIMO — remove comparativos duplicados."""
    return df[df["ORDEM_EXERC"] == "ÚLTIMO"].copy()


def filter_accounts(df: pd.DataFrame, accounts: list) -> pd.DataFrame:
    """Mantém apenas as contas relevantes."""
    return df[df["DS_CONTA"].isin(accounts)].copy()


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renomeia e converte colunas para nomes padronizados."""
    df = df.rename(columns={
        "DT_REFER": "date",
        "DS_CONTA": "account",
        "VL_CONTA": "value"
    })
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def run_dre() -> pd.DataFrame:
    """Pipeline completo de extração da DRE."""
    df = load_raw(RAW_PATH_DRE)
    df = filter_petrobras(df)
    df = filter_years(df)
    df = filter_ultimo_exercicio(df)
    df = filter_accounts(df, SELECTED_DRE)
    df = standardize_columns(df)
    print(f"DRE extraída: {len(df)} registros, {df['account'].nunique()} contas.")
    return df


def run_bpp() -> pd.DataFrame:
    """Pipeline completo de extração do BPP."""
    df = load_raw(RAW_PATH_BPP)
    df = filter_petrobras(df)
    df = filter_years(df)
    df = filter_ultimo_exercicio(df)
    df = filter_accounts(df, SELECTED_BPP)
    df = standardize_columns(df)
    print(f"BPP extraído: {len(df)} registros, {df['account'].nunique()} contas.")
    return df


if __name__ == "__main__":
    df_dre = run_dre()
    df_bpp = run_bpp()
    print("\nAmostra DRE:")
    print(df_dre[["date", "account", "value"]].head())
    print("\nAmostra BPP:")
    print(df_bpp[["date", "account", "value"]].head())