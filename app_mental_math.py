import streamlit as st
import random

# Configuração da página para parecer um app de celular
st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

st.title("🔢 Mestre da Multiplicação")
st.write("Treine sua mente com números de 2 dígitos.")

# --- LÓGICA DE ESTADO (Para o app não 'resetar' a conta toda hora) ---
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.acertos = 0

def nova_pergunta():
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.resposta_usuario = "" # Limpa o campo de texto

# --- INTERFACE ---
n1 = st.session_state.n1
n2 = st.session_state.n2
resultado_real = n1 * n2

st.subheader(f"Quanto é {n1} × {n2}?")

# Campo de entrada (o parâmetro 'key' ajuda o Streamlit a manter o valor)
resposta = st.text_input("Sua resposta:", key="resposta_usuario")

col1, col2 = st.columns(2)

with col1:
    if st.button("Verificar"):
        if resposta:
            try:
                if int(resposta) == resultado_real:
                    st.success(f"Correto! {n1} × {n2} = {resultado_real}")
                    st.session_state.acertos += 1
                else:
                    st.error(f"Incorreto. O resultado era {resultado_real}")
            except ValueError:
                st.warning("Por favor, digite um número.")
        else:
            st.info("Digite algo antes de verificar.")

with col2:
    if st.button("Próxima Conta ➡️"):
        nova_pergunta()
        st.rerun()

st.divider()
st.sidebar.metric("Sessão Atual", f"{st.session_state.acertos} acertos")
if st.sidebar.button("Zerar Placar"):
    st.session_state.acertos = 0
    st.rerun()