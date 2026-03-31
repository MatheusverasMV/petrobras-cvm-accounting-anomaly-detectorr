# Petrobras Financial Statement Validator

Projeto de portfólio focado em análise de demonstrações financeiras da Petrobras utilizando dados públicos da CVM.

O objetivo é aplicar conceitos de análise de dados, SQL e auditoria contábil para validar consistência financeira e identificar possíveis anomalias nos dados.

---

## Objetivos

- Validar consistência contábil das demonstrações financeiras
- Detectar variações anormais ao longo do tempo
- Realizar consultas analíticas com SQL
- Construir base de dados para visualização no Power BI

---

## Tecnologias utilizadas

- Python (pandas, sqlite3)
- SQL (SQLite)
- Power BI
- Jupyter Notebook

---

## Estrutura do projeto
petrobras-financial-statement-validator/
│
├── data/
│ ├── raw/ # Dados brutos da CVM
│ └── processed/ # Dados tratados e banco SQLite
│
├── notebooks/
│ └── petrobras_analysis.ipynb
│
├── sql/
│ ├── create_tables.sql
│ ├── validation_checks.sql
│ └── anomaly_queries.sql
│
├── src/
│ ├── extract.py
│ ├── load_sqlite.py
│ ├── validate.py
│ └── anomaly.py
│
├── dashboard/
│ ├── petrobras_financial_dashboard.pbix
│ └── dashboard_preview.png
│
├── README.md
└── requirements.txt

## Pipeline do projeto
Dados CVM → Python (ETL) → SQLite → SQL → Notebook → Power BI

## Análises realizadas

### 1. Validação contábil
Verificação da equação patrimonial:

Ativo = Passivo + Patrimônio Líquido

---

### 2. Análise de crescimento
Cálculo de crescimento trimestral (QoQ):
QoQ = (Valor_t - Valor_{t-1}) / Valor_{t-1}
### 3. Indicadores financeiros

- Receita líquida ao longo do tempo
- Lucro líquido
- Debt Ratio (Dívida / Patrimônio Líquido)

---

### 4. Detecção de anomalias

- Variações superiores a 25%
- Outliers utilizando Z-score

---

## Banco de dados

Os dados tratados são armazenados em SQLite na tabela:

`financial_statements`

Campos principais:
- DT_REFER (data)
- DS_CONTA (nome da conta)
- VL_CONTA (valor)

---

## Dashboard (Power BI)

O projeto inclui um dashboard interativo com:

- Evolução da receita
- Relação dívida/patrimônio
- Indicadores financeiros
- Alertas de anomalias

Preview:

![Dashboard](dashboard/dashboard_preview.png)

---

## Principais aprendizados

- Manipulação de dados financeiros reais
- Uso de SQL para análise de dados
- Aplicação de conceitos de auditoria
- Integração entre Python, SQL e Power BI

---

## Autor: Matheus de Araujo Veras

Projeto desenvolvido para portfólio com foco em estágio em dados e auditoria.