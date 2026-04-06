-- ──────────────────────────────────────────────────────────────────────────
-- Verificação de nulos nas colunas críticas
-- ──────────────────────────────────────────────────────────────────────────
SELECT
    SUM(CASE WHEN date    IS NULL THEN 1 ELSE 0 END) AS nulls_date,
    SUM(CASE WHEN account IS NULL THEN 1 ELSE 0 END) AS nulls_account,
    SUM(CASE WHEN value   IS NULL THEN 1 ELSE 0 END) AS nulls_value
FROM financial_statements;


-- ──────────────────────────────────────────────────────────────────────────
-- Contagem de registros por conta — verifica cobertura
-- ──────────────────────────────────────────────────────────────────────────
SELECT
    account,
    COUNT(*)        AS n_periodos,
    MIN(date)       AS periodo_inicial,
    MAX(date)       AS periodo_final,
    MIN(value)      AS valor_min,
    MAX(value)      AS valor_max
FROM financial_statements
GROUP BY account
ORDER BY account;


-- ──────────────────────────────────────────────────────────────────────────
-- Debt Ratio com proteção contra divisão por zero
-- ──────────────────────────────────────────────────────────────────────────
SELECT
    a.date,
    a.value                        AS debt,
    b.value                        AS equity,
    ROUND(a.value * 1.0 / b.value, 4) AS debt_ratio
FROM financial_statements a
JOIN financial_statements b
    ON a.date = b.date
WHERE a.account = 'Empréstimos'
  AND b.account = 'Patrimônio líquido'
  AND b.value != 0
ORDER BY a.date;


-- ──────────────────────────────────────────────────────────────────────────
-- Verificação de anos presentes na série
-- ──────────────────────────────────────────────────────────────────────────
SELECT
    SUBSTR(date, 1, 4) AS ano,
    COUNT(*)           AS n_registros
FROM financial_statements
GROUP BY ano
ORDER BY ano;