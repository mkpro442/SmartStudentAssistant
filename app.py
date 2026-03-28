# =============================================================
#  app.py  —  Smart Student Chatbot  (Streamlit + Groq)
# =============================================================
#  Local run:   streamlit run app.py
#  Deploy:      Push to GitHub → connect on share.streamlit.io
# =============================================================

import streamlit as st
from datetime import datetime
from groq_client import GroqClient

# ── Page config (MUST be first Streamlit call) ────────────────
st.set_page_config(
    page_title="Smart Student Chatbot",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Overall background ---- */
.stApp { background-color: #1e1e2e; }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background-color: #181825;
}
[data-testid="stSidebar"] * { color: #cdd6f4 !important; }

/* ---- Main text ---- */
html, body, [class*="css"] { color: #cdd6f4; }

/* ---- Chat input box ---- */
.stChatInput textarea {
    background-color: #313244 !important;
    color: #cdd6f4 !important;
    border: 1px solid #45475a !important;
    border-radius: 12px !important;
}

/* ---- User message bubble ---- */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]) {
    border-radius: 16px;
}

/* ---- Buttons ---- */
.stButton > button {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 8px;
}
.stButton > button:hover {
    background-color: #89b4fa;
    color: #1e1e2e;
    border-color: #89b4fa;
}

/* ---- Suggestion chips row ---- */
div[data-testid="column"] .stButton > button {
    width: 100%;
    font-size: 13px;
    padding: 6px 10px;
}

/* ---- Metric cards ---- */
[data-testid="stMetric"] {
    background-color: #313244;
    border-radius: 10px;
    padding: 10px 16px;
}

/* ---- Expander ---- */
details { border: 1px solid #45475a !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# =============================================================
#  Session state initialisation
# =============================================================
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []       # displayed messages {role, content, time}
    if "history" not in st.session_state:
        st.session_state.history  = []       # Groq API history {role, text}
    if "client" not in st.session_state:
        st.session_state.client   = None
    if "api_key" not in st.session_state:
        st.session_state.api_key  = ""
    if "total_messages" not in st.session_state:
        st.session_state.total_messages = 0
    if "session_start" not in st.session_state:
        st.session_state.session_start = datetime.now().strftime("%I:%M %p")

init_state()


# =============================================================
#  Sidebar
# =============================================================
with st.sidebar:
    st.markdown("## 🎓 Student Chatbot")
    st.markdown("Powered by **Llama 3.3 70B (Groq)** · Free tier")
    st.divider()

    # ── API Key input ──────────────────────────────────────────
    st.markdown("### 🔑 API Key")

    # Try Streamlit Cloud secrets first (for deployed app)
    cloud_key = ""
    try:
        cloud_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    if cloud_key:
        st.success("✅ API key loaded from Streamlit secrets!")
        active_key = cloud_key
    else:
        api_input = st.text_input(
            "Enter your Groq API key",
            type="password",
            placeholder="gsk_...",
            help="Get a free key at https://console.groq.com",
        )
        if api_input:
            st.session_state.api_key = api_input
        active_key = st.session_state.api_key

        if not active_key:
            st.info("👆 Add your free Groq API key above to start chatting.\n\n"
                    "Get one free at [console.groq.com](https://console.groq.com)")

    # Create / update client when key is available
    if active_key:
        if st.session_state.client is None:
            with st.spinner("Connecting to Groq…"):
                st.session_state.client = GeminiClient(api_key=active_key)
            st.success("✅ Connected!")

    st.divider()

    # ── Session stats ──────────────────────────────────────────
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    col1.metric("Messages", st.session_state.total_messages)
    col2.metric("Started", st.session_state.session_start)

    st.divider()

    # ── Controls ───────────────────────────────────────────────
    st.markdown("### ⚙️ Controls")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages       = []
        st.session_state.history        = []
        st.session_state.total_messages = 0
        st.rerun()

    st.divider()

    # ── Topics cheat sheet ────────────────────────────────────
    with st.expander("💡 What can I ask?"):
        st.markdown("""
- 📚 Study techniques & tips
- 📝 Exam prep & revision
- ⏰ Time management
- 💪 Motivation & procrastination
- 🗒️ Note-taking methods
- 🧠 Stress & mental health
- 💼 Career & internships
- 💻 Coding & Python help
- 📐 Maths for AI/ML
- 🎓 College life & friendships
        """)

    # ── Get API key link ──────────────────────────────────────
    st.markdown(
        "🔗 [Get free Groq API key](https://console.groq.com)",
        unsafe_allow_html=False
    )


# =============================================================
#  Main chat area
# =============================================================
st.markdown("# 🎓 Smart Student Assistant")
st.markdown("*Ask me anything about studying, exams, career, coding, or college life!*")
st.divider()

# ── Suggestion chips ──────────────────────────────────────────
SUGGESTIONS = [
    "How do I study effectively? 📚",
    "Tips for exam prep 📝",
    "I feel lazy and unmotivated 😴",
    "How to get an internship? 💼",
    "Help me debug my Python code 💻",
    "I'm stressed about college 😰",
]

# Only show chips if no messages yet
if not st.session_state.messages:
    st.markdown("**✨ Quick start — tap a topic:**")
    cols = st.columns(3)
    for i, suggestion in enumerate(SUGGESTIONS):
        if cols[i % 3].button(suggestion, key=f"chip_{i}"):
            # Treat chip click as a user message
            st.session_state._pending_input = suggestion

# ── Chat history display ──────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"],
                         avatar="🧑‍🎓" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])
        st.caption(f"*{msg['time']}*")

