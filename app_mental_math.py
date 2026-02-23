import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# --- LÓGICA DE ESTADO ---
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""

def gerar_nova_conta(modo):
    if modo == "1 x 2 dígitos":
        st.session_state.n1 = random.randint(2, 9)
        st.session_state.n2 = random.randint(10, 99)
    else: # 2 x 2 dígitos
        st.session_state.n1 = random.randint(10, 99)
        st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""
    # Limpar o campo de resposta via session_state
    if "campo_resposta" in st.session_state:
        st.session_state.campo_resposta = ""

# --- INTERFACE ---
# Menu para escolher o tipo de conta
modo_treino = st.radio(
    "Escolha o nível de dificuldade:",
    ("2 x 2 dígitos", "1 x 2 dígitos"),
    horizontal=True
)

# Mostra a conta com destaque
st.subheader(f"Quanto é {st.session_state.n1} × {st.session_state.n2}?")

# Campo de entrada
resposta = st.text_input("Resultado:", key="campo_resposta")

# Botão de verificar
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

# Exibe o feedback (se houver)
if st.session_state.feedback:
    st.write(st.session_state.feedback)

# Botão para próxima conta
if st.button("Próxima Conta ➡️"):
    gerar_nova_conta(modo_treino)
    st.rerun()