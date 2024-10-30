import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import yaml
import matplotlib.pyplot as plt
import numpy as np

# Carregar variáveis do .env
load_dotenv()

# Função para carregar a chave da API
def carregar_chave_api():
    """Tenta carregar a chave do .env e, se não encontrar, tenta o config.yaml."""
    # Primeiro, tenta carregar a chave do .env
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        #st.write("Chave carregada do .env")  # Debug para monitorar
        return api_key

    # Se não encontrada no .env, tenta carregar do config.yaml
    try:
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file) or {}
            api_key = config.get('OPENAI_API_KEY')
        
        if api_key and api_key != "USE_ENV":
            #st.write("Chave carregada do config.yaml")  # Debug para monitorar
            return api_key
        else:
            raise ValueError("Chave não encontrada ou é um placeholder.")

    except (FileNotFoundError, ValueError) as e:
        st.error("Erro: Chave da API não encontrada. Verifique seu .env ou config.yaml.")
        st.stop()

# Carregar a chave da API
api_key = carregar_chave_api()

# Inicializar o modelo ChatOpenAI
def inicializar_modelo():
    """Inicializa o modelo OpenAI."""
    try:
        return ChatOpenAI(api_key=api_key, model_name='gpt-3.5-turbo', temperature=0)
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo OpenAI: {e}")
        st.stop()

# Inicializar o modelo
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
