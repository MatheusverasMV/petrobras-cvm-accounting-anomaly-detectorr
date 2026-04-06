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
- Storytelling executivo em notebook

---

## Pipeline
dados brutos (CVM)
↓
tratamento e padronização
↓
persistência em SQLite
↓
análise SQL (JOIN, LAG, RANK, Running Total)
↓
detecção de anomalias (QoQ + Z-score)
↓
executive dashboard (KPI panel + gráficos)
↓
exportação dos dados processados
---

## Estrutura do notebook

| Seção | Conteúdo |
|-------|----------|
| 1–3   | Leitura, filtragem e padronização dos dados da CVM |
| 4     | Persistência em banco SQLite |
| 5–6   | Queries SQL: receita e debt ratio com JOIN |
| 7     | Visualizações da receita e risco |
| 8–9   | Variação QoQ e alertas automáticos |
| 10    | Detecção de outliers com Z-score |
| 11    | Exportação dos datasets processados |
| 12    | Conclusão |
| 13    | Executive Dashboard — KPI panel, gráficos 2×2, radar de anomalias e insights |
| 14    | SQL Analytics Avançado — LAG, RANK, DENSE_RANK, Running Total |
![Dashboard](data/processed/dashboard.png)

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

## SQL avançado

A seção 14 demonstra o uso de window functions diretamente no SQLite,
sem transformações externas em pandas:
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
por tipo de alerta na seção 13.3.

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

## Estrutura do repositório
petrobras-financial-validator/
├── data/
│   ├── raw/
│   │   └── dfp_cia_aberta_DRE_con.csv
│   └── processed/
│       ├── petrobras.db
│       ├── final_data.csv
│       ├── revenue_analysis.csv
│       ├── alerts.csv
│       └── dashboard.png
├── notebooks/
│   └── petrobras_financial_validator.ipynb
├── requirements.txt
└── README.md
---

## Como executar
```bash
# 1. Clone o repositório
git clone https://github.com/MatheusverasMV/petrobras-financial-validator.git
cd petrobras-financial-validator

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Baixe os dados da CVM e coloque em data/raw/

# 4. Execute o notebook
jupyter notebook notebooks/petrobras_financial_validator.ipynb
```

---

## requirements.txt
pandas
matplotlib
jupyter

---

## Autor

Desenvolvido como projeto de portfólio para vagas de estágio em
dados, BI e análise financeira.