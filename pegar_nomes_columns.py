import pandas as pd

# Substitua pelo nome do arquivo que você quer checar no momento
arquivo = 'feminicidio_final.parquet'

# Carrega apenas o cabeçalho (mais rápido para arquivos grandes)
df = pd.read_parquet(arquivo)

print(f"\n--- Colunas encontradas no arquivo: {arquivo} ---")

# Opção 1: Lista simples
print(df.columns.tolist())
