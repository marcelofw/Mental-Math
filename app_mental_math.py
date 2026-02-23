import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# 2. CSS NINJA para Mobile (Força 3 colunas em telas pequenas)
st.markdown("""
    <style>
    /* Alvo: Containers de colunas do Streamlit */
    [data-testid="column"] {
        flex: 1 1 31% !important;
        width: 31% !important;
        min-width: 31% !important;
    }
    
    /* Garante que o bloco horizontal não quebre linha */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 5px !important;
    }

    /* Estilo dos botões numéricos */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 24px !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Inicialização do Estado
for key in ['n1', 'n2', 'resposta', 'feedback', 'modo']:
    if key not in st.session_state:
        if key == 'modo': st.session_state.modo = "2 x 2"
        elif key == 'resposta': st.session_state.resposta = ""
        elif key == 'feedback': st.session_state.feedback = ""
        else: st.session_state[key] = random.randint(10, 99)

def atualizar_conta():
    if st.session_state.modo == "1 x 2":
        st.session_state.n1 = random.randint(2, 9)
    else:
        st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.resposta = ""
    st.session_state.feedback = ""

# 4. Interface
st.radio("Modo:", ["2 x 2", "1 x 2"], key="modo", on_change=atualizar_conta, horizontal=True)

st.markdown(f"<h2 style='text-align: center;'>{st.session_state.n1} × {st.session_state.n2}</h2>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: #1E90FF;'>{st.session_state.resposta if st.session_state.resposta else '?'}</h1>", unsafe_allow_html=True)

# 5. O TECLADO (Construção manual das linhas)
def add_num(v): st.session_state.resposta += str(v)

# Linhas da Calculadora
def criar_linha(nums):
    cols = st.columns(len(nums))
    for i, n in enumerate(nums):
        if cols[i].button(str(n), key=f"btn_{n}"):
            add_num(n)
            st.rerun()

criar_linha([1, 2, 3])
criar_linha([4, 5, 6])
criar_linha([7, 8, 9])

# Linha de utilitários
c1, c2, c3 = st.columns(3)
if c1.button("0"): add_num(0); st.rerun()
if c2.button("⌫"): st.session_state.resposta = st.session_state.resposta[:-1]; st.rerun()
if c3.button("C"): st.session_state.resposta = ""; st.rerun()

st.divider()

# Botões de Ação
if st.button("VERIFICAR ✅", type="primary", use_container_width=True):
    real = st.session_state.n1 * st.session_state.n2
    if st.session_state.resposta and int(st.session_state.resposta) == real:
        st.session_state.feedback = "✅ Correto!"
        st.balloons()
    else:
        st.session_state.feedback = f"❌ Errado! Era {real}"

if st.button("PRÓXIMA CONTA ➡️", use_container_width=True):
    atualizar_conta()
    st.rerun()

if st.session_state.feedback:
    st.write(st.session_state.feedback)