import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# --- INICIALIZAÇÃO DE ESTADO (Correção do Erro) ---
# Se qualquer uma dessas chaves não existir, nós as criamos agora
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)

if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

# --- FUNÇÃO PARA GERAR NOVA CONTA ---
def gerar_nova_conta(modo):
    if modo == "1 x 2 dígitos":
        st.session_state.n1 = random.randint(2, 9)
        st.session_state.n2 = random.randint(10, 99)
    else:
        st.session_state.n1 = random.randint(10, 99)
        st.session_state.n2 = random.randint(10, 99)
    
    st.session_state.feedback = ""
    # Limpa o campo de resposta
    st.session_state.campo_resposta = ""

# --- INTERFACE ---
modo_treino = st.radio(
    "Escolha o nível de dificuldade:",
    ("2 x 2 dígitos", "1 x 2 dígitos"),
    horizontal=True
)

st.subheader(f"Quanto é {st.session_state.n1} × {st.session_state.n2}?")

# Campo de entrada
resposta = st.text_input("Resultado:", key="campo_resposta")

if st.button("Verificar"):
    if resposta:
        try:
            resultado_real = st.session_state.n1 * st.session_state.n2
            if int(resposta) == resultado_real:
                st.session_state.feedback = f"✅ Correto! {st.session_state.n1} × {st.session_state.n2} = {resultado_real}"
            else:
                st.session_state.feedback = f"❌ Errado. Era {resultado_real}"
        except ValueError:
            st.session_state.feedback = "⚠️ Digite um número válido."
    else:
        st.session_state.feedback = "🤔 Digite uma resposta."

# Agora o feedback sempre existirá (mesmo que vazio), evitando o AttributeError
if st.session_state.feedback:
    st.write(st.session_state.feedback)

if st.button("Próxima Conta ➡️"):
    gerar_nova_conta(modo_treino)
    st.rerun()