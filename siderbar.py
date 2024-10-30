import streamlit as st
from langchain_openai import ChatOpenAI  # Importação atualizada
from langchain.prompts import PromptTemplate
import os
import yaml
import matplotlib.pyplot as plt
import numpy as np

# Carregar a chave da API do arquivo config.yaml
def carregar_chave_api():
    """Carrega a chave da API do arquivo config.yaml e define como variável de ambiente."""
    try:
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
    except FileNotFoundError:
        st.error("Arquivo config.yaml não encontrado. Verifique se ele está no diretório correto.")
        st.stop()
    except KeyError:
        st.error("A chave 'OPENAI_API_KEY' não foi encontrada no arquivo config.yaml.")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar a chave da API: {e}")
        st.stop()

# Inicializar o modelo ChatOpenAI
def inicializar_modelo():
    """Inicializa o modelo OpenAI e retorna a instância."""
    try:
        return ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo OpenAI: {e}")
        st.stop()

# Carregar a chave da API e inicializar o modelo
carregar_chave_api()
openai = inicializar_modelo()

# Definir o template do prompt
template = '''
Você é um analista financeiro.
Escreva um relatório financeiro detalhado para a empresa "{empresa}" para o período {periodo}.
O relatório deve ser escrito em {idioma} e incluir a seguinte análise: {analise}.
Certifique-se de fornecer insights e conclusões para esta seção.
Formate o relatório utilizando Markdown.
'''

prompt_template = PromptTemplate.from_template(template=template)

# Opções para os selects
empresas = ['ACME Corp', 'Globex Corporation', 'Soylent Corp', 'Initech', 'Umbrella Corporation']
trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
anos = [2021, 2022, 2023, 2024]
idiomas = ['Português', 'Inglês', 'Espanhol', 'Francês', 'Alemão']
analises = [
    "Análise do Balanço Patrimonial",
    "Análise do Fluxo de Caixa",
    "Análise de Tendências",
    "Análise de Receita e Lucro",
    "Análise de Posição de Mercado"
]

# Título da aplicação
st.title('Gerador de Relatório Financeiro')

# Criando os controles na barra lateral
empresa = st.sidebar.selectbox('Selecione a empresa:', empresas)
trimestre = st.sidebar.selectbox('Selecione o trimestre:', trimestres)
ano = st.sidebar.selectbox('Selecione o ano:', anos)
periodo = f"{trimestre} {ano}"
idioma = st.sidebar.selectbox('Selecione o idioma:', idiomas)
analise = st.sidebar.selectbox('Selecione a análise:', analises)

# Função para gerar um gráfico de exemplo
def gerar_grafico_exemplo():
    """Gera um gráfico de exemplo com dados aleatórios."""
    fig, ax = plt.subplots()
    dados = np.random.rand(10)
    ax.plot(dados, marker='o')
    ax.set_title('Exemplo de Gráfico')
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    return fig

# Botão para gerar o relatório
if st.sidebar.button('Gerar Relatório'):
    try:
        # Gerar o prompt usando o template
        prompt = prompt_template.format(
            empresa=empresa,
            periodo=periodo,
            idioma=idioma,
            analise=analise
        )

        # Fazer a chamada ao modelo OpenAI
        response = openai.predict(prompt)

        # Exibir o relatório gerado e o gráfico
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader('Relatório Gerado:')
            st.markdown(response)

        with col2:
            st.subheader('Gráfico Gerado:')
            fig = gerar_grafico_exemplo()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar o relatório: {e}")
else:
    st.info("Selecione as opções desejadas e clique em 'Gerar Relatório'.")
