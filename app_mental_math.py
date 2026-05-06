import streamlit as st
import random
import time

# 1. Configuração da página
st.set_page_config(page_title="Treino Mental Pro", page_icon="🧮", layout="centered")

# --- INICIALIZAÇÃO DO ESTADO ---
# Usamos o tempo para garantir que a semente do random seja sempre única
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
    # Resetar a semente para garantir números novos em cada clique
    random.seed(time.time())
    
    op = st.session_state.get('op_selector', "Multiplicação")
    d1_txt = st.session_state.get('d1_selector', "2 dígitos")
    d2_txt = st.session_state.get('d2_selector', "1 dígito")
    
    r1_min, r1_max = obter_range(d1_txt)
    r2_min, r2_max = obter_range(d2_txt)

    if op == "Divisão":
        # Sorteamos o n2 (divisor) dentro do seu range
        n2_temp = random.randint(r2_min, r2_max)
        
        # Trava de segurança: n2 não pode ser maior que o valor máximo do n1
        if n2_temp > r1_max:
            n2_temp = random.randint(2, r1_max)
        
        # Sorteamos um n1 temporário para basear o cálculo do múltiplo
        n1_base = random.randint(r1_min, r1_max)
        
        # Calculamos o múltiplo mais próximo para ser divisão exata
        quociente = n1_base // n2_temp
        if quociente == 0: quociente = 1
        
        n1_final = quociente * n2_temp
        
        # Garante que n1_final não saia do range de dígitos escolhido
        if n1_final < r1_min:
            n1_final = (r1_min // n2_temp + 1) * n2_temp
        if n1_final > r1_max:
            n1_final = (r1_max // n2_temp) * n2_temp
            
        st.session_state.n1 = n1_final
        st.session_state.n2 = n2_temp
    else:
        # Adição, Subtração e Multiplicação
        st.session_state.n1 = random.randint(r1_min, r1_max)
        st.session_state.n2 = random.randint(r2_min, r2_max)
    
    # Evitar resultados negativos na subtração
    if op == "Subtração" and st.session_state.n1 < st.session_state.n2:
        st.session_state.n1, st.session_state.n2 = st.session_state.n2, st.session_state.n1
        
    st.session_state.operacao_atual = op
    st.session_state.feedback = ""
    st.session_state.contador += 1

# --- INTERFACE ---
st.title("🧮 Treino Mental Personalizado")
st.markdown("Configure sua dificuldade e pratique o cálculo rápido!")

# Painel de Configuração
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

# Exibição da Conta
simbolos = {"Multiplicação": "×", "Adição": "+", "Subtração": "-", "Divisão": "÷"}
simbolo = simbolos.get(st.session_state.operacao_atual, "×")

st.markdown("<h3 style='text-align: center;'>Quanto é:</h3>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center;'>{st.session_state.n1} {simbolo} {st.session_state.n2}</h1>", unsafe_allow_html=True)

# Entrada de Dados
# A key dinâmica limpa o input a cada nova conta
resposta = st.text_input("Sua resposta:", key=f"input_{st.session_state.contador}", placeholder="Digite e aperte Enter")

# Botões de Ação
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("Verificar ✅", use_container_width=True, type="primary"):
        if resposta:
            try:
                res_user = int(resposta)
                n1, n2 = st.session_state.n1, st.session_state.n2
                op = st.session_state.operacao_atual
                
                # Cálculo do resultado real
                if op == "Multiplicação": real = n1 * n2
                elif op == "Adição": real = n1 + n2
                elif op == "Subtração": real = n1 - n2
                else: real = n1 // n2
                
                if res_user == real:
                    st.session_state.feedback = f"✅ Correto! {n1} {simbolo} {n2} = {real}"
                else:
                    st.session_state.feedback = f"❌ Errado! O resultado correto era {real}"
            except ValueError:
                st.session_state.feedback = "⚠️ Por favor, digite apenas números inteiros!"
        else:
            st.session_state.feedback = "🤔 Digite um valor antes de verificar."

with col_btn2:
    if st.button("Próxima Conta ➡️", use_container_width=True):
        gerar_conta()
        st.rerun()

# Exibição do Feedback (abaixo dos botões)
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)