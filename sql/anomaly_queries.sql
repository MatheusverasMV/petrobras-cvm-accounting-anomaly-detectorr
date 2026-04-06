-- ──────────────────────────────────────────────────────────────────────────
-- 14.1 Variação período a período (LAG)
-- Calcula variação absoluta e percentual da receita em relação ao período anterior
-- ──────────────────────────────────────────────────────────────────────────
SELECT
    date,
    value                                                AS receita,
    LAG(value) OVER (ORDER BY date)                      AS receita_anterior,
    ROUND(value - LAG(value) OVER (ORDER BY date), 2)    AS variacao_abs,
    ROUND(
        (value - LAG(value) OVER (ORDER BY date))
        * 100.0 / LAG(value) OVER (ORDER BY date),
        2
    )                                                    AS variacao_pct
FROM financial_statements
WHERE account = 'Receita líquida'
ORDER BY date;


-- ──────────────────────────────────────────────────────────────────────────
-- 14.2 Ranking de períodos por receita (RANK e DENSE_RANK)
-- Ordena períodos do melhor para o pior resultado de receita
-- ──────────────────────────────────────────────────────────────────────────
SELECT
    date,
    value                                              AS receita,
    RANK()       OVER (ORDER BY value DESC)            AS rank_receita,
    DENSE_RANK() OVER (ORDER BY value DESC)            AS dense_rank_receita
FROM financial_statements
WHERE account = 'Receita líquida'
ORDER BY rank_receita;


-- ──────────────────────────────────────────────────────────────────────────
-- 14.3 Receita acumulada corrente (Running Total)
-- Acumula receita período a período usando frame clause
-- ──────────────────────────────────────────────────────────────────────────
SELECT
    date,
    value                                              AS receita,
    ROUND(
        SUM(value) OVER (
            ORDER BY date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    )                                                  AS receita_acumulada
FROM financial_statements
WHERE account = 'Receita líquida'
ORDER BY date;