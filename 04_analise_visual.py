import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Carregar os dados
df = pd.read_parquet('feminicidio_final.parquet')

# 2. Criar a coluna UF a partir de MUNICIPIO_OBITO
# Formato esperado: "Nome da Cidade, UF"
df['UF'] = df['MUNICIPIO_OBITO'].str.split(',').str[-1].str.strip()

# --- GRÁFICO 1: DISTRIBUIÇÃO POR ESTADO ---
plt.figure(figsize=(12, 6))
order = df['UF'].value_counts().index 

sns.countplot(data=df, x='UF', order=order, hue='UF', palette='viridis', legend=False)

plt.title('Distribuição de Óbitos por Estado (UF)', fontsize=15)
plt.xlabel('Estado')
plt.ylabel('Quantidade de Óbitos')
plt.show()

# --- GRÁFICO 2: LOCAL vs MÉTODO (TOP 5) ---

# Nomes exatos conforme sua lista:
coluna_metodo = 'DESCRICAO' 
coluna_local = 'LOCAL_OCORRENCIA_OBITO'

# Identificar as top 5 formas de óbito
top_5_causas = df[coluna_metodo].value_counts().nlargest(5).index

# Filtrar o dataframe apenas com essas causas
df_top = df[df[coluna_metodo].isin(top_5_causas)]

# Criar a tabela de cruzamento (proporção em %)
ct = pd.crosstab(df_top[coluna_local], df_top[coluna_metodo], normalize='index') * 100

# Plotar o gráfico de barras empilhadas
ax = ct.plot(kind='bar', stacked=True, colormap='viridis', figsize=(14, 7))

plt.title('Dinâmica da Violência: Local de Ocorrência vs. Método Utilizado', fontsize=15)
plt.legend(title='Método da Agressão', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.ylabel('Percentual de Ocorrências (%)')
plt.xlabel('Local onde ocorreu o óbito')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()