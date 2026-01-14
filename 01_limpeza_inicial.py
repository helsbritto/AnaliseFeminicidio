import pandas as pd

# 1. Carregar o arquivo .parquet
df = pd.read_parquet('feminicidio_raw.parquet')

# 2. Excluir as colunas especificadas
# O parâmetro 'errors=ignore' serve para não dar erro caso a coluna já não exista
colunas_para_excluir = ['COD_MUNICIPIO_RESID', 'DT_CADASTRO_OBITO']
df = df.drop(columns=colunas_para_excluir, errors='ignore')

# 3. Limpeza de dados nulos
# Opção A: Remover linhas que contenham QUALQUER valor nulo
df_limpo = df.dropna()

# Opção B: Remover nulos apenas de colunas específicas (exemplo)
# df_limpo = df.dropna(subset=['OUTRA_COLUNA_IMPORTANTE'])

# 4. Salvar o resultado em um novo arquivo
df_limpo.to_parquet('feminicidio_temp.parquet', index=False)

# 1. Carregar o arquivo .parquet
df = pd.read_parquet('feminicidio_temp.parquet')

# 2. Excluir a coluna CAUSA_BASICA
# O errors='ignore' evita que o script pare caso a coluna não exista
df = df.drop(columns=['CAUSA_BASICA'], errors='ignore')
df = df.drop(columns=['HORA_OBITO'], errors='ignore')
# 3. Alterar o nome da coluna DESCRIÇÃO para FORMA_OBITO
# Usamos um dicionário: {'NOME_ANTIGO': 'NOME_NOVO'}
df = df.rename(columns={'DESCRIÇÃO': 'FORMA_DO_OBITO'})

# 4. Salvar o arquivo final processado
df.to_parquet('feminicidio_temp.parquet', index=False)

print("Colunas processadas com sucesso!")
print(f"Colunas atuais no arquivo: {df.columns.tolist()}")

print("Limpeza concluída com sucesso!")
