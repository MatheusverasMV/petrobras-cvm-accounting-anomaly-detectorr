CREATE TABLE IF NOT EXISTS financial_statements (
    date    TEXT    NOT NULL,
    account TEXT    NOT NULL,
    value   REAL    NOT NULL,
    PRIMARY KEY (date, account)
);