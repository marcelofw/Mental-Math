import streamlit as st
import random

# 1. Configuração da página
st.set_page_config(page_title="Treino Mental", page_icon="🧮")

# --- INICIALIZAÇÃO DO ESTADO ---
# Isso garante que as variáveis existam antes da interface carregar
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""
    st.session_state.contador = 0
    st.session_state.operacao_atual = "Multiplicação"

# --- FUNÇÕES ---
def gerar_conta():
    # Busca os valores dos widgets ou usa o padrão caso ainda não existam
    modo = st.session_state.get('modo_selector', "Médio (2 dígitos)")
    op = st.session_state.get('op_selector', "Multiplicação")
    
    if "1 dígito" in modo:
        r_min, r_max = 2, 9
    elif "2 dígitos" in modo:
        r_min, r_max = 10, 99
    else:
        r_min, r_max = 100, 999

    st.session_state.n1 = random.randint(r_min, r_max)
    st.session_state.n2 = random.randint(r_min, r_max)
    
    # Evitar números negativos na subtração
    if op == "Subtração" and st.session_state.n1 < st.session_state.n2:
        st.session_state.n1, st.session_state.n2 = st.session_state.n2, st.session_state.n1
        
    st.session_state.operacao_atual = op
    st.session_state.feedback = ""
    st.session_state.contador += 1

# --- INTERFACE ---
st.title("🧮 Desafio de Cálculo Mental")

col_config1, col_config2 = st.columns(2)

with col_config1:
    st.selectbox(
        "Operação:", 
        ["Multiplicação", "Adição", "Subtração"], 
        key="op_selector", 
        on_change=gerar_conta
    )

with col_config2:
    st.selectbox(
        "Dificuldade:", 
        ["Fácil (1 dígito)", "Médio (2 dígitos)", "Difícil (3 dígitos)"], 
        index=1,
        key="modo_selector", 
        on_change=gerar_conta
    )

st.divider()

# Mapeamento de símbolos
simbolos = {"Multiplicação": "×", "Adição": "+", "Subtração": "-"}
simbolo = simbolos.get(st.session_state.operacao_atual, "×")

# Pergunta
st.header(f"Quanto é {st.session_state.n1} {simbolo} {st.session_state.n2}?")

# Campo de Resposta
# O uso da key dinâmica limpa o campo automaticamente na próxima conta
resposta = st.text_input(
    "Sua resposta:", 
    key=f"input_{st.session_state.contador}",
    placeholder="Digite o resultado..."
)

# Botões
col_b1, col_b2 = st.columns(2)

with col_b1:
    if st.button("Verificar ✅", use_container_width=True, type="primary"):
        if resposta:
            try:
                res_user = int(resposta)
                n1, n2 = st.session_state.n1, st.session_state.n2
                op = st.session_state.operacao_atual
                
                if op == "Multiplicação": real = n1 * n2
                elif op == "Adição": real = n1 + n2
                else: real = n1 - n2
                
                if res_user == real:
                    st.session_state.feedback = f"✅ Correto! {n1} {simbolo} {n2} = {real}"
                else:
                    st.session_state.feedback = f"❌ Errado! O resultado era {real}"
            except ValueError:
                st.session_state.feedback = "⚠️ Digite apenas números inteiros!"
        else:
            st.session_state.feedback = "🤔 Digite algo primeiro."

with col_b2:
    if st.button("Próxima Conta ➡️", use_container_width=True):
        gerar_conta()
        st.rerun()

# Exibição do Feedback
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)