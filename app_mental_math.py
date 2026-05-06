import streamlit as st
import random

# 1. Configuração da página
st.set_page_config(page_title="Treino Mental Custom", page_icon="🧮")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'n1' not in st.session_state:
    st.session_state.update({
        'n1': random.randint(10, 99),
        'n2': random.randint(2, 9),
        'feedback': "",
        'contador': 0,
        'operacao_atual': "Multiplicação"
    })

# --- FUNÇÕES ---
def obter_range(opcao_texto):
    mapa = {
        "1 dígito": (2, 9),
        "2 dígitos": (10, 99),
        "3 dígitos": (100, 999),
        "4 dígitos": (1000, 9999)
    }
    return mapa.get(opcao_texto, (2, 9))

def gerar_conta():
    op = st.session_state.get('op_selector', "Multiplicação")
    d1 = st.session_state.get('d1_selector', "2 dígitos")
    d2 = st.session_state.get('d2_selector', "1 dígito")
    
    r1_min, r1_max = obter_range(d1)
    r2_min, r2_max = obter_range(d2)

    if op == "Divisão":
        # Para divisão exata: n2 é o divisor, resultado é o quociente
        # n1 será o produto deles (dividendo)
        st.session_state.n2 = random.randint(r2_min, r2_max)
        # Limitamos o quociente para não gerar números gigantescos
        # Se n1 for 4 dígitos, o quociente é ajustado proporcionalmente
        max_quociente = 100 if d1 != "4 dígitos" else 1000
        quociente = random.randint(2, max_quociente)
        st.session_state.n1 = st.session_state.n2 * quociente
    else:
        st.session_state.n1 = random.randint(r1_min, r1_max)
        st.session_state.n2 = random.randint(r2_min, r2_max)
    
    # Ajuste para subtração (evitar negativos)
    if op == "Subtração" and st.session_state.n1 < st.session_state.n2:
        st.session_state.n1, st.session_state.n2 = st.session_state.n2, st.session_state.n1
        
    st.session_state.operacao_atual = op
    st.session_state.feedback = ""
    st.session_state.contador += 1

# --- INTERFACE ---
st.title("🧮 Treino Mental Personalizado")

# Configurações em colunas
col_op, col_n1, col_n2 = st.columns(3)

opcoes_digitos = ["1 dígito", "2 dígitos", "3 dígitos", "4 dígitos"]

with col_op:
    st.selectbox("Operação:", ["Multiplicação", "Adição", "Subtração", "Divisão"], 
                 key="op_selector", on_change=gerar_conta)

with col_n1:
    st.selectbox("Dígitos do nº 1:", opcoes_digitos, index=1, 
                 key="d1_selector", on_change=gerar_conta)

with col_n2:
    st.selectbox("Dígitos do nº 2:", opcoes_digitos, index=0, 
                 key="d2_selector", on_change=gerar_conta)

st.divider()

# Mapeamento de símbolos
simbolos = {"Multiplicação": "×", "Adição": "+", "Subtração": "-", "Divisão": "÷"}
simbolo = simbolos.get(st.session_state.operacao_atual, "×")

# Pergunta
st.subheader("Resolva a conta:")
st.header(f"{st.session_state.n1} {simbolo} {st.session_state.n2} = ?")

# Campo de Resposta
resposta = st.text_input(
    "Sua resposta:", 
    key=f"input_{st.session_state.contador}",
    placeholder="Digite o resultado..."
)

# Botões
c1, c2 = st.columns(2)
with c1:
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

with c2:
    if st.button("Próxima Conta ➡️", use_container_width=True):
        gerar_conta()
        st.rerun()

# Feedback
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)