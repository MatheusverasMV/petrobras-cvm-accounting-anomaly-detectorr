import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

ANOMALY_THRESHOLD = 0.25
ZSCORE_THRESHOLD  = 2.0
ALERTS_PATH = Path(__file__).parent.parent / "data" / "processed" / "alerts.csv"


def load_revenue(conn: sqlite3.Connection) -> pd.DataFrame:
    """Busca série de receita líquida ordenada por data."""
    query = """
    SELECT date, value
    FROM financial_statements
    WHERE account = 'Receita líquida'
    ORDER BY date
    """
    df = pd.read_sql(query, conn)
    return df.sort_values("date").reset_index(drop=True).copy()


def compute_qoq(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula variação percentual período a período."""
    df["qoq"] = df["value"].pct_change()
    return df


def compute_zscore(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula Z-score da série de receita."""
    df["zscore"] = (df["value"] - df["value"].mean()) / df["value"].std()
    return df


def detect_qoq_alerts(df: pd.DataFrame, threshold: float = ANOMALY_THRESHOLD) -> pd.DataFrame:
    """Retorna períodos com variação QoQ acima do threshold."""
    return df[df["qoq"].abs() > threshold].copy()


def detect_zscore_outliers(df: pd.DataFrame, threshold: float = ZSCORE_THRESHOLD) -> pd.DataFrame:
    """Retorna períodos com Z-score acima do threshold."""
    return df[df["zscore"].abs() > threshold].copy()


def build_radar(alerts: pd.DataFrame, outliers: pd.DataFrame) -> pd.DataFrame:
    """Consolida alertas QoQ e outliers Z-score em uma tabela única."""
    qoq_df = alerts[["date", "value", "qoq"]].copy()
    qoq_df["tipo"] = "QoQ"
    qoq_df = qoq_df.rename(columns={"qoq": "indicador"})

    zscore_df = outliers[["date", "value", "zscore"]].copy()
    zscore_df["tipo"] = "Z-score"
    zscore_df = zscore_df.rename(columns={"zscore": "indicador"})

    return pd.concat([qoq_df, zscore_df], ignore_index=True).sort_values("date")


def export_alerts(radar: pd.DataFrame) -> None:
    """Salva tabela de anomalias em CSV."""
    radar.to_csv(ALERTS_PATH, index=False)
    print(f"Alertas exportados: {len(radar)} evento(s) em {ALERTS_PATH}")


def run(conn: sqlite3.Connection) -> dict:
    """Executa pipeline completo de detecção de anomalias."""
    revenue = load_revenue(conn)
    revenue = compute_qoq(revenue)
    revenue = compute_zscore(revenue)

    alerts   = detect_qoq_alerts(revenue)
    outliers = detect_zscore_outliers(revenue)
    radar    = build_radar(alerts, outliers)

    export_alerts(radar)

    print(f"\nAnomalias QoQ:     {len(alerts)} evento(s)")
    print(f"Outliers Z-score:  {len(outliers)} evento(s)")
    print(f"Total no radar:    {len(radar)} evento(s)")

    return {
        "revenue": revenue,
        "alerts":  alerts,
        "outliers": outliers,
        "radar":   radar
    }


if __name__ == "__main__":
    from load_sqlite import get_connection
    from extract import run as extract
    from load_sqlite import run as load

    df_clean = extract()
    conn     = load(df_clean)
    results  = run(conn)
    conn.close()