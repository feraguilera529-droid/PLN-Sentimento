import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="🤖",
    layout="centered"
)

# Título e descrição explicando a versão offline
st.title("🤖 Analisador de Sentimentos Offline")
st.markdown("""
Esta é uma aplicação executada inteiramente **offline**, utilizando bibliotecas tradicionais de Processamento de Linguagem Natural (PLN) em Python (`TextBlob`). 
Nenhuma API externa (como OpenAI ou Google Cloud) é utilizada para a análise de sentimento. 
Caso você digite em português, o texto será traduzido de forma invisível para o inglês antes de passar pela análise.
""")

st.markdown("---")

# Área de texto para entrada do usuário
texto_usuario = st.text_area(
    "Digite o texto que deseja analisar:",
    placeholder="Ex: Eu adorei este aplicativo, ele é simplesmente fantástico!",
    height=150
)

# Botão 'Analisar'
if st.button("Analisar Sentimento", type="primary"):
    if not texto_usuario.strip():
        st.warning("⚠️ Por favor, digite algum texto antes de clicar em analisar.")
    else:
        with st.spinner("Processando análise de sentimento..."):
            try:
                # Tradução invisível para o inglês (o TextBlob funciona melhor em inglês)
                # O GoogleTranslator do deep-translator detecta o idioma automaticamente ou traduz de pt para en
                texto_traduzido = GoogleTranslator(source='auto', target='en').translate(texto_usuario)
                
                # Análise com TextBlob
                blob = TextBlob(texto_traduzido)
                polaridade = blob.sentiment.polarity  # Valor entre -1.0 e 1.0
                
                # Classificação baseada na polaridade
                if polaridade > 0.05:
                    sentimento = "Positivo"
                    st.success(f"**Resultado:** Sentimento {sentimento} (Polaridade: `{polaridade:.2f}`)")
                elif polaridade < -0.05:
                    sentimento = "Negativo"
                    st.error(f"**Resultado:** Sentimento {sentimento} (Polaridade: `{polaridade:.2f}`)")
                else:
                    sentimento = "Neutro"
                    st.warning(f"**Resultado:** Sentimento {sentimento} (Polaridade: `{polaridade:.2f}`)")
                
                # Exibir detalhes extras opcionais para transparência
                with st.expander("Ver detalhes técnicos (Tradução e Métrica)"):
                    st.write(f"**Texto Original:** {texto_usuario}")
                    st.write(f"**Texto Traduzido (para o TextBlob):** {texto_traduzido}")
                    st.write(f"**Subjetividade (0 = Factual, 1 = Subjetivo):** {blob.sentiment.subjectivity:.2f}")

            except Exception as e:
                st.error(f"Ocorreu um erro durante o processamento: {e}")

# Rodapé informando sobre a licença MIT
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 12px;'>"
    "Desenvolvido com Python & Streamlit • Licença MIT"
    "</div>", 
    unsafe_allow_html=True
)