# ── Welcome message (first load) ──────────────────────────────
if not st.session_state.messages and st.session_state.client:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(
            "👋 Hello! I'm your **Smart Student Assistant**, powered by Groq & Llama 3.3.\n\n"
            "I can help you with studying, exams, time management, motivation, "
            "coding, career advice, and a lot more! What's on your mind today? 😊"
        )


# =============================================================
#  Handle input  (both text box and chip clicks)
# =============================================================
def handle_message(user_input: str):
    """Process a user message: display it, call Groq, display reply."""
    if not st.session_state.client:
        st.error("⚠️ Please enter your Groq API key in the sidebar first!")
        return

    timestamp = datetime.now().strftime("%I:%M %p")

    # ── Show user message ──────────────────────────────────────
    st.session_state.messages.append({
        "role":    "user",
        "content": user_input,
        "time":    timestamp,
    })
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_input)
        st.caption(f"*{timestamp}*")

    # ── Call Groq ──────────────────────────────────────────────
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking…"):
            reply = st.session_state.client.chat(
                user_input,
                st.session_state.history
            )
        st.markdown(reply)
        reply_time = datetime.now().strftime("%I:%M %p")
        st.caption(f"*{reply_time}*")

    # ── Update Groq history (multi-turn memory) ────────────────
    st.session_state.history.append(
        {"role": "user",  "text": user_input}
    )
    st.session_state.history.append(
        {"role": "model", "text": reply}
    )

    # ── Save to displayed messages ────────────────────────────
    st.session_state.messages.append({
        "role":    "assistant",
        "content": reply,
        "time":    reply_time,
    })
    st.session_state.total_messages += 1


# ── Check for chip click ──────────────────────────────────────
if hasattr(st.session_state, "_pending_input") and st.session_state._pending_input:
    pending = st.session_state._pending_input
    st.session_state._pending_input = None
    handle_message(pending)
    st.rerun()

# ── Chat input box ────────────────────────────────────────────
user_text = st.chat_input(
    "Ask me anything… (e.g. 'How do I stop procrastinating?')",
    disabled=(st.session_state.client is None),
)
if user_text:
    handle_message(user_text)
    st.rerun()

# ── Prompt when no API key ────────────────────────────────────
if st.session_state.client is None:
    st.warning("👈 Add your **free Groq API key** in the sidebar to start chatting!")
