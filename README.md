# Petrobras Financial Statement Validator

Análise das demonstrações financeiras da Petrobras com dados públicos da CVM,
aplicando Python, SQL e técnicas de auditoria contábil para validar consistência,
calcular KPIs financeiros e detectar anomalias trimestrais.

---

## Visão geral

Este projeto replica processos comuns em análise financeira e auditoria de dados,
cobrindo o pipeline completo desde a ingestão dos dados brutos até a geração de
um painel executivo com insights dinâmicos.

Desenvolvido como projeto de portfólio para demonstrar habilidades em:
- Análise e tratamento de dados financeiros reais
- SQL intermediário e avançado (window functions)
- Detecção estatística de anomalias
- Pipeline modular com separação entre extração, carga e validação
- Storytelling executivo em notebook

---

## Dashboard

![Dashboard](dashboard/executive_dashboard_preview.png)

---

## Pipeline
dados brutos (CVM)
↓
extract.py — leitura, filtro e padronização
↓
load_sqlite.py — persistência em SQLite
↓
validate.py — checagem de consistência automática
↓
anomaly.py — detecção QoQ e Z-score
↓
notebook — SQL analytics, dashboard executivo e insights
↓
data/processed/ — CSVs e PNG exportados

---

## Estrutura do repositório
petrobras-cvm-accounting/
├── dashboard/
│   └── executive_dashboard_preview.png
├── data/
│   ├── raw/
│   │   └── COMO_BAIXAR.md
│   └── processed/
│       ├── alerts.csv
│       ├── final_data.csv
│       ├── revenue_analysis.csv
│       └── petrobras.db
├── notebooks/
│   └── petrobras_analysis.ipynb
├── scr/
│   ├── extract.py
│   ├── load_sqlite.py
│   ├── anomaly.py
│   └── validate.py
├── sql/
│   ├── create_tables.sql
│   ├── anomaly_queries.sql
│   └── validation_checks.sql
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

---

## Estrutura do notebook

| Seção | Conteúdo |
|-------|----------|
| 1–3 | Leitura, filtragem e padronização dos dados da CVM |
| 4 | Persistência em banco SQLite |
| 5–6 | Queries SQL: receita e debt ratio com JOIN |
| 7 | Visualizações da receita e risco |
| 8–9 | Variação QoQ e alertas automáticos |
| 10 | Detecção de outliers com Z-score |
| 11 | Exportação dos datasets processados |
| 12 | Conclusão |
| 13 | Executive Dashboard — KPI panel, gráficos 2×2, radar de anomalias e insights |
| 14 | SQL Analytics Avançado — LAG, RANK, DENSE_RANK, Running Total |

---

## KPIs analisados

- Receita líquida
- Lucro líquido
- Margem líquida (Lucro / Receita)
- Debt Ratio (Empréstimos / Patrimônio Líquido)
- Variação QoQ trimestral
- Z-score da receita
- Receita acumulada corrente (Running Total)

---

## SQL 

A seção 14 e os arquivos em `sql/` demonstram o uso de window functions
diretamente no SQLite, sem transformações externas em pandas:
```sql
-- LAG: variação período a período
LAG(value) OVER (ORDER BY date)

-- RANK e DENSE_RANK: ranking de períodos por receita
RANK() OVER (ORDER BY value DESC)

-- Running Total: receita acumulada corrente
SUM(value) OVER (
    ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

---

## Detecção de anomalias

Dois métodos independentes são aplicados à série de receita líquida:

**QoQ (variação trimestral):** variações superiores a 25% entre períodos
consecutivos são sinalizadas automaticamente.

**Z-score:** valores além de ±2 desvios padrão da média histórica
são marcados como outliers estatísticos.

Os resultados são consolidados em um radar de anomalias com highlight
por tipo de alerta na seção 13.3 do notebook.

---

## Validação automática

O módulo `scr/validate.py` executa quatro verificações automáticas
antes de qualquer análise:

- Ausência de nulos nas colunas críticas
- Presença de todas as contas esperadas
- Cobertura temporal correta (2023–2024)
- Tipos numéricos válidos na coluna de valores

---

## Stack

| Ferramenta | Uso |
|------------|-----|
| Python 3.x | linguagem principal |
| pandas | tratamento e análise de dados |
| SQLite + sqlite3 | persistência e queries SQL |
| matplotlib | visualizações |
| Jupyter Notebook | ambiente de desenvolvimento |

---

## Fonte dos dados

Dados públicos disponibilizados pela CVM (Comissão de Valores Mobiliários)
no portal de dados abertos:

[https://dados.cvm.gov.br](https://dados.cvm.gov.br)

Arquivo utilizado: `dfp_cia_aberta_DRE_con.csv`
Período analisado: 2023–2024

---

## Como executar
```bash
# 1. Clone o repositório
git clone https://github.com/MatheusverasMV/petrobras-cvm-accounting.git
cd petrobras-cvm-accounting

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Baixe os dados da CVM
# Siga as instruções em data/raw/COMO_BAIXAR.md

# 4. Execute o pipeline modular (opcional)
python scr/extract.py
python scr/load_sqlite.py
python scr/validate.py
python scr/anomaly.py

# 5. Ou execute diretamente pelo notebook
jupyter notebook notebooks/petrobras_analysis.ipynb
```

---

## requirements.txt
pandas
matplotlib
jupyter

## Autor

Desenvolvido como projeto de portfólio para vagas de estágio em
dados, BI e análise financeira.