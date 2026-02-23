import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# 2. CSS REALMENTE FORÇADO (Grid Nativo)
st.markdown("""
    <style>
    /* Estilização dos botões para parecerem uma calculadora real */
    div.stButton > button {
        width: 100% !important;
        height: 65px !important;
        font-size: 24px !important;
        background-color: #f0f2f6;
        border-radius: 12px;
        margin-bottom: -10px;
    }
    
    /* Força o container das colunas a NUNCA quebrar a linha */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
    }
    [data-testid="column"] {
        width: 33% !important;
        flex: 1 1 33% !important;
        min-width: 33% !important;
    }
    h1, h2 { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Inicialização do Estado
for key in ['n1', 'n2', 'resposta', 'feedback', 'modo']:
    if key not in st.session_state:
        if key == 'modo': st.session_state.modo = "2 x 2"
        elif key == 'resposta': st.session_state.resposta = ""
        elif key == 'feedback': st.session_state.feedback = ""
        else: st.session_state[key] = random.randint(10, 99)

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

st.write(f"## {st.session_state.n1} × {st.session_state.n2}")
# Display da resposta com destaque
st.markdown(f"<h1 style='color: #1E90FF; background: #f8f9fb; border-radius: 10px; padding: 10px;'>{st.session_state.resposta if st.session_state.resposta else '?'}</h1>", unsafe_allow_html=True)

# 5. TECLADO NUMÉRICO (Usando funções para evitar repetição)
def pressionou(tecla):
    if tecla == "⌫":
        st.session_state.resposta = st.session_state.resposta[:-1]
    elif tecla == "C":
        st.session_state.resposta = ""
    else:
        st.session_state.resposta += str(tecla)
    st.rerun()

# Layout do Teclado - Criando as linhas manualmente para garantir o layout
linhas = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["⌫", 0, "C"]
]

for idx, linha in enumerate(linhas):
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button(str(linha[0]), key=f"b{idx}1"): pressionou(linha[0])
    with c2: 
        if st.button(str(linha[1]), key=f"b{idx}2"): pressionou(linha[1])
    with c3: 
        if st.button(str(linha[2]), key=f"b{idx}3"): pressionou(linha[2])

st.markdown("<br>", unsafe_allow_html=True)

# 6. Verificação e Navegação
col_v, col_p = st.columns(2)

with col_v:
    if st.button("VERIFICAR ✅", type="primary", use_container_width=True):
        real = st.session_state.n1 * st.session_state.n2
        if st.session_state.resposta and int(st.session_state.resposta) == real:
            st.session_state.feedback = f"✅ Acertou! {real}"
        else:
            st.session_state.feedback = f"❌ Errou! Era {real}"

with col_p:
    if st.button("PRÓXIMA ➡️", use_container_width=True):
        atualizar()
        st.rerun()

if st.session_state.feedback:
    st.info(st.session_state.feedback)