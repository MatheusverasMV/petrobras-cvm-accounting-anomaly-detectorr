## Como obter os dados brutos

Os arquivos de dados brutos não estão incluídos no repositório por serem
grandes demais. Siga os passos abaixo para baixá-los antes de executar
o projeto.

### 1. Acesse o portal da CVM

https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/

### 2. Baixe os arquivos dos anos 2023 e 2024
dfp_cia_aberta_2023.zip
dfp_cia_aberta_2024.zip

### 3. Extraia e coloque nesta pasta os seguintes arquivos
dfp_cia_aberta_DRE_con_2023.csv
dfp_cia_aberta_DRE_con_2024.csv
dfp_cia_aberta_BPP_con_2023.csv
dfp_cia_aberta_BPP_con_2024.csv

### 4. Una os arquivos por tipo

Execute no terminal dentro desta pasta:

python -c "
import pandas as pd

pd.concat([
    pd.read_csv('dfp_cia_aberta_DRE_con_2023.csv', sep=';', encoding='latin1'),
    pd.read_csv('dfp_cia_aberta_DRE_con_2024.csv', sep=';', encoding='latin1'),
]).to_csv('dfp_cia_aberta_DRE_con.csv', sep=';', index=False, encoding='latin1')

pd.concat([
    pd.read_csv('dfp_cia_aberta_BPP_con_2023.csv', sep=';', encoding='latin1'),
    pd.read_csv('dfp_cia_aberta_BPP_con_2024.csv', sep=';', encoding='latin1'),
]).to_csv('dfp_cia_aberta_BPP_con.csv', sep=';', index=False, encoding='latin1')

print('Arquivos prontos.')
"

### 5. Arquivos finais esperados nesta pasta
dfp_cia_aberta_DRE_con.csv
dfp_cia_aberta_BPP_con.csv

Após isso, execute o notebook normalmente.