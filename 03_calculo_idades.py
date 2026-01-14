import pandas as pd

# 1. Carregar o arquivo
df = pd.read_parquet('dados_obitos_final.parquet')

# 2. Converter para data informando o formato exato (%d%m%Y)
# O .str.zfill(8) garante que datas como 1011999 virem 01011999
df['DT_NASCIMENTO'] = pd.to_datetime(
    df['DT_NASCIMENTO'].astype(str).str.zfill(8), 
    format='%d%m%Y', 
    errors='coerce'
)

df['DT_OBITO'] = pd.to_datetime(
    df['DT_OBITO'].astype(str).str.zfill(8), 
    format='%d%m%Y', 
    errors='coerce'
)

# 3. Remover linhas onde a conversão falhou (datas que não existem no calendário)
df = df.dropna(subset=['DT_NASCIMENTO', 'DT_OBITO'])

# 4. Calcular a idade
df['IDADE_VITIMA'] = df['DT_OBITO'].dt.year - df['DT_NASCIMENTO'].dt.year

# Ajuste fino: subtrair 1 se o óbito ocorreu ANTES do aniversário no ano
foi_antes_aniversario = (
    (df['DT_OBITO'].dt.month < df['DT_NASCIMENTO'].dt.month) | 
    ((df['DT_OBITO'].dt.month == df['DT_NASCIMENTO'].dt.month) & 
     (df['DT_OBITO'].dt.day < df['DT_NASCIMENTO'].dt.day))
)
df.loc[foi_antes_aniversario, 'IDADE_VITIMA'] -= 1

# 5. Converter para número inteiro (opcional, para não ficar 25.0)
df['IDADE_VITIMA'] = df['IDADE_VITIMA'].astype(int)

# 6. Excluir as colunas de data originais
df = df.drop(columns=['DT_NASCIMENTO', 'DT_OBITO'])

# Salvar
df.to_parquet('dados_com_idade_correta.parquet', index=False)

print("Idade calculada com sucesso usando o formato DDMMYYYY!")
print(df[['IDADE_VITIMA']].head())