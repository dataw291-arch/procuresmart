import streamlit as st
from app.context.router import route_message
from app.agents.procurement import handle_procurement
from app.agents.supplier import handle_supplier
from app.config.azure_openai import chat_with_ai

st.set_page_config(page_title="ProcureSmart Assistant", layout="wide")
st.title("💡 ProcureSmart Enterprise Assistant")

if "history" not in st.session_state:
    st.session_state.history = []
if "step" not in st.session_state:
    st.session_state.step = 0

user_input = st.chat_input("Ask about procurement or supplier policies...")

if user_input:
    agent = route_message(user_input)
    if agent == "procurement":
        answer = handle_procurement(user_input, st.session_state.step)
        st.session_state.step += 1
    else:
        answer = handle_supplier(user_input)

    st.session_state.history.append((user_input, answer))

# Display history
for q, a in st.session_state.history:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(a)