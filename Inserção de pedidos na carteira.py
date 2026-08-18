import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

def processar_e_expandir_producao(caminho_entrada, caminho_saida, novos_pedidos=500):
    df = pd.read_excel(caminho_entrada)
    fake = Faker('pt_BR')
      
    # Cria um catálogo único de produtos baseados no CÓD.BM existente
    colunas_produto = ["CÓD.BM", "DESCRIÇÃO", "MOLDAGEM", "Material", "Peso Galhada", "Peso Pç", "PÇ PLACA", "RENDIMENTO"]
    df_catalogo_produtos = df[colunas_produto].drop_duplicates(subset=["CÓD.BM"]).dropna(subset=["CÓD.BM"])
    
    # Cria um catálogo de clientes
    colunas_cliente = ["CÓD.TER", "CLIENTE"]
    df_catalogo_clientes = df[colunas_cliente].drop_duplicates(subset=["CÓD.TER"]).dropna(subset=["CÓD.TER"])
    
    # Gerar 500 novos pedidos
    novas_linhas = []
    
    for _ in range(novos_pedidos):
        # Sorteia um produto e um cliente do catálogo original
        prod_sorteado = df_catalogo_produtos.sample(1).iloc[0]
        cli_sorteado = df_catalogo_clientes.sample(1).iloc[0]
        
        # Cria a nova linha respeitando a amarração
        nova_linha = {
            "CÓD.BM": prod_sorteado["CÓD.BM"],
            "DESCRIÇÃO": prod_sorteado["DESCRIÇÃO"],
            "MOLDAGEM": prod_sorteado["MOLDAGEM"],
            "Material": prod_sorteado["Material"],
            "Peso Galhada": prod_sorteado["Peso Galhada"],
            "Peso Pç": prod_sorteado["Peso Pç"],
            "PÇ PLACA": prod_sorteado["PÇ PLACA"],
            "RENDIMENTO": prod_sorteado["RENDIMENTO"],
            "CÓD.TER": cli_sorteado["CÓD.TER"],
            "CLIENTE": cli_sorteado["CLIENTE"]
        }
        novas_linhas.append(nova_linha)
        
    df_novos = pd.DataFrame(novas_linhas)

    df_completo = pd.concat([df, df_novos], ignore_index=True)
    
    # PED.BM sequencial, PED.CLIENTE aleatório
    numero_inicial_op = 10001
    numero_inicial_ped_bm = 50001
    
    df_completo['OP'] = range(numero_inicial_op, numero_inicial_op + len(df_completo))
    df_completo['PED.BM'] = range(numero_inicial_ped_bm, numero_inicial_ped_bm + len(df_completo))
    df_completo['PED.CLIENTE'] = [fake.bothify(text='CLI-#####') for _ in range(len(df_completo))]
    
    # Emissão OP: data aleatória este ano. Entrega: Pelo menos +20 dias, limite de 365.
    data_hoje = datetime.now()
    inicio_ano = datetime(data_hoje.year, 1, 1)
    
    def gerar_datas(row):
        emissao = fake.date_between(start_date=inicio_ano, end_date=data_hoje.date())
        dias_para_entrega = random.randint(20, 300)
        entrega = emissao + timedelta(days=dias_para_entrega)
        
        # Garante que a data de entrega caia em dia útil (segunda a sexta)
        if entrega.weekday() == 5:    # Sábado -> avança 2 dias para Segunda
            entrega += timedelta(days=2)
        elif entrega.weekday() == 6:  # Domingo -> avança 1 dia para Segunda
            entrega += timedelta(days=1)
            
        return pd.Series([emissao, entrega])
        
    df_completo[['EMISSÃO OP', 'ENTREGA']] = df_completo.apply(gerar_datas, axis=1)
       
    # Quantidade aleatória por OP ("PEÇAS PEDIDO")
    df_completo['PEÇAS PEDIDO'] = [random.randint(100, 5000) for _ in range(len(df_completo))]
    
    # Garante que os números usados na matemática sejam float/int, substituindo vazios/erros
    df_completo['PÇ PLACA'] = pd.to_numeric(df_completo['PÇ PLACA'], errors='coerce').fillna(1)
    df_completo['Peso Pç'] = pd.to_numeric(df_completo['Peso Pç'], errors='coerce').fillna(0)
    
    # QTD CX PED = Teto (PEÇAS PEDIDO / PÇ PLACA)
    df_completo['QTD CX PED'] = np.ceil(df_completo['PEÇAS PEDIDO'] / df_completo['PÇ PLACA'])
    
    # Simulação de Produção (para alimentar as lógicas seguintes)
    def simular_qtd_prod(qtd_ped):
        cenario = random.choice(['TOTAL', 'PARCIAL', 'VAZIO'])
        if cenario == 'TOTAL':
            return qtd_ped
        elif cenario == 'PARCIAL':
            # Produziu pelo menos 1, e no máximo o total - 1
            max_parcial = max(1, int(qtd_ped) - 1)
            return random.randint(1, max_parcial)
        else:
            return np.nan # Simula vazio (NÃO PRODUZIDO)
            
    df_completo['QTD CX PROD'] = df_completo['QTD CX PED'].apply(simular_qtd_prod)
    
    # PEÇAS VAZADAS = QTD CX PROD * PÇ PLACA (vazios tratados como 0 no cálculo)
    df_completo['PEÇAS VAZADAS'] = df_completo['QTD CX PROD'].fillna(0) * df_completo['PÇ PLACA']
    
    # PESO PEÇA TOTAL = PEÇAS PEDIDO * Peso Pç
    df_completo['PESO PEÇA TOTAL'] = df_completo['PEÇAS PEDIDO'] * df_completo['Peso Pç']
    
    # STATUS PROD
    def definir_status(row):
        qtd_prod = row['QTD CX PROD']
        qtd_ped = row['QTD CX PED']
        
        if pd.isna(qtd_prod) or qtd_prod == 0:
            return "NÃO PRODUZIDO"
        elif qtd_prod == qtd_ped:
            return "PRODUZIDO TOTAL"
        else:
            return "PRODUZIDO PARCIAL"
            
    df_completo['STATUS PROD'] = df_completo.apply(definir_status, axis=1)

    # Inserir novas colunas
    df_completo['PESO GALHADA TOTAL PED'] = df_completo['QTD CX PED'] * df_completo['Peso Galhada']
    df_completo['PESO GALHADA TOTAL PROD'] = df_completo['QTD CX PROD'] * df_completo['Peso Galhada']
    df_completo['PESO PEÇA TOTAL PROD'] = df_completo['PEÇAS VAZADAS'] * df_completo['Peso Pç']
    df_completo['PESO EXCLUSIVO GALHADA'] = df_completo['Peso Galhada'] - (df_completo['PÇ PLACA'] * df_completo['Peso Pç'])
    df_completo['PESO TOTAL E. GALHADA PED'] = df_completo['PESO EXCLUSIVO GALHADA']  * df_completo['QTD CX PED']
    df_completo['PESO TOTAL E. GALHADA PROD'] = df_completo['PESO EXCLUSIVO GALHADA']  * df_completo['QTD CX PROD']

    novos_nomes_colunas ={
        'QTD CX PROD': 'QTD CAIXAS PROD',
        'QTD CX PED': 'QTD CAIXAS PED',
        'Peso Pç': 'PESO PEÇA',
        'PED.BM ':'PEDIDO INTERNO',
        'CÓD.BM': 'CÓDIGO ITEM',
        'PED.CLIENTE': 'PEDIDO CLIENTE',
        'STATUS PROD': 'STATUS PRODUÇÃO',
        'CÓD.TER':'CADASTRO CLIENTE',
        'Material': 'MATERIAL',
        'Peso Galhada':  'PESO GALHADA',
        'Peso Pç': 'PESO PEÇA',
        'PÇ PLACA': 'EMPLACAMENTO',
        'EMISSAO OP': 'EMISSÃO'
    }
    df_completo.rename(columns=novos_nomes_colunas, inplace=True)

    df_completo.to_excel(caminho_saida, index=False)

# CAMINHOS
arquivo_original = r'C:\Users\shenr\Downloads\dados\Excel\Carteira Faker(script limpeza).xlsx' 
arquivo_novo = r'C:\Users\shenr\Downloads\dados\Excel\Carteira Faker(script limpeza + aleatorio).xlsx'

processar_e_expandir_producao(arquivo_original, arquivo_novo, novos_pedidos=500)
print("OK!")