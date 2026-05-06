import streamlit as st
import random

# 1. Configuração da página
st.set_page_config(page_title="Treino Mental Multi-Operações", page_icon="🧮")

# --- INICIALIZAÇÃO DO ESTADO ---
opcoes_modo = ["Fácil (1 dígito)", "Médio (2 dígitos)", "Difícil (3 dígitos)"]
opcoes_operacao = ["Multiplicação", "Adição", "Subtração"]

if 'n1' not in st.session_state:
    st.session_state.update({
        'n1': 0,
        'n2': 0,
        'feedback': "",
        'contador': 0,
        'operacao_atual': "Multiplicação"
    })

# --- FUNÇÕES ---
def gerar_conta():
    modo = st.session_state.modo_selector
    op = st.session_state.op_selector
    
    # Define os intervalos baseado no nível
    if "1 dígito" in modo:
        range_min, range_max = 2, 9
    elif "2 dígitos" in modo:
        range_min, range_max = 10, 99
    else:
        range_min, range_max = 100, 999

    st.session_state.n1 = random.randint(range_min, range_max)
    st.session_state.n2 = random.randint(range_min, range_max)
    
    # Garantir que subtração não resulte em números negativos (opcional, para facilitar)
    if op == "Subtração" and st.session_state.n1 < st.session_state.n2:
        st.session_state.n1, st.session_state.n2 = st.session_state.n2, st.session_state.n1
        
    st.session_state.operacao_atual = op
    st.session_state.feedback = ""
    st.session_state.contador += 1

# Inicializa a primeira conta se os números forem 0
if st.session_state.n1 == 0:
    # Definimos valores padrão para evitar erro no primeiro carregamento
    st.session_state.n1, st.session_state.n2 = 10, 10

# --- INTERFACE ---
st.title("🧮 Desafio de Cálculo Mental")

col_config1, col_config2 = st.columns(2)

with col_config1:
    st.selectbox("Operação:", opcoes_operacao, key="op_selector", on_change=gerar_conta)

with col_config2:
    st.selectbox("Dificuldade:", opcoes_modo, key="modo_selector", on_change=gerar_conta)

st.divider()

# Mapeamento de símbolos
simbolos = {"Multiplicação": "×", "Adição": "+", "Subtração": "-"}
simbolo = simbolos[st.session_state.operacao_atual]

# Pergunta
st.header(f"Quanto é {st.session_state.n1} {simbolo} {st.session_state.n2}?")

# Campo de Resposta
resposta = st.text_input(
    "Sua resposta:", 
    key=f"input_{st.session_state.contador}",
    placeholder="Digite o resultado e aperte Enter"
)

# Lógica de Verificação
def verificar():
    if resposta:
        try:
            n1, n2 = st.session_state.n1, st.session_state.n2
            op = st.session_state.operacao_atual
            
            if op == "Multiplicação": real = n1 * n2
            elif op == "Adição": real = n1 + n2
            else: real = n1 - n2
            
            if int(resposta) == real:
                st.session_state.feedback = f"✅ Correto! {n1} {simbolo} {n2} = {real}"
            else:
                st.session_state.feedback = f"❌ Errado! O resultado era {real}"
        except ValueError:
            st.session_state.feedback = "⚠️ Digite apenas números inteiros!"
    else:
        st.session_state.feedback = "🤔 Digite algo primeiro."

# Botões
col_b1, col_b2 = st.columns(2)

with col_b1:
    if st.button("Verificar ✅", use_container_width=True, type="primary"):
        verificar()

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