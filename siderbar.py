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
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key

    try:
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file) or {}
            api_key = config.get('OPENAI_API_KEY')

        if api_key and api_key != "USE_ENV":
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

# Título principal
st.title('📊 Gerador de Relatório Financeiro')

# Separador de seções
st.divider()

# Criando os controles na barra lateral
st.sidebar.header("Configurações do Relatório")
empresa = st.sidebar.selectbox('Selecione a empresa:', empresas)
trimestre = st.sidebar.selectbox('Selecione o trimestre:', trimestres)
ano = st.sidebar.selectbox('Selecione o ano:', anos)
periodo = f"{trimestre} {ano}"
idioma = st.sidebar.selectbox('Selecione o idioma:', idiomas)
analise = st.sidebar.selectbox('Selecione a análise:', analises)

# Função para gerar um gráfico de exemplo
def gerar_grafico_exemplo():
    fig, ax = plt.subplots(figsize=(10, 6))
    dados = np.random.rand(10)
    ax.plot(dados, marker='o', linestyle='-', linewidth=2)
    ax.set_title('Exemplo de Gráfico', fontsize=18)
    ax.set_xlabel('Eixo X', fontsize=14)
    ax.set_ylabel('Eixo Y', fontsize=14)
    ax.grid(True)
    return fig

# Botão para gerar o relatório
if st.sidebar.button('📄 Gerar Relatório'):
    try:
        prompt = prompt_template.format(
            empresa=empresa,
            periodo=periodo,
            idioma=idioma,
            analise=analise
        )
        response = openai.predict(prompt)

        st.subheader('📝 Relatório Gerado:')
        st.markdown(
            f"<div style='background-color: #1e1e1e; color: white; padding: 15px; "
            f"border-radius: 10px; font-size: 16px; max-width: 100%; "
            f"overflow-wrap: break-word;'>{response}</div>",
            unsafe_allow_html=True
        )

        st.subheader('📈 Gráfico Gerado:')
        fig = gerar_grafico_exemplo()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar o relatório: {e}")

else:
    st.info("🔧 Ajuste as configurações na barra lateral e clique em 'Gerar Relatório'.")

# Separador final
st.divider()

# --- Rodapé Centralizado ---
st.write("---")
st.markdown(
    """
    <div style='text-align: center; margin-top: 10px; line-height: 1.0;'>
        <p style='font-size: 16px; font-weight: bold; margin: 0 0 8px 0;'>Projeto: Gerador de Relatório Financeiro</p>
        <p style='font-size: 14px; margin: 0 0 5px 0;'>Desenvolvido por:</p>
        <p style='font-size: 20px; color: #4CAF50; font-weight: bold; margin: 0;'>Cláudio Ferreira Neves</p>
        <p style='font-size: 16px; color: #555; margin: 0;'>Especialista em RPA e AI</p>
        <p style='font-size: 14px; margin: 10px 0 5px 0;'>Ferramentas utilizadas: Python, Streamlit, LangChain, Pandas, Matplotlib</p>
        <p style='font-size: 12px; color: #777; margin: 0;'>© 2024</p>
    </div>
    """,
    unsafe_allow_html=True
)
