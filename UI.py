import streamlit as st
from backend.agent.agent import run_agent
import tempfile
import os

# 1. Page Configuration
st.set_page_config(page_title="BriefAI", page_icon="📄", layout="centered")

# 2. Premium Dark CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #1c1c22 0%, #15151a 55%, #0e0e12 100%);
        color: #e8e6e1;
    }

    .main .block-container { padding-top: 5rem; max-width: 760px; }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .hero-title, .hero-subtitle, .brand-badge { animation: fadeUp 0.5s ease both; }
    .hero-subtitle { animation-delay: 0.08s; }
    .answer-card { animation: fadeUp 0.4s ease both; }

    .brand-badge {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12rem;
        text-transform: uppercase;
        color: #e0b589;
        background: rgba(224, 181, 137, 0.1);
        border: 1px solid rgba(224, 181, 137, 0.2);
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 2.8rem;
        letter-spacing: -0.04rem;
        color: #f5f3ee;
        line-height: 1.15;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #9b98a3;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.02);
        border: 1.5px dashed #2e2e38;
        border-radius: 14px;
        padding: 0.5rem 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #e0b589;
    }
    [data-testid="stFileUploader"] label {
        color: #7a7880 !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stFileDropzoneInstructions"] {
        color: #55535e !important;
        font-size: 0.82rem !important;
    }

    .stTextInput input {
        background: #1f1f26 !important;
        border: 1px solid #34343d !important;
        border-radius: 14px !important;
        color: #f0eee9 !important;
        padding: 1.1rem 1.3rem !important;
        font-size: 1.05rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
    }
    .stTextInput input::placeholder { color: #6e6c78 !important; }
    .stTextInput input:focus {
        border-color: #e0b589 !important;
        box-shadow: 0 0 0 4px rgba(224, 181, 137, 0.12) !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #e0b589, #c4895a) !important;
        color: #15151a !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        padding: 0.8rem 0 !important;
        font-size: 1rem !important;
        transition: all 0.2s ease;
        box-shadow: 0 4px 16px rgba(224, 181, 137, 0.15);
    }
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(224, 181, 137, 0.25);
    }

    /* Example prompt chips */
    div[data-testid="column"] .stButton button {
        background: #1f1f26 !important;
        color: #c8c6d0 !important;
        border: 1px solid #34343d !important;
        border-radius: 999px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.5rem 1rem !important;
        box-shadow: none !important;
    }
    div[data-testid="column"] .stButton button:hover {
        background: #26262e !important;
        border-color: #e0b589 !important;
        color: #f5f3ee !important;
        transform: none;
    }

    .manifesto-container {
        margin-top: 3.5rem;
        border-top: 1px solid #2a2a32;
        padding-top: 2rem;
    }
    .manifesto-header {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05rem;
        color: #7a7884;
        margin-bottom: 1.2rem;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid #2a2a32;
        border-radius: 14px;
        padding: 1.25rem;
        height: 100%;
        transition: all 0.2s ease;
    }
    .feature-card:hover {
        border-color: #e0b589;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
        transform: translateY(-2px);
    }
    .feature-card .icon { font-size: 1.4rem; margin-bottom: 0.5rem; display: block; }
    .feature-card h4 {
        font-family: 'Fraunces', serif;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 0 0 0.4rem 0;
        color: #f5f3ee;
    }
    .feature-card p {
        font-size: 0.85rem;
        color: #9b98a3;
        line-height: 1.5;
        margin: 0;
    }

    .answer-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08rem;
        text-transform: uppercase;
        color: #e0b589;
        margin-bottom: 1rem;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown('<div class="brand-badge">BriefAI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">What can I find for you?</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Ask about your files and I\'ll dig through them, read them, and tell you what matters.</div>',
    unsafe_allow_html=True
)

# 4. Session state init
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "uploaded_file_path" not in st.session_state:
    st.session_state.uploaded_file_path = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# 5. File uploader
uploaded_file = st.file_uploader(
    "Drop a file",
    type=["pdf", "docx", "txt"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        st.session_state.uploaded_file_path = tmp.name
        st.session_state.uploaded_file_name = uploaded_file.name
    st.success(f"📄 **{uploaded_file.name}** ready — now ask me anything about it.")

# 6. Text input + Ask button inside form (enables Enter key)
with st.form(key="query_form", clear_on_submit=False):
    user_input = st.text_input(
        "Task Input",
        value=st.session_state.user_input,
        label_visibility="collapsed",
        placeholder="e.g. Summarize the uploaded file, or find my resume..."
    )
    run_triggered = st.form_submit_button("Ask BriefAI", use_container_width=True)

# 7. Example chips — always visible
chip_col1, chip_col2, chip_col3 = st.columns(3)
examples = [
    "List my recent documents",
    "Summarize my resume",
    "Find my latest proposal"
]
for col, example in zip([chip_col1, chip_col2, chip_col3], examples):
    with col:
        if st.button(example, use_container_width=True):
            st.session_state.user_input = example
            st.rerun()

# 8. Run agent on submit
if run_triggered and user_input:

    enriched_input = user_input
    if st.session_state.uploaded_file_path:
        enriched_input = (
            f"{user_input}\n\n"
            f"[The user has uploaded a file. Use this path directly: "
            f"{st.session_state.uploaded_file_path}]"
        )

    with st.spinner("Reading through your files..."):
        try:
            result = run_agent(enriched_input)
        except Exception:
            st.error("Something went wrong on my end — please try again in a moment.")
            st.stop()

    response_text = result.get("final_response")

    if response_text:
        st.markdown('<p class="answer-label">Answer</p>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(response_text)
    else:
        st.info("I finished, but didn't have anything to report back — try rephrasing your question.")

# 9. Feature grid — always visible, sits below answer naturally
st.markdown('<div class="manifesto-container">', unsafe_allow_html=True)
st.markdown('<div class="manifesto-header">What BriefAI can do</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
        <div class="feature-card">
            <span class="icon">📁</span>
            <h4>Finds your files</h4>
            <p>Searches your Documents, Downloads, and Desktop for the PDFs and Word docs you need.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <span class="icon">📖</span>
            <h4>Reads everything</h4>
            <p>Opens and understands PDFs, Word documents, and text files automatically.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <span class="icon">✨</span>
            <h4>Sums it up</h4>
            <p>Pulls out exactly what matters, so you don't have to read it all yourself.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)