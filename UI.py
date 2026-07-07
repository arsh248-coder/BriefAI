import streamlit as st
from backend.agent.agent import run_agent
import tempfile
import os
import streamlit.components.v1 as components
from fpdf import FPDF


def generate_pdf(text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=15)
    clean_text = text.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 7, clean_text)
    return pdf.output()


# 1. Page Configuration
st.set_page_config(page_title="BriefAI", page_icon="📄", layout="wide")

# 2. Theme state init
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

is_dark = st.session_state.theme == "dark"

# Theme variables
if is_dark:
    bg = "radial-gradient(circle at 50% 0%, #1c1c22 0%, #15151a 55%, #0e0e12 100%)"
    text_primary = "#f5f3ee"
    text_secondary = "#9b98a3"
    text_muted = "#6e6c78"
    surface = "#1f1f26"
    surface2 = "#1a1a20"
    border = "#34343d"
    border2 = "#2a2a32"
    chat_user_bg = "#2a2a35"
    chat_user_border = "#34343d"
    chat_user_color = "#f0eee9"
    card_bg = "rgba(255,255,255,0.025)"
    input_bg = "#1f1f26"
    input_color = "#f0eee9"
    input_placeholder = "#6e6c78"
    chip_bg = "#1f1f26"
    chip_color = "#c8c6d0"
    chip_hover_bg = "#26262e"
    manifesto_border = "#2a2a32"
    manifesto_header_color = "#7a7884"
    toggle_icon = "☀️"
    sidebar_bg = "#13131a"
    sidebar_border = "#2a2a32"
    sidebar_item_bg = "#1f1f26"
    sidebar_item_border = "#2a2a32"
    sidebar_text = "#c8c6d0"
else:
    bg = "radial-gradient(circle at 50% 0%, #fdfcf9 0%, #f7f5f0 60%, #f2efe8 100%)"
    text_primary = "#1c1c1e"
    text_secondary = "#5a5860"
    text_muted = "#8a8895"
    surface = "#ffffff"
    surface2 = "#ffffff"
    border = "#e3e0d8"
    border2 = "#ece8df"
    chat_user_bg = "#f0ece3"
    chat_user_border = "#e3e0d8"
    chat_user_color = "#1c1c1e"
    card_bg = "rgba(255,255,255,0.8)"
    input_bg = "#ffffff"
    input_color = "#1c1c1e"
    input_placeholder = "#a8a6b0"
    chip_bg = "#ffffff"
    chip_color = "#4a4a52"
    chip_hover_bg = "#faf8f3"
    manifesto_border = "#ece8df"
    manifesto_header_color = "#a8a6b0"
    toggle_icon = "🌙"
    sidebar_bg = "#faf8f3"
    sidebar_border = "#ece8df"
    sidebar_item_bg = "#ffffff"
    sidebar_item_border = "#e3e0d8"
    sidebar_text = "#4a4a52"

