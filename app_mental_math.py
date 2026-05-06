import streamlit as st
import random
import time

# 1. Configuração da página
st.set_page_config(page_title="Treino Mental Pro", page_icon="🧮", layout="centered")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'n1' not in st.session_state:
    random.seed(time.time())
    st.session_state.update({
        'n1': random.randint(10, 99),
        'n2': random.randint(2, 9),
        'feedback': "",
        'contador': 0,
        'operacao_atual': "Multiplicação"
    })

# --- FUNÇÕES DE APOIO ---
def obter_range(opcao_texto):
    mapa = {
        "1 dígito": (2, 9),
        "2 dígitos": (10, 99),
        "3 dígitos": (100, 999),
        "4 dígitos": (1000, 9999)
    }
    return mapa.get(opcao_texto, (2, 9))

def gerar_conta():
    random.seed(time.time())
    
    op = st.session_state.get('op_selector', "Multiplicação")
    d1_txt = st.session_state.get('d1_selector', "2 dígitos")
    d2_txt = st.session_state.get('d2_selector', "1 dígito")
    
    r1_min, r1_max = obter_range(d1_txt)
    r2_min, r2_max = obter_range(d2_txt)

    # Agora sorteia n1 e n2 puramente pelos dígitos escolhidos
    st.session_state.n1 = random.randint(r1_min, r1_max)
    st.session_state.n2 = random.randint(r2_min, r2_max)
    
    # Ajuste para evitar negativos na subtração
    if op == "Subtração" and st.session_state.n1 < st.session_state.n2:
        st.session_state.n1, st.session_state.n2 = st.session_state.n2, st.session_state.n1
        
    st.session_state.operacao_atual = op
    st.session_state.feedback = ""
    st.session_state.contador += 1

# --- INTERFACE ---
st.title("🧮 Treino Mental: Números Reais")

with st.expander("⚙️ Configurações do Desafio", expanded=True):
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

simbolos = {"Multiplicação": "×", "Adição": "+", "Subtração": "-", "Divisão": "÷"}
simbolo = simbolos.get(st.session_state.operacao_atual, "×")

if st.session_state.operacao_atual == "Divisão":
    st.info("💡 Para divisões não exatas, use **2 casas decimais** (Ex: 3.33)")

st.markdown("<h3 style='text-align: center;'>Resolva:</h3>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center;'>{st.session_state.n1} {simbolo} {st.session_state.n2}</h1>", unsafe_allow_html=True)

# Entrada de dados (Aceita ponto ou vírgula)
resposta = st.text_input("Sua resposta:", key=f"input_{st.session_state.contador}")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("Verificar ✅", use_container_width=True, type="primary"):
        if resposta:
            try:
                # Converte vírgula em ponto para o Python entender como float
                res_limpa = resposta.replace(',', '.')
                res_user = float(res_limpa)
                
                n1, n2 = st.session_state.n1, st.session_state.n2
                op = st.session_state.operacao_atual
                
                # Cálculo do resultado real
                if op == "Multiplicação": real = float(n1 * n2)
                elif op == "Adição": real = float(n1 + n2)
                elif op == "Subtração": real = float(n1 - n2)
                else: real = round(n1 / n2, 2) # Arredonda para 2 casas
                
                if abs(res_user - real) < 0.001: # Comparação segura para floats
                    st.session_state.feedback = f"✅ Correto! O resultado é {real}"
                else:
                    st.session_state.feedback = f"❌ Errado! O resultado exato era {real}"
            except ValueError:
                st.session_state.feedback = "⚠️ Digite um número válido (ex: 10.5 ou 10,5)"
        else:
            st.session_state.feedback = "🤔 Digite algo primeiro."

with col_btn2:
    if st.button("Próxima Conta ➡️", use_container_width=True):
        gerar_conta()
        st.rerun()

if st.session_state.feedback:
    if "✅" in st.session_state.feedback: st.success(st.session_state.feedback)
    else: st.error(st.session_state.feedback)