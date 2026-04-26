import streamlit as st
import random

# 1. Configuração da página
st.set_page_config(page_title="Treino Mental", page_icon="🔢")

# --- INICIALIZAÇÃO ROBUSTA DO ESTADO ---
# Usamos um loop para garantir que tudo exista antes de carregar a interface
opcoes_modo = ["1 x 2 dígitos", "2 x 2 dígitos", "1 x 3 dígitos", "2 x 3 dígitos"]

for key, value in {
    'n1': random.randint(10, 99),
    'n2': random.randint(10, 99),
    'feedback': "",
    'contador': 0,
    'modo': "2 x 2 dígitos"
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- FUNÇÕES ---
def gerar_conta():
    modo = st.session_state.modo_selector
    
    if modo == "1 x 2 dígitos":
        st.session_state.n1 = random.randint(2, 9)
        st.session_state.n2 = random.randint(10, 99)
    elif modo == "2 x 2 dígitos":
        st.session_state.n1 = random.randint(10, 99)
        st.session_state.n2 = random.randint(10, 99)
    elif modo == "1 x 3 dígitos":
        st.session_state.n1 = random.randint(2, 9)
        st.session_state.n2 = random.randint(100, 999)
    elif modo == "2 x 3 dígitos":
        st.session_state.n1 = random.randint(10, 99)
        st.session_state.n2 = random.randint(100, 999)
    
    st.session_state.feedback = ""
    st.session_state.contador += 1

# --- INTERFACE ---
st.title("🔢 Desafio de Multiplicação")

# Radio para trocar o modo
st.radio(
    "Escolha o nível:",
    opcoes_modo,
    key="modo_selector",  # Chave interna para o widget
    on_change=gerar_conta,
    horizontal=True
)

st.divider()

# Pergunta
st.header(f"Quanto é {st.session_state.n1} × {st.session_state.n2}?")

# Campo de Resposta (A key muda via contador para limpar o campo)
resposta = st.text_input(
    "Sua resposta:", 
    key=f"input_{st.session_state.contador}",
    placeholder="Digite o resultado..."
)

# Botões
col1, col2 = st.columns(2)

with col1:
    if st.button("Verificar ✅", use_container_width=True, type="primary"):
        if resposta:
            try:
                real = st.session_state.n1 * st.session_state.n2
                if int(resposta) == real:
                    st.session_state.feedback = f"✅ Correto! {st.session_state.n1} × {st.session_state.n2} = {real}"
                else:
                    st.session_state.feedback = f"❌ Errado! Era {real}"
            except ValueError:
                st.session_state.feedback = "⚠️ Digite apenas números!"
        else:
            st.session_state.feedback = "🤔 Digite algo primeiro."

with col2:
    if st.button("Próxima Conta ➡️", use_container_width=True):
        gerar_conta()
        st.rerun()

# Feedback
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)