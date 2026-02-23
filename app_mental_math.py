import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Cálculo Mental", page_icon="🔢", layout="centered")

# 2. CSS para forçar o layout de calculadora no Celular (3 colunas sempre)
st.markdown("""
    <style>
    /* Força as colunas a ficarem lado a lado no mobile */
    [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        gap: 0.5rem !important;
    }
    [data-testid="column"] {
        width: 33% !important;
        flex: 1 1 33% !important;
        min-width: 33% !important;
    }
    /* Estiliza os botões para ficarem mais altos e fáceis de tocar */
    .stButton button {
        height: 3.5rem;
        font-size: 1.5rem !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Inicialização Segura do Estado
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
if 'modo_escolhido' not in st.session_state:
    st.session_state.modo_escolhido = "2 x 2 dígitos"
if 'resposta_atual' not in st.session_state:
    st.session_state.resposta_atual = ""
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

# 4. Funções de Lógica
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

# 5. Interface Principal
st.title("🔢 Treino Mental")

# Seletor de modo (on_change faz o sorteio imediato)
st.radio(
    "Dificuldade:",
    ["2 x 2 dígitos", "1 x 2 dígitos"],
    key="modo_escolhido",
    on_change=sortear_numeros,
    horizontal=True
)

st.divider()

# Exibição da Conta
st.markdown(f"<h2 style='text-align: center;'>Quanto é {st.session_state.n1} × {st.session_state.n2}?</h2>", unsafe_allow_html=True)

# Display da Resposta (azul se vazio, verde se digitando)
cor_display = "gray" if not st.session_state.resposta_atual else "#1E90FF"
st.markdown(f"<h1 style='text-align: center; color: {cor_display};'>{st.session_state.resposta_atual if st.session_state.resposta_atual else '?'}</h1>", unsafe_allow_html=True)

# 6. Teclado Numérico Estilo Calculadora
with st.container():
    # Teclas 1 a 9 em grid 3x3
    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j in range(3):
            num = i + j + 1
            if cols[j].button(str(num), use_container_width=True, key=f"key_{num}"):
                digitar(num)
                st.rerun()

    # Linha final: 0, Backspace (⌫) e Limpar (C)
    c1, c2, c3 = st.columns(3)
    if c1.button("0", use_container_width=True):
        digitar(0)
        st.rerun()
    if c2.button("⌫", use_container_width=True):
        limpar_digito()
        st.rerun()
    if c3.button("C", use_container_width=True):
        st.session_state.resposta_atual = ""
        st.rerun()

st.divider()

# 7. Ações de Verificação e Próxima
col_v, col_p = st.columns(2)

with col_v:
    if st.button("VERIFICAR ✅", use_container_width=True, type="primary"):
        if st.session_state.resposta_atual:
            res_real = st.session_state.n1 * st.session_state.n2
            if int(st.session_state.resposta_atual) == res_real:
                st.session_state.feedback = f"✅ Correto! {res_real}"
            else:
                st.session_state.feedback = f"❌ Errado! Era {res_real}"
        else:
            st.session_state.feedback = "⚠️ Digite algo!"

with col_p:
    if st.button("PRÓXIMA ➡️", use_container_width=True):
        sortear_numeros()
        st.rerun()

# 8. Feedback Final
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)