import pandas as pd

# 1. Carregar o seu arquivo parquet
df = pd.read_parquet('nomes_corrigidos.parquet')

# 2. Carregar a tabela de referência de municípios (IBGE)
url_ibge = "https://raw.githubusercontent.com/kelvins/municipios-brasileiros/main/csv/municipios.csv"
df_ibge = pd.read_csv(url_ibge)

# 3. Ajustar os códigos para o cruzamento (6 dígitos)
df_ibge['codigo_6'] = df_ibge['codigo_ibge'].astype(str).str[:6]
df['COD_MUNICIPIO_OBITO'] = df['COD_MUNICIPIO_OBITO'].astype(str)

# 4. Cruzar os dados para obter nomes dos municípios e códigos de UF
df = pd.merge(
    df, 
    df_ibge[['codigo_6', 'nome', 'codigo_uf']], 
    left_on='COD_MUNICIPIO_OBITO', 
    right_on='codigo_6', 
    how='left'
)

# 5. Mapear códigos de UF para siglas
mapa_ufs = {
    11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO',
    21: 'MA', 22: 'PI', 23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL',
    28: 'SE', 29: 'BA', 31: 'MG', 32: 'ES', 33: 'RJ', 35: 'SP', 41: 'PR',
    42: 'SC', 43: 'RS', 50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF'
}
df['UF_SIGLA'] = df['codigo_uf'].map(mapa_ufs)

# 6. Criar a nova coluna MUNICIPIO_OBITO no formato "Nome do Município, UF"
df['MUNICIPIO_OBITO'] = df['nome'] + ', ' + df['UF_SIGLA']

# 7. Limpeza: Remover a coluna de código original e as colunas auxiliares
colunas_para_remover = ['COD_MUNICIPIO_OBITO', 'codigo_6', 'nome', 'codigo_uf', 'UF_SIGLA']
df = df.drop(columns=colunas_para_remover, errors='ignore')

# 8. Salvar o arquivo final
df.to_parquet('dados_obitos_final.parquet', index=False)

print("Processo concluído!")
print(f"Colunas atuais: {df.columns.tolist()}")
print(df[['MUNICIPIO_OBITO']].head())