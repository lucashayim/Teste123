import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import streamlit

# 1. Função para carregar e preparar os dados
# Essa função é o "coração" da automação, pois ela sabe como encontrar os dados relevantes no seu arquivo.
def carregar_dados_relatorio(caminho_arquivo):
    """
    Carrega o relatório e extrai os dados de acessos de pessoas e veículos.
    """
    try:
        # Lê o arquivo e ignora as 4 primeiras linhas que não contêm dados úteis
        df = pd.read_csv(caminho_arquivo, header=None, skiprows=4)
        
        # Encontra a linha onde começam os dados de pessoas ('Motorista e Ajudantes')
        indice_pessoas = df[df.iloc[:, 0] == 'Motorista e Ajudantes'].index[0]
        
        # Extrai os dados de pessoas (as 4 próximas linhas após o índice encontrado)
        dados_pessoas = df.iloc[indice_pessoas:indice_pessoas+4, :]
        df_pessoas = pd.DataFrame({
            'Categoria': dados_pessoas.iloc[:, 0].values,
            'Quantidade': pd.to_numeric(dados_pessoas.iloc[:, 4].values, errors='coerce')
        })
        
        # Encontra a linha onde começam os dados de veículos ('Entregas de Materia Prima')
        indice_veiculos = df[df.iloc[:, 0] == 'Entregas de Materia Prima'].index[0]
        
        # Extrai os dados de veículos (as 4 próximas linhas após o índice encontrado)
        dados_veiculos = df.iloc[indice_veiculos:indice_veiculos+4, :]
        df_veiculos = pd.DataFrame({
            'Categoria': dados_veiculos.iloc[:, 0].values,
            'Quantidade': pd.to_numeric(dados_veiculos.iloc[:, 4].values, errors='coerce')
        })
        
        return df_pessoas, df_veiculos
        
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None, None
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        return None, None

# 2. Função para criar o gráfico (reutilizando o código anterior)
def criar_grafico_seaborn(df, titulo, nome_arquivo):
    """
    Gera e salva um gráfico de barras a partir de um DataFrame.
    """
    if df is None or df.empty:
        print(f"Não há dados para gerar o gráfico '{titulo}'.")
        return
        
    df = df.sort_values(by='Quantidade', ascending=False)
    
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    
    ax = sns.barplot(x='Quantidade', y='Categoria', data=df)
    plt.title(titulo, fontsize=18, pad=20)
    plt.xlabel('Quantidade', fontsize=14, labelpad=15)
    plt.ylabel('Categoria', fontsize=14, labelpad=15)
    
    for p in ax.patches:
        ax.annotate(f'{int(p.get_width())}',
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=12)
                    
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    print(f"Gráfico '{nome_arquivo}' criado com sucesso!")

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    # Nome do arquivo que o usuário vai subir.
    nome_arquivo_relatorio = 'Estatística_de_Acessos.xlsx - Plan1.csv'
    
    # Executa a função para carregar os dados
    df_pessoas, df_veiculos = carregar_dados_relatorio(nome_arquivo_relatorio)
    
    # Cria os gráficos se os dados foram carregados com sucesso
    if df_pessoas is not None:
        criar_grafico_seaborn(df_pessoas, 'Total de Acessos de Pessoas por Categoria', 'acessos_pessoas.png')
    if df_veiculos is not None:

        criar_grafico_seaborn(df_veiculos, 'Total de Acessos de Veículos por Categoria', 'acessos_veiculos.png')
