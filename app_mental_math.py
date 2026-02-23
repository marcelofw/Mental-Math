import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# 2. CSS "Bala de Prata" para forçar horizontalidade no Mobile
st.markdown("""
    <style>
    /* Remove o scroll horizontal e força colunas lado a lado */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 0.3rem !important;
    }
    /* Força cada coluna a ter exatamente um terço da largura */
    [data-testid="column"] {
        width: 33% !important;
        min-width: 33% !important;
        flex: 1 1 33% !important;
    }
    /* Estilo dos botões para não ocuparem espaço demais */
    .stButton button {
        width: 100% !important;
        padding: 0px !important;
        height: 50px !important;
        font-size: 20px !important;
    }
    /* Centralização de textos */
    .stMarkdown h2, .stMarkdown h1 {
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Inicialização do Estado
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.modo = "2 x 2"
    st.session_state.resposta = ""
    st.session_state.feedback = ""

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

st.write(f"## Quanto é {st.session_state.n1} × {st.session_state.n2}?")
st.write(f"# :blue[{st.session_state.resposta if st.session_state.resposta else '?'}]")

# 5. Teclado Numérico (Forçado)
def add_n(n): 
    st.session_state.resposta += str(n)
    st.rerun()

# Linhas do Teclado
for linha in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
    c1, c2, c3 = st.columns(3)
    if c1.button(str(linha[0]), key=f"k{linha[0]}"): add_n(linha[0])
    if c2.button(str(linha[1]), key=f"k{linha[1]}"): add_n(linha[1])
    if c3.button(str(linha[2]), key=f"k{linha[2]}"): add_n(linha[2])

c1, c2, c3 = st.columns(3)
if c1.button("0", key="k0"): add_n(0)
if c2.button("⌫", key="back"): 
    st.session_state.resposta = st.session_state.resposta[:-1]
    st.rerun()
if c3.button("C", key="clear"): 
    st.session_state.resposta = ""
    st.rerun()

st.divider()

# Botões de Ação
if st.button("VERIFICAR ✅", type="primary", use_container_width=True):
    real = st.session_state.n1 * st.session_state.n2
    if st.session_state.resposta and int(st.session_state.resposta) == real:
        st.session_state.feedback = "✅ Correto!"
    else:
        st.session_state.feedback = f"❌ Errado! Era {real}"

if st.button("PRÓXIMA CONTA ➡️", use_container_width=True):
    atualizar_conta()
    st.rerun()

if st.session_state.feedback:
    st.info(st.session_state.feedback)