import pandas as pd
import numpy as np

caminho_arquivo = r'C:\Users\shenr\Downloads\dados\Excel\Carteira Faker.xlsx'
df = pd.read_excel(caminho_arquivo)

# Remover as colunas indesejadas
colunas_para_remover = ['PESO GAL TOTAL', 'MOLD', 'TP', 'STATUS','QTD CX RESTANTE']
df = df.drop(columns=colunas_para_remover)


# Filtrar os vazios
colunas_para_filtrar = ['MOLDAGEM', 'RENDIMENTO']
df = df.dropna(subset=colunas_para_filtrar)

# Caminho
caminho_arquivo_limpo = r'C:\Users\shenr\Downloads\dados\Excel\Carteira Faker(script limpeza).xlsx'
df.to_excel(caminho_arquivo_limpo, index=False)
print('OK!')