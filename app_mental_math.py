import streamlit as st
import random

st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# --- FUNÇÕES DE LÓGICA ---
def sortear_numeros():
    if st.session_state.modo_escolhido == "1 x 2 dígitos":
        st.session_state.n1 = random.randint(2, 9)
        st.session_state.n2 = random.randint(10, 99)
    else:
        st.session_state.n1 = random.randint(10, 99)
        st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""
    st.session_state.resposta_atual = "" # Limpa a digitação

def digitar(numero):
    st.session_state.resposta_atual += str(numero)

def limpar_digito():
    st.session_state.resposta_atual = st.session_state.resposta_atual[:-1]

# --- INICIALIZAÇÃO DO ESTADO ---
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.modo_escolhido = "2 x 2 dígitos"
    st.session_state.resposta_atual = ""
    st.session_state.feedback = ""

# --- INTERFACE ---
st.radio(
    "Dificuldade:",
    ["2 x 2 dígitos", "1 x 2 dígitos"],
    key="modo_escolhido",
    on_change=sortear_numeros,
    horizontal=True
)

# Display da Pergunta e Resposta
st.markdown(f"### Quanto é {st.session_state.n1} × {st.session_state.n2}?")
st.markdown(f"## :blue[{st.session_state.resposta_atual if st.session_state.resposta_atual else '?'}]")

# --- TECLADO NUMÉRICO ---
# Criando a grade 3x3 para os números
container_teclado = st.container()
with container_teclado:
    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j in range(3):
            num = i + j + 1
            if cols[j].button(str(num), use_container_width=True):
                digitar(num)
                st.rerun()

    # Última linha do teclado (0, Limpar, Verificar)
    c1, c2, c3 = st.columns(3)
    if c1.button("0", use_container_width=True):
        digitar(0)
        st.rerun()
    if c2.button("⌫", use_container_width=True):
        limpar_digito()
        st.rerun()
    if c3.button("Limpar", use_container_width=True):
        st.session_state.resposta_atual = ""
        st.rerun()

# Botões de Ação Final
st.divider()
if st.button("VERIFICAR ✅", use_container_width=True, type="primary"):
    if st.session_state.resposta_atual:
        res_real = st.session_state.n1 * st.session_state.n2
        if int(st.session_state.resposta_atual) == res_real:
            st.session_state.feedback = f"✅ Correto! {res_real}"
        else:
            st.session_state.feedback = f"❌ Errado! Era {res_real}"
    else:
        st.session_state.feedback = "🤔 Digite algo primeiro."

if st.button("PRÓXIMA CONTA ➡️", on_click=sortear_numeros, use_container_width=True):
    pass

# Exibe o feedback
if st.session_state.feedback:
    st.info(st.session_state.feedback)