import streamlit as st
import random

st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# --- 1. INICIALIZAÇÃO SEGURA DO ESTADO ---
# Garantimos que TODAS as variáveis existam antes de qualquer lógica
if 'modo_escolhido' not in st.session_state:
    st.session_state.modo_escolhido = "2 x 2 dígitos"

if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)

if 'resposta_atual' not in st.session_state:
    st.session_state.resposta_atual = ""

if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

# --- 2. FUNÇÕES DE LÓGICA ---
def sortear_numeros():
    if st.session_state.modo_escolhido == "1 x 2 dígitos":
        st.session_state.n1 = random.randint(2, 9)
        st.session_state.n2 = random.randint(10, 99)
    else:
        st.session_state.n1 = random.randint(10, 99)
        st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""
    st.session_state.resposta_atual = ""

def digitar(numero):
    st.session_state.resposta_atual += str(numero)

def limpar_digito():
    st.session_state.resposta_atual = st.session_state.resposta_atual[:-1]

# --- 3. INTERFACE ---
# Radio button para trocar o modo
st.radio(
    "Dificuldade:",
    ["2 x 2 dígitos", "1 x 2 dígitos"],
    key="modo_escolhido",
    on_change=sortear_numeros,
    horizontal=True
)

st.markdown(f"### Quanto é {st.session_state.n1} × {st.session_state.n2}?")

# Display da resposta que vai sendo montada
# Usamos o método .get() para evitar o erro de atributo se algo falhar
resp_visual = st.session_state.get('resposta_atual', '')
st.markdown(f"## :blue[{resp_visual if resp_visual else '?'}]")

# --- 4. TECLADO NUMÉRICO ---
with st.container():
    # Teclas 1 a 9
    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j in range(3):
            num = i + j + 1
            if cols[j].button(str(num), use_container_width=True, key=f"btn_{num}"):
                digitar(num)
                st.rerun()

    # Teclas 0, Backspace e Limpar Tudo
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

st.divider()

# --- 5. VERIFICAÇÃO ---
if st.button("VERIFICAR ✅", use_container_width=True, type="primary"):
    if st.session_state.resposta_atual:
        res_real = st.session_state.n1 * st.session_state.n2
        if int(st.session_state.resposta_atual) == res_real:
            st.session_state.feedback = f"✅ Correto! {st.session_state.n1} x {st.session_state.n2} = {res_real}"
        else:
            st.session_state.feedback = f"❌ Errado! O resultado era {res_real}"
    else:
        st.session_state.feedback = "🤔 Digite algo primeiro."

if st.button("PRÓXIMA CONTA ➡️", on_click=sortear_numeros, use_container_width=True):
    pass

if st.session_state.feedback:
    # Mostra o feedback com um estilo de alerta (verde para sucesso, azul para info)
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.info(st.session_state.feedback)