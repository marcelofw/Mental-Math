import streamlit as st
import random

# 1. Configuração da página
st.set_page_config(page_title="Treino Mental Custom", page_icon="🧮")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'n1' not in st.session_state:
    st.session_state.update({
        'n1': 12,
        'n2': 3,
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
    d1_txt = st.session_state.get('d1_selector', "2 dígitos")
    d2_txt = st.session_state.get('d2_selector', "1 dígito")
    
    r1_min, r1_max = obter_range(d1_txt)
    r2_min, r2_max = obter_range(d2_txt)

    if op == "Divisão":
        # 1. Sorteamos o n2 (Divisor) primeiro
        n2_temp = random.randint(r2_min, r2_max)
        
        # 2. Sorteamos um n1 (Dividendo) temporário
        n1_temp = random.randint(r1_min, r1_max)
        
        # 3. Trava de Sanidade: Se o divisor for maior que o dividendo (ex: 1 dígito / 4 dígitos)
        # nós forçamos o divisor a ser menor que o dividendo para manter os dígitos escolhidos.
        if n2_temp > r1_max:
             # Se o usuário pediu divisor de 4 dígitos mas dividendo de 1, 
             # reduzimos o divisor para o máximo do dividendo
             n2_temp = random.randint(2, r1_max)
        
        # 4. Ajuste para divisão exata
        # Encontramos o quociente inteiro
        quociente = n1_temp // n2_temp
        if quociente == 0: quociente = 1
        
        n1_ajustado = quociente * n2_temp
        
        # 5. Garante que n1_ajustado ainda está no range de dígitos do d1
        if n1_ajustado < r1_min:
            n1_ajustado = (r1_min // n2_temp + 1) * n2_temp
        
        # Se mesmo assim passar do range (ex: 999 + algo), pegamos o múltiplo anterior
        if n1_ajustado > r1_max:
            n1_ajustado = (r1_max // n2_temp) * n2_temp
            
        st.session_state.n1 = n1_ajustado
        st.session_state.n2 = n2_temp
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

col_op, col_n1, col_n2 = st.columns(3)
opcoes_digitos = ["1 dígito", "2 dígitos", "3 dígitos", "4 dígitos"]

with col_op:
    st.selectbox("Operação:", ["Multiplicação", "Adição", "Subtração", "Divisão"], 
                 key="op_selector", on_change=gerar_conta)

with col_n1:
    st.selectbox("Dígitos do nº 1 (Dividendo):", opcoes_digitos, index=1, 
                 key="d1_selector", on_change=gerar_conta)

with col_n2:
    st.selectbox("Dígitos do nº 2 (Divisor):", opcoes_digitos, index=0, 
                 key="d2_selector", on_change=gerar_conta)

st.divider()

simbolos = {"Multiplicação": "×", "Adição": "+", "Subtração": "-", "Divisão": "÷"}
simbolo = simbolos.get(st.session_state.operacao_atual, "×")

st.subheader("Resolva a conta:")
st.header(f"{st.session_state.n1} {simbolo} {st.session_state.n2} = ?")

resposta = st.text_input("Sua resposta:", key=f"input_{st.session_state.contador}")

c1, c2 = st.columns(2)
with c1:
    if st.button("Verificar ✅", use_container_width=True, type="primary"):
        if resposta:
            try:
                res_user = int(resposta)
                n1, n2 = st.session_state.n1, st.session_state.n2
                op = st.session_state.operacao_atual
                
                real = n1 * n2 if op == "Multiplicação" else n1 + n2 if op == "Adição" else n1 - n2 if op == "Subtração" else n1 // n2
                
                if res_user == real:
                    st.session_state.feedback = f"✅ Correto! {n1} {simbolo} {n2} = {real}"
                else:
                    st.session_state.feedback = f"❌ Errado! Era {real}"
            except ValueError:
                st.session_state.feedback = "⚠️ Digite apenas números!"
        else:
            st.session_state.feedback = "🤔 Digite algo."

with c2:
    if st.button("Próxima Conta ➡️", use_container_width=True):
        gerar_conta()
        st.rerun()

if st.session_state.feedback:
    if "✅" in st.session_state.feedback: st.success(st.session_state.feedback)
    else: st.error(st.session_state.feedback)