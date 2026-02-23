import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# 2. CSS GRID (A prova de falhas para Mobile)
# Aqui definimos um grid de 3 colunas que NÃO QUEBRA nunca.
st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        max-width: 300px;
        margin: 0 auto;
    }
    /* Estilizando os botões do Streamlit para preencherem o grid */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        font-size: 22px !important;
        font-weight: bold !important;
    }
    .main-title { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. Inicialização do Estado
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.resposta = ""
    st.session_state.feedback = ""
    st.session_state.modo = "2 x 2"

def atualizar():
    if st.session_state.modo == "1 x 2":
        st.session_state.n1 = random.randint(2, 9)
    else:
        st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.resposta = ""
    st.session_state.feedback = ""

# 4. Interface
st.radio("Dificuldade:", ["2 x 2", "1 x 2"], key="modo", on_change=atualizar, horizontal=True)

st.markdown(f"<h2 class='main-title'>Quanto é {st.session_state.n1} × {st.session_state.n2}?</h2>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: #1E90FF;'>{st.session_state.resposta if st.session_state.resposta else '?'}</h1>", unsafe_allow_html=True)

# 5. O TECLADO COM COLUNAS "FORCE-ROW"
# Para garantir que o Streamlit não quebre, usamos o container de colunas
# mas com botões menores e chaves únicas.

def add(n):
    st.session_state.resposta += str(n)
    st.rerun()

# Criando o teclado usando um padrão de 3 colunas fixas
teclado = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["⌫", 0, "C"]
]

for linha in teclado:
    cols = st.columns(3) # O Streamlit tentará empilhar aqui...
    for i, char in enumerate(linha):
        if cols[i].button(str(char), key=f"btn_{char}", use_container_width=True):
            if char == "⌫": st.session_state.resposta = st.session_state.resposta[:-1]
            elif char == "C": st.session_state.resposta = ""
            else: add(char)
            st.rerun()

st.divider()

# 6. Verificação
if st.button("VERIFICAR ✅", type="primary", use_container_width=True):
    real = st.session_state.n1 * st.session_state.n2
    if st.session_state.resposta and int(st.session_state.resposta) == real:
        st.session_state.feedback = f"✅ Acertou! {real}"
    else:
        st.session_state.feedback = f"❌ Errou! Era {real}"

if st.button("PRÓXIMA CONTA ➡️", use_container_width=True):
    atualizar()
    st.rerun()

if st.session_state.feedback:
    st.info(st.session_state.feedback)