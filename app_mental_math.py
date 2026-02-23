import streamlit as st
import random

# 1. Configuração da página
st.set_page_config(page_title="Treino Mental", page_icon="🔢")

# 2. Inicialização do Estado (Garante que o app não quebre ao abrir)
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""
    st.session_state.contador = 0  # Usado para resetar o campo de texto

def gerar_conta():
    if st.session_state.modo == "1 x 2 dígitos":
        st.session_state.n1 = random.randint(2, 9)
    else:
        st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""
    st.session_state.contador += 1  # Muda a key do input, limpando-o

# 3. Interface
st.title("🔢 Desafio de Multiplicação")

# Seletor de Modo
st.radio(
    "Escolha o nível:",
    ["2 x 2 dígitos", "1 x 2 dígitos"],
    key="modo",
    on_change=gerar_conta,
    horizontal=True
)

st.divider()

# Pergunta
st.header(f"Quanto é {st.session_state.n1} × {st.session_state.n2}?")

# Campo de Resposta (A key muda toda vez que geramos uma conta nova)
# No Android, 'type="default"' com 'label_visibility' ajuda na limpeza visual
resposta = st.text_input(
    "Sua resposta:", 
    key=f"input_{st.session_state.contador}",
    placeholder="Digite o resultado aqui..."
)

# 4. Botões de Ação
col1, col2 = st.columns(2)

with col1:
    if st.button("Verificar ✅", use_container_width=True, type="primary"):
        if resposta:
            try:
                real = st.session_state.n1 * st.session_state.n2
                if int(resposta) == real:
                    st.session_state.feedback = f"✅ Correto! {real}"
                else:
                    st.session_state.feedback = f"❌ Errado! Era {real}"
            except ValueError:
                st.session_state.feedback = "⚠️ Digite apenas números!"
        else:
            st.session_state.feedback = "🤔 Escreva algo antes."

with col2:
    if st.button("Próxima Conta ➡️", use_container_width=True):
        gerar_conta()
        st.rerun()

# 5. Feedback
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)