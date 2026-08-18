import pandas as pd
from faker import Faker

def anonimizar_planilha_faker(caminho_arquivo_entrada, caminho_arquivo_saida):
    nome_da_aba = 'Tabela_Consulta_de_Sql2000'
    df = pd.read_excel(caminho_arquivo_entrada, sheet_name=nome_da_aba)
    df.columns = df.columns.str.strip()
    
    fake = Faker('pt_BR')
    Faker.seed(42) 

    # Clientes
    codigos_clientes = df['CÓD.TER'].dropna().unique()
    mapa_clientes = {codigo: fake.company() for codigo in codigos_clientes}
    # Substitui a coluna 'CLIENTE' usando o mapa
    df['CLIENTE'] = df['CÓD.TER'].map(mapa_clientes)

    # Produtos
    codigos_produtos = df['CÓD.BM'].dropna().unique()
    mapa_produtos = {
        codigo: f"PEÇA {fake.word().upper()} {fake.bothify(text='??-####').upper()}" 
        for codigo in codigos_produtos
        }
    # Substitui a coluna 'DESCRIÇÃO' usando o mapa
    df['DESCRIÇÃO'] = df['CÓD.BM'].map(mapa_produtos)

    # Salva o resultado em um novo arquivo Excel
    df.to_excel(caminho_arquivo_saida, index=False)
    
# Caminhos
arquivo_original = r'C:\Users\shenr\Downloads\dados\Excel\Carteira BEMA ST-08.xlsx' 
arquivo_novo = r'C:\Users\shenr\Downloads\dados\Excel\Carteira Faker.xlsx'


anonimizar_planilha_faker(arquivo_original, arquivo_novo)
print('OK!')