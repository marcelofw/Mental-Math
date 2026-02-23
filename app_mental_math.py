import streamlit as st
import random

st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# --- FUNÇÃO PARA GERAR NÚMEROS ---
def sortear_numeros():
    if st.session_state.modo_escolhido == "1 x 2 dígitos":
        st.session_state.n1 = random.randint(2, 9)
        st.session_state.n2 = random.randint(10, 99)
    else:
        st.session_state.n1 = random.randint(10, 99)
        st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""
    # O 'hack' para limpar o campo: mudamos a chave do input
    st.session_state.input_key += 1

# --- INICIALIZAÇÃO DO ESTADO ---
if 'n1' not in st.session_state:
    st.session_state.modo_escolhido = "2 x 2 dígitos"
    st.session_state.input_key = 0
    sortear_numeros()

# --- INTERFACE ---
# O on_change faz a função rodar assim que você clica na opção
st.radio(
    "Dificuldade:",
    ["2 x 2 dígitos", "1 x 2 dígitos"],
    key="modo_escolhido",
    on_change=sortear_numeros,
    horizontal=True
)

st.subheader(f"Quanto é {st.session_state.n1} × {st.session_state.n2}?")

# Usamos a input_key para resetar o campo automaticamente
resposta = st.text_input("Resultado:", key=f"resp_{st.session_state.input_key}")

col1, col2 = st.columns(2)

with col1:
    if st.button("Verificar", use_container_width=True):
        if resposta:
            try:
                res_real = st.session_state.n1 * st.session_state.n2
                if int(resposta) == res_real:
                    st.session_state.feedback = f"✅ Correto! {res_real}"
                else:
                    st.session_state.feedback = f"❌ Errado! Era {res_real}"
            except ValueError:
                st.session_state.feedback = "⚠️ Digite apenas números."
        else:
            st.session_state.feedback = "🤔 Digite algo."

with col2:
    if st.button("Próxima Conta ➡️", on_click=sortear_numeros, use_container_width=True):
        pass # A função sortear_numeros já faz o trabalho no clique

if st.session_state.feedback:
    st.write(st.session_state.feedback)