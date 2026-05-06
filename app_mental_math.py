import streamlit as st
import random

# 1. Configuração da página
st.set_page_config(page_title="Treino Mental Pro", page_icon="🧮")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""
    st.session_state.contador = 0
    st.session_state.operacao_atual = "Multiplicação"

# --- FUNÇÕES ---
def gerar_conta():
    modo = st.session_state.get('modo_selector', "Médio (2 dígitos)")
    op = st.session_state.get('op_selector', "Multiplicação")
    
    # Define os intervalos baseado no nível
    ranges = {
        "Fácil (1 dígito)": (2, 9),
        "Médio (2 dígitos)": (10, 99),
        "Difícil (3 dígitos)": (100, 999),
        "Expert (4 dígitos)": (1000, 9999)
    }
    r_min, r_max = ranges.get(modo, (10, 99))

    if op == "Divisão":
        # Lógica de divisão segura para evitar o erro de range vazio
        if modo == "Expert (4 dígitos)":
            # Para 4 dígitos, sorteamos um divisor de 2 ou 3 dígitos para ser viável
            st.session_state.n2 = random.randint(10, 500)
        elif modo == "Difícil (3 dígitos)":
            st.session_state.n2 = random.randint(10, 100)
        else:
            st.session_state.n2 = random.randint(r_min, r_max)
            
        # O resultado (quociente) será sempre simples para permitir cálculo mental
        resultado_inteiro = random.randint(2, 20 if "dígito" in modo else 50)
        st.session_state.n1 = st.session_state.n2 * resultado_inteiro
    else:
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
        ["Multiplicação", "Adição", "Subtração", "Divisão"], 
        key="op_selector", 
        on_change=gerar_conta
    )

with col_config2:
    st.selectbox(
        "Dificuldade:", 
        ["Fácil (1 dígito)", "Médio (2 dígitos)", "Difícil (3 dígitos)", "Expert (4 dígitos)"], 
        index=1,
        key="modo_selector", 
        on_change=gerar_conta
    )

st.divider()

# Mapeamento de símbolos
simbolos = {"Multiplicação": "×", "Adição": "+", "Subtração": "-", "Divisão": "÷"}
simbolo = simbolos.get(st.session_state.operacao_atual, "×")

# Pergunta
st.header(f"Quanto é {st.session_state.n1} {simbolo} {st.session_state.n2}?")

# Campo de Resposta
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
                elif op == "Subtração": real = n1 - n2
                else: real = n1 // n2
                
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

# Feedback
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)