# 3. CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

    .stApp {{
        background: {bg};
        color: {text_primary};
    }}

    .main .block-container {{ padding-top: 5rem; max-width: 760px; margin: 0 auto; }}

    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .hero-title, .hero-subtitle, .brand-badge {{ animation: fadeUp 0.5s ease both; }}
    .hero-subtitle {{ animation-delay: 0.08s; }}

    .brand-badge {{
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
    }}

    .hero-title {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 2.8rem;
        letter-spacing: -0.04rem;
        color: {text_primary};
        line-height: 1.15;
        margin-bottom: 0.5rem;
    }}

    .hero-subtitle {{
        color: {text_secondary};
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        border-right: 1px solid {sidebar_border} !important;
    }}
    [data-testid="stSidebar"] .stMarkdown p {{
        color: {sidebar_text} !important;
        font-size: 0.85rem;
    }}

    .sidebar-header {{
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08rem;
        color: #e0b589;
        margin-bottom: 0.8rem;
    }}

    /* Sidebar remove button */
    [data-testid="stSidebar"] .stButton button {{
        background: transparent !important;
        color: {text_muted} !important;
        border: none !important;
        border-radius: 4px !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        padding: 0.1rem 0.3rem !important;
        box-shadow: none !important;
        min-height: 0 !important;
        line-height: 1 !important;
    }}
    [data-testid="stSidebar"] .stButton button:hover {{
        color: #e05858 !important;
        background: rgba(224, 88, 88, 0.08) !important;
        transform: none !important;
        box-shadow: none !important;
    }}

    /* Toggle button */
    .toggle-btn button {{
        background: transparent !important;
        color: {text_muted} !important;
        border: 1px solid {border2} !important;
        border-radius: 999px !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.35rem 1rem !important;
        box-shadow: none !important;
        float: right;
    }}
    .toggle-btn button:hover {{
        color: #e0b589 !important;
        border-color: #e0b589 !important;
        transform: none !important;
        box-shadow: none !important;
    }}

    /* File uploader */
    [data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.02);
        border: 1.5px dashed {border};
        border-radius: 14px;
        padding: 0.5rem 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }}
    [data-testid="stFileUploader"]:hover {{ border-color: #e0b589; }}
    [data-testid="stFileUploader"] label {{ color: {text_muted} !important; font-size: 0.85rem !important; }}
    [data-testid="stFileDropzoneInstructions"] {{ color: {text_muted} !important; font-size: 0.82rem !important; }}
    [data-testid="stFileUploader"] section {{
        background: {surface} !important;
        border-color: {border} !important;
    }}
    [data-testid="stFileUploader"] section > button {{
        background: {surface} !important;
        color: {text_primary} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stFileUploader"] section span {{
        color: {text_secondary} !important;
    }}

    .stTextInput input {{
        background: {input_bg} !important;
        border: 1px solid {border} !important;
        border-radius: 14px !important;
        color: {input_color} !important;
        padding: 1.1rem 1.3rem !important;
        font-size: 1.05rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }}
    .stTextInput input::placeholder {{ color: {input_placeholder} !important; }}
    .stTextInput input:focus {{
        border-color: #e0b589 !important;
        box-shadow: 0 0 0 4px rgba(224, 181, 137, 0.12) !important;
    }}

    .stButton button {{
        background: linear-gradient(135deg, #e0b589, #c4895a) !important;
        color: #15151a !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        padding: 0.8rem 0 !important;
        font-size: 1rem !important;
        transition: all 0.2s ease;
        box-shadow: 0 4px 16px rgba(224, 181, 137, 0.15);
    }}
    .stButton button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(224, 181, 137, 0.25);
    }}

    /* Chip buttons */
    div[data-testid="column"] .stButton button {{
        background: {chip_bg} !important;
        color: {chip_color} !important;
        border: 1px solid {border} !important;
        border-radius: 999px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.5rem 1rem !important;
        box-shadow: none !important;
    }}
    div[data-testid="column"] .stButton button:hover {{
        background: {chip_hover_bg} !important;
        border-color: #e0b589 !important;
        color: {text_primary} !important;
        transform: none;
    }}

    /* Chat bubbles */
    .chat-user {{
        background: {chat_user_bg};
        border: 1px solid {chat_user_border};
        border-radius: 16px 16px 4px 16px;
        padding: 0.9rem 1.2rem;
        margin: 0.5rem 0;
        color: {chat_user_color};
        font-size: 0.95rem;
        line-height: 1.5;
        margin-left: 3rem;
    }}

    .chat-label-user {{
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08rem;
        text-transform: uppercase;
        color: {text_muted};
        margin-bottom: 0.3rem;
        text-align: right;
    }}

    .chat-label-assistant {{
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08rem;
        text-transform: uppercase;
        color: #e0b589;
        margin-bottom: 0.3rem;
    }}

    .clear-btn button {{
        background: transparent !important;
        color: {text_muted} !important;
        border: 1px solid {border2} !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        padding: 0.3rem 0.8rem !important;
        box-shadow: none !important;
    }}
    .clear-btn button:hover {{
        color: #e0b589 !important;
        border-color: #e0b589 !important;
        transform: none !important;
        box-shadow: none !important;
    }}

    /* Download button */
    [data-testid="stDownloadButton"] button {{
        background: transparent !important;
        color: {text_muted} !important;
        border: 1px solid {border2} !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        padding: 0.3rem 0.8rem !important;
        box-shadow: none !important;
        width: auto !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        color: #e0b589 !important;
        border-color: #e0b589 !important;
        transform: none !important;
        box-shadow: none !important;
    }}

    .manifesto-container {{
        margin-top: 3.5rem;
        border-top: 1px solid {manifesto_border};
        padding-top: 2rem;
    }}
    .manifesto-header {{
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05rem;
        color: {manifesto_header_color};
        margin-bottom: 1.2rem;
    }}

    .feature-card {{
        background: {card_bg};
        border: 1px solid {border2};
        border-radius: 14px;
        padding: 1.25rem;
        height: 100%;
        transition: all 0.2s ease;
    }}
    .feature-card:hover {{
        border-color: #e0b589;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }}
    .feature-card .icon {{ font-size: 1.4rem; margin-bottom: 0.5rem; display: block; }}
    .feature-card h4 {{
        font-family: 'Fraunces', serif;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 0 0 0.4rem 0;
        color: {text_primary};
    }}
    .feature-card p {{
        font-size: 0.85rem;
        color: {text_secondary};
        line-height: 1.5;
        margin: 0;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: {border2} !important;
        border-radius: 14px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. Sidebar — file history
with st.sidebar:
    st.markdown('<div class="sidebar-header">📚 Indexed Documents</div>', unsafe_allow_html=True)
    st.markdown("Files BriefAI has read and remembers:")
    st.markdown("---")

    try:
        from backend.agent.embedder import get_indexed_files, delete_document
        indexed_files = get_indexed_files()

        if not indexed_files:
            st.markdown(
                f'<p style="color:{text_muted};font-size:0.82rem;">No files indexed yet — upload a file or ask BriefAI to read one.</p>',
                unsafe_allow_html=True
            )
        else:
            for f in indexed_files:
                col_name, col_del = st.columns([5, 1])
                with col_name:
                    st.markdown(f"""
                        <div style="
                            font-size: 0.82rem;
                            color: {sidebar_text};
                            padding: 0.3rem 0;
                            border-bottom: 1px solid {sidebar_border};
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                        ">📄 {f['name']}</div>
                    """, unsafe_allow_html=True)
                with col_del:
                    if st.button("✕", key=f"del_{f['path']}", help=f"Remove {f['name']}"):
                        delete_document(f["path"])
                        st.rerun()

    except Exception as e:
        st.markdown(
            f'<p style="color:{text_muted};font-size:0.82rem;">Could not load index.</p>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown(
        f'<p style="color:{text_muted};font-size:0.75rem;">BriefAI remembers these files across sessions using ChromaDB.</p>',
        unsafe_allow_html=True
    )

# 5. Header row with toggle
header_col, toggle_col = st.columns([6, 1])
with header_col:
    st.markdown('<div class="brand-badge">BriefAI</div>', unsafe_allow_html=True)
with toggle_col:
    st.markdown('<div class="toggle-btn">', unsafe_allow_html=True)
    if st.button(toggle_icon, use_container_width=False):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="hero-title">What can I find for you?</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="hero-subtitle">Ask about your files and I\'ll dig through them, read them, and tell you what matters.</div>',
    unsafe_allow_html=True
)

# 6. Session state init
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "uploaded_file_path" not in st.session_state:
    st.session_state.uploaded_file_path = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# 7. File uploader — multi-file
uploaded_files = st.file_uploader(
    "Drop files",
    type=["pdf", "docx", "txt", "jpg", "jpeg", "png", "gif", "webp"],
    label_visibility="collapsed",
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        st.session_state.uploaded_file_path = temp_path
        st.session_state.uploaded_file_name = uploaded_file.name

        ext = os.path.splitext(uploaded_file.name)[1].lower()
        image_exts = [".jpg", ".jpeg", ".png", ".gif", ".webp"]

        if ext not in image_exts:
            with st.spinner(f"Indexing {uploaded_file.name}..."):
                try:
                    from backend.agent.tools import embed_and_index
                    embed_and_index(temp_path)
                    st.success(f"📄 **{uploaded_file.name}** indexed.")
                except Exception as e:
                    st.warning(f"📄 **{uploaded_file.name}** couldn't be indexed: {e}")
        else:
            st.success(f"🖼 **{uploaded_file.name}** ready — ask me anything about it.")

# 8. Chat history display
if st.session_state.chat_history:
    for i, turn in enumerate(st.session_state.chat_history):
        st.markdown(f'<div class="chat-label-user">You</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-user">{turn["user"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-label-assistant">BriefAI</div>', unsafe_allow_html=True)
        st.markdown(turn["assistant"])

        if i == len(st.session_state.chat_history) - 1:
            copy_text = turn["assistant"].replace("'", "\\'").replace("\n", "\\n").replace("\r", "")
            components.html(f"""
                <textarea id="copy-area" style="position:fixed;top:-9999px;">{turn["assistant"]}</textarea>
                <button onclick="
                    var el = document.getElementById('copy-area');
                    el.style.top = '0';
                    el.select();
                    el.setSelectionRange(0, 99999);
                    document.execCommand('copy');
                    el.style.top = '-9999px';
                    this.innerText = '✓ Copied';
                    this.style.color = '#4ade80';
                    this.style.borderColor = '#4ade80';
                    setTimeout(() => {{
                        this.innerText = '⎘ Copy answer';
                        this.style.color = '#6e6c78';
                        this.style.borderColor = '#2a2a32';
                    }}, 2000);
                " style="
                    background: transparent;
                    border: 1px solid #2a2a32;
                    color: #6e6c78;
                    border-radius: 8px;
                    padding: 0.3rem 0.8rem;
                    font-size: 0.78rem;
                    cursor: pointer;
                    font-family: Inter, sans-serif;
                ">⎘ Copy answer</button>
            """, height=45)

            pdf_bytes = generate_pdf(turn["assistant"])
            st.download_button(
                label="⬇ Download as PDF",
                data=bytes(pdf_bytes),
                file_name="BriefAI_Answer.pdf",
                mime="application/pdf",
                use_container_width=False
            )

        st.markdown("---")

    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("✕ Clear chat", use_container_width=False):
        st.session_state.chat_history = []
        st.session_state.last_response = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 9. Input form
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input(
        "Task Input",
        value="",
        label_visibility="collapsed",
        placeholder="e.g. Summarize the uploaded file, or find my resume..."
    )
    run_triggered = st.form_submit_button("Ask BriefAI", use_container_width=True)

# 10. Example chips
if not run_triggered:
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

# 11. Run agent on submit
if run_triggered and user_input:
    st.session_state.user_input = ""

    enriched_input = user_input
    if st.session_state.uploaded_file_path:
        ext = os.path.splitext(st.session_state.uploaded_file_path)[1].lower()
        image_exts = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        if ext in image_exts:
            enriched_input = (
                f"{user_input}\n\n"
                f"[The user has uploaded an image. Use read_image on this path directly: "
                f"{st.session_state.uploaded_file_path}]"
            )
        else:
            enriched_input = (
                f"{user_input}\n\n"
                f"[The user has uploaded a file. Use this path directly: "
                f"{st.session_state.uploaded_file_path}]"
            )

    with st.spinner("Reading through your files..."):
        try:
            result = run_agent(enriched_input, st.session_state.chat_history)
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    response_text = result.get("final_response")

    if response_text:
        st.session_state.chat_history.append({
            "user": user_input,
            "assistant": response_text
        })
        st.session_state.last_response = response_text
        st.rerun()
    else:
        st.info("I finished, but didn't have anything to report back — try rephrasing your question.")

# 12. Landing feature grid
if not run_triggered:
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