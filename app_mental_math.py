import streamlit as st
import random

# 1. Configuração inicial
st.set_page_config(page_title="Cálculo Mental", page_icon="🔢")

# 2. Inicialização do estado
if 'n1' not in st.session_state:
    st.session_state.n1 = random.randint(10, 99)
    st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""

# 3. Função para gerar nova conta (Sem tentar limpar a key do widget aqui)
def proxima_conta(modo):
    if modo == "1 x 2 dígitos":
        st.session_state.n1 = random.randint(2, 9)
        st.session_state.n2 = random.randint(10, 99)
    else:
        st.session_state.n1 = random.randint(10, 99)
        st.session_state.n2 = random.randint(10, 99)
    st.session_state.feedback = ""
    # Em vez de limpar a key, apenas forçamos o rerun. 
    # Para o campo zerar, vamos usar um truque de ID no widget abaixo.

# 4. Interface
modo_treino = st.radio(
    "Dificuldade:",
    ("2 x 2 dígitos", "1 x 2 dígitos"),
    horizontal=True
)

st.subheader(f"Quanto é {st.session_state.n1} × {st.session_state.n2}?")

# Truque: Usamos uma key que muda ou simplesmente não forçamos o valor.
# Para limpar o campo no Android facilmente, o botão 'Próxima Conta' dará o refresh.
resposta = st.text_input("Resultado:", key="campo_resposta")

col1, col2 = st.columns(2)

with col1:
    if st.button("Verificar"):
        if resposta:
            try:
                res_real = st.session_state.n1 * st.session_state.n2
                if int(resposta) == res_real:
                    st.session_state.feedback = f"✅ Correto! ({res_real})"
                else:
                    st.session_state.feedback = f"❌ Errado! Era {res_real}"
            except ValueError:
                st.session_state.feedback = "⚠️ Digite apenas números."
        else:
            st.session_state.feedback = "🤔 Digite algo."

with col2:
    if st.button("Próxima Conta ➡️"):
        proxima_conta(modo_treino)
        # Ao rodar o rerun, o widget é recriado. 
        # Para garantir que ele limpe, podemos usar o fragmento de limpeza do Streamlit:
        st.rerun()

if st.session_state.feedback:
    st.write(st.session_state.feedback)