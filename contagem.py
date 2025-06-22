import pandas as pd

#Caminho do arquivo
caminho_arquivo_resultados = "resultados_baseline.csv"

print(f"\nIniciando contagem bruta de sucesso/falha para '{caminho_arquivo_resultados}'...")

try:
    df_resultados = pd.read_csv(caminho_arquivo_resultados)

    acertos = 0
    total = len(df_resultados)

    for index, linha in df_resultados.iterrows():
        # Normaliza as strings para uma comparação mais justa:
        # remove espaços no início/fim e converte para minúsculas.
        # Também remove o ponto e vírgula final, que pode variar.
        sql_gerado = str(linha['sql_gerado_baseline']).strip().lower().rstrip(';')
        sql_correto = str(linha['sql_correto']).strip().lower().rstrip(';')
        
        if sql_gerado == sql_correto:
            acertos += 1
            
    taxa_de_acerto = (acertos / total) * 100 if total > 0 else 0

    print("\n--- Resultado da Contagem Bruta (Baseline) ---")
    print(f"Total de Exemplos Avaliados: {total}")
    print(f"Número de Acertos (Match Exato): {acertos}")
    print(f"Taxa de Acerto Bruta: {taxa_de_acerto:.2f}%")

except FileNotFoundError:
    print(f"ERRO: O arquivo de resultados '{caminho_arquivo_resultados}' não foi encontrado.")