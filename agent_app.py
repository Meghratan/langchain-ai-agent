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

st.set_page_config(
    page_title="L Agent — AI Detective",
    page_icon="🧠",
    layout="centered"
)

# ── Claude-inspired CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Styrene+A:wght@400;500&family=Copernicus:wght@400;600&display=swap');
/* fallback stack if custom fonts blocked */

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Söhne', 'ui-sans-serif', system-ui, -apple-system, sans-serif;
    background-color: #f9f7f4 !important;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 6rem !important;
    max-width: 720px !important;
}

/* ── Page title ── */
.page-header {
    text-align: center;
    margin-bottom: 2rem;
}
.page-header h1 {
    font-size: 2rem;
    font-weight: 600;
    color: #1a1a1a;
    letter-spacing: -0.02em;
    margin: 0 0 0.25rem;
}
.page-header p {
    font-size: 0.85rem;
    color: #9b8fa6;
    margin: 0;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Message rows ── */
.msg-row {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
    animation: fadeSlideIn 0.25s ease both;
}
.msg-row.user  { flex-direction: row-reverse; }

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0);   }
}

/* ── Avatars ── */
.avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.avatar.user      { background: #cf6e42; }
.avatar.assistant { background: #e8e2dc; }

/* ── Bubbles ── */
.bubble {
    max-width: 82%;
    padding: 0.75rem 1rem;
    border-radius: 18px;
    font-size: 0.95rem;
    line-height: 1.6;
    color: #1a1a1a;
}
.bubble.user {
    background: #cf6e42;
    color: #fff;
    border-bottom-right-radius: 4px;
}
.bubble.assistant {
    background: #ffffff;
    border: 1px solid #e8e2dc;
    border-bottom-left-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

/* ── Chat input override ── */
.stChatInput > div {
    border-radius: 14px !important;
    border: 1.5px solid #ddd7d0 !important;
    background: #ffffff !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}
.stChatInput textarea {
    font-size: 0.95rem !important;
    color: #1a1a1a !important;
}
.stChatInput button {
    background: #cf6e42 !important;
    border-radius: 10px !important;
}

/* Hide default st.chat_message wrappers – we draw our own */
.stChatMessage { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>🧠 L Agent — AI Detective</h1>
    <p>LangChain · Gemini · SerpAPI</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Render history ───────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    icon = "👤" if role == "user" else "🤖"
    st.markdown(f"""
    <div class="msg-row {role}">
        <div class="avatar {role}">{icon}</div>
        <div class="bubble {role}">{content}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Input ────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask something…")

if user_input:
    # Append & show user bubble immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"""
    <div class="msg-row user">
        <div class="avatar user">👤</div>
        <div class="bubble user">{user_input}</div>
    </div>
    """, unsafe_allow_html=True)

    # Call agent
    with st.spinner(""):
        response, st.session_state.chat_history = ask_agent(
            user_input, st.session_state.chat_history
        )

    # Show assistant bubble
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(f"""
    <div class="msg-row assistant">
        <div class="avatar assistant">🤖</div>
        <div class="bubble assistant">{response}</div>
    </div>
    """, unsafe_allow_html=True)