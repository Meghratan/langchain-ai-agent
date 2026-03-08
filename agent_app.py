# import streamlit as st
# from agent_core import ask_agent

# st.set_page_config(page_title="AI Agent", page_icon="🤖")

# st.title("🤖 My AI Agent")
# st.write("Ask anything...")

# # Search bar
# user_input = st.text_input("Enter your query:")

# if st.button("Search"):
#     if user_input:
#         with st.spinner("Thinking..."):
#             result = ask_agent(user_input)
#         st.success("Answer:")
#         st.write(result)
#     else:
#         st.warning("Please enter a question.")

# new window memory style
import streamlit as st
from agent_core import ask_agent

st.set_page_config(page_title="AI Agent", layout="wide")

st.title("MAGGIE YOUR AI Agent")

if "history" not in st.session_state:
    st.session_state.history = []

# Show chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
user_input = st.chat_input("Ask something...")

if user_input:

    answer, st.session_state.history = ask_agent(
        user_input,
        st.session_state.history
    )

    with st.chat_message("assistant"):
        st.write(answer)