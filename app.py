import streamlit as st
import os
import uuid

from src.pipeline import process_input
from src.summarizer import summarize_meeting
from src.rag_pipeline import answer_question
from src.pdf_generator import create_pdf


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MeetMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background: #f6f7fb;
    }

    .block-container {
        max-width: 980px;
        padding-top: 4.5rem;
        padding-bottom: 4rem;
    }

    /* Streamlit's own top toolbar is fixed/overlaid — the extra
       block-container padding above clears it so the hero icon
       and title are never rendered underneath it. */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    h1, h2, h3, h4, h5, p, span, div {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
            Inter, Roboto, Helvetica, Arial, sans-serif;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background: #171923;
        border-right: 1px solid #232633;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        border-radius: 10px;
        border: 1px solid #2b2f3d;
        background: #1f222e;
        color: #e5e7eb;
        font-weight: 500;
        font-size: 0.88rem;
        padding: 0.5rem 0.75rem;
        min-height: 2.4rem;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #2a2e3d;
        border-color: #6d5bd0;
    }

    .new-analysis-btn button {
        background: linear-gradient(135deg, #7c5cff, #6d5bd0) !important;
        border: none !important;
        color: white !important;
        font-weight: 650 !important;
    }

    .new-analysis-btn button:hover {
        opacity: 0.92;
    }

    .session-active button {
        background: #2c2f6b !important;
        border: 1px solid #7c5cff !important;
        color: #ffffff !important;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.4rem 0 1rem 0;
        border-bottom: 1px solid #262a38;
        margin-bottom: 0.9rem;
    }

    .sidebar-brand-title {
        font-size: 1.15rem;
        font-weight: 750;
        color: #f4f4f6;
        letter-spacing: -0.02em;
    }

    .sidebar-section-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #7d8299;
        margin: 1.1rem 0 0.5rem 0.1rem;
        text-transform: uppercase;
    }

    .sidebar-empty {
        color: #6b7080;
        font-size: 0.82rem;
        padding: 0.3rem 0.1rem;
        line-height: 1.4;
    }

    .sidebar-footer {
        position: sticky;
        bottom: 0;
        margin-top: 2.5rem;
        padding-top: 0.9rem;
        border-top: 1px solid #262a38;
        color: #6b7080;
        font-size: 0.78rem;
        line-height: 1.4;
    }

    .sidebar-footer b {
        color: #b7bacb;
    }

    /* ---------- Header ---------- */

    .mm-header {
        text-align: center;
        padding: 8px 10px 22px 10px;
    }

    .mm-header-badge {
        font-size: 34px;
        line-height: 1;
    }

    .mm-header-title {
        font-size: 30px;
        font-weight: 800;
        color: #14151f;
        margin: 6px 0 2px 0;
        letter-spacing: -0.02em;
    }

    .mm-header-subtitle {
        font-size: 15px;
        font-weight: 600;
        color: #6d5bd0;
        margin-bottom: 6px;
    }

    .mm-header-tagline {
        color: #6b7280;
        font-size: 14px;
        max-width: 480px;
        margin: 0 auto;
        line-height: 1.5;
    }

    .mm-header-compact {
        text-align: left;
        padding: 4px 2px 14px 2px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid #e6e7f0;
        margin-bottom: 1.1rem;
    }

    .mm-header-compact .mm-header-title {
        font-size: 20px;
        margin: 0;
    }

    .mm-header-compact .mm-header-badge {
        font-size: 22px;
    }

    /* ---------- Feature cards ---------- */

    .feature-card {
        background: white;
        border: 1px solid #e8e9f2;
        border-radius: 14px;
        padding: 1rem 0.9rem;
        text-align: center;
        min-height: 118px;
        box-shadow: 0 2px 8px rgba(20, 21, 31, 0.03);
        transition: all 0.15s ease;
    }

    .feature-card:hover {
        border-color: #c9c2fb;
        box-shadow: 0 6px 16px rgba(109, 91, 208, 0.10);
        transform: translateY(-1px);
    }

    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 0.35rem;
    }

    .feature-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #191a24;
    }

    .feature-text {
        font-size: 0.78rem;
        color: #7a7f93;
        margin-top: 0.2rem;
        line-height: 1.35;
    }

    /* ---------- Section titles ---------- */

    .section-title {
        font-size: 1.15rem;
        font-weight: 750;
        color: #191a24;
        margin-bottom: 0.15rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .section-description {
        color: #7a7f93;
        font-size: 0.88rem;
        margin-bottom: 0.9rem;
    }

    /* ---------- Input card ---------- */

    .mm-card {
        background: white;
        border: 1px solid #e8e9f2;
        border-radius: 16px;
        padding: 1.2rem 1.3rem 1.3rem 1.3rem;
        box-shadow: 0 2px 10px rgba(20, 21, 31, 0.03);
        margin-bottom: 1.1rem;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 2.7rem;
        font-weight: 650;
        border: 1px solid #d9dae5;
        background: white;
        color: #191a24;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        border-color: #7c5cff;
        color: #6d5bd0;
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 2.7rem;
        font-weight: 650;
    }

    div[data-testid="stFormSubmitButton"] button,
    .mm-primary-btn button {
        background: linear-gradient(135deg, #7c5cff, #6d5bd0) !important;
        color: white !important;
        border: none !important;
    }

    .mm-primary-btn button:hover {
        opacity: 0.9;
        color: white !important;
    }

    /* ---------- Toggle tabs (upload / youtube) ---------- */

    .mm-toggle-active button {
        background: #191a24 !important;
        color: white !important;
        border: 1px solid #191a24 !important;
    }

    .mm-toggle-inactive button {
        background: #f2f2f7 !important;
        color: #5c5f6e !important;
        border: 1px solid #e8e9f2 !important;
    }

    /* ---------- File uploader ---------- */

    [data-testid="stFileUploader"] {
        background: #fafafe;
        border-radius: 12px;
        border: 1px dashed #d9dae5;
        padding: 0.4rem;
    }

    /* ---------- Chat bubbles ---------- */

    .stChatMessage {
        border-radius: 14px;
    }

    /* ---------- Status pill ---------- */

    .mm-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #f2f0ff;
        color: #5b3fd6;
        border: 1px solid #e1dbff;
        border-radius: 999px;
        padding: 0.4rem 0.9rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
    }

    .mm-status-done {
        background: #ecfdf3;
        color: #1a7f4e;
        border: 1px solid #c8f2dc;
    }

    /* ---------- Insight cards ---------- */

    .insight-card {
        background: white;
        border: 1px solid #e8e9f2;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(20, 21, 31, 0.03);
    }

    .insight-card-title {
        font-weight: 750;
        font-size: 0.95rem;
        color: #191a24;
        margin-bottom: 0.4rem;
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.82rem;
        padding-top: 3rem;
    }

    </style>
    """
)


# ============================================================
# SESSION STATE
# ============================================================

if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "session_order" not in st.session_state:
    st.session_state.session_order = []

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None


def _new_session_id():
    return str(uuid.uuid4())


def _get_current_session():
    sid = st.session_state.current_session_id
    if sid and sid in st.session_state.sessions:
        return st.session_state.sessions[sid]
    return None


def _create_session(title, source_type):
    sid = _new_session_id()
    st.session_state.sessions[sid] = {
        "id": sid,
        "title": title,
        "source_type": source_type,
        "transcript": None,
        "analysis": None,
        "transcript_path": None,
        "chat_history": [],
        "pdf_data": None,
    }
    st.session_state.session_order.insert(0, sid)
    st.session_state.current_session_id = sid
    return st.session_state.sessions[sid]


# ============================================================
# SIDEBAR — CHAT / ANALYSIS HISTORY
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">
            <div style="font-size:22px;">🧠</div>
            <div class="sidebar-brand-title">MeetMind</div>
        </div>
        """
    )

    st.markdown('<div class="new-analysis-btn">', unsafe_allow_html=True)

    if st.button("＋  New Analysis", key="new_analysis_btn"):
        st.session_state.current_session_id = None
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.html('<div class="sidebar-section-label">Recent Analyses</div>')

    if not st.session_state.session_order:

        st.html(
            """
            <div class="sidebar-empty">
                No analyses yet.<br>
                Process a meeting or YouTube video to get started.
            </div>
            """
        )

    else:

        for sid in st.session_state.session_order:

            session = st.session_state.sessions.get(sid)

            if not session:
                continue

            is_active = sid == st.session_state.current_session_id

            icon = "🎥" if session["source_type"] == "youtube" else "📝"

            wrapper_class = "session-active" if is_active else ""

            st.markdown(
                f'<div class="{wrapper_class}">',
                unsafe_allow_html=True
            )

            if st.button(
                f"{icon}  {session['title']}",
                key=f"session_btn_{sid}"
            ):
                st.session_state.current_session_id = sid
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    st.html(
        """
        <div class="sidebar-footer">
            <b>MeetMind</b><br>
            AI Meeting Intelligence
        </div>
        """
    )


# ============================================================
# HEADER
# ============================================================

current_session = _get_current_session()

if current_session and current_session.get("transcript"):

    st.html(
        f"""
        <div class="mm-header-compact">
            <div class="mm-header-badge">🧠</div>
            <div class="mm-header-title">MeetMind</div>
        </div>
        """
    )

else:

    st.html(
        """
        <div class="mm-header">
            <div class="mm-header-badge">🧠</div>
            <div class="mm-header-title">MeetMind</div>
            <div class="mm-header-subtitle">AI Audio & Video Intelligence Assistant
</div>
            <div class="mm-header-tagline">
                Turn conversations into searchable insights,
                summaries, decisions and action items.
            </div>
        </div>
        """
    )


# ============================================================
# FEATURE CARDS (only before a session has results)
# ============================================================

if not (current_session and current_session.get("transcript")):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.html(
            """
            <div class="feature-card">
                <div class="feature-icon">🎙️</div>
                <div class="feature-title">Transcription</div>
                <div class="feature-text">
                    Convert speech into timestamped text.
                </div>
            </div>
            """
        )

    with col2:
        st.html(
            """
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI Analysis</div>
                <div class="feature-text">
                    Summaries, decisions and action items.
                </div>
            </div>
            """
        )

    with col3:
        st.html(
            """
            <div class="feature-card">
                <div class="feature-icon">🔎</div>
                <div class="feature-title">RAG Search</div>
                <div class="feature-text">
                    Ask questions grounded in your content.
                </div>
            </div>
            """
        )

    with col4:
        st.html(
            """
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <div class="feature-title">PDF Reports</div>
                <div class="feature-text">
                    Export your meeting intelligence.
                </div>
            </div>
            """
        )

    st.write("")


# ============================================================
# INPUT SECTION (only when no active processed session)
# ============================================================

if not (current_session and current_session.get("transcript")):

    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "Upload File"

    st.html(
        """
        <div class="section-title">🎥 Add your media</div>
        <div class="section-description">
            Upload a media file or analyze a YouTube video.
        </div>
        """
    )

    st.markdown('<div class="mm-card">', unsafe_allow_html=True)

    toggle_col1, toggle_col2, spacer = st.columns([1, 1, 3])

    with toggle_col1:
        cls = (
            "mm-toggle-active"
            if st.session_state.input_mode == "Upload File"
            else "mm-toggle-inactive"
        )
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button("🎥 Upload File", key="toggle_upload"):
            st.session_state.input_mode = "Upload File"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with toggle_col2:
        cls = (
            "mm-toggle-active"
            if st.session_state.input_mode == "YouTube URL"
            else "mm-toggle-inactive"
        )
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button("🔗 YouTube URL", key="toggle_youtube"):
            st.session_state.input_mode = "YouTube URL"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    input_type = st.session_state.input_mode

    st.write("")

    # --------------------------------------------------------
    # UPLOAD FILE
    # --------------------------------------------------------

    if input_type == "Upload File":

        st.caption("Upload your audio or video to get started — MP4 • MP3 • WAV")

        uploaded_file = st.file_uploader(
            "Drop your audio or video here",
            type=["mp4", "mp3", "wav"],
            label_visibility="collapsed"
        )

        if uploaded_file:

            st.success(f"Selected: {uploaded_file.name}")

            st.markdown('<div class="mm-primary-btn">', unsafe_allow_html=True)
            process_clicked = st.button(
                "⚡ Process Media",
                use_container_width=True,
                key="process_upload_btn"
            )
            st.markdown('</div>', unsafe_allow_html=True)

            if process_clicked:

                input_path = os.path.join(
                    "data",
                    "input",
                    uploaded_file.name
                )

                status_box = st.empty()

                try:

                    with open(input_path, "wb") as file:
                        file.write(uploaded_file.getbuffer())

                    status_box.html(
                        '<div class="mm-status">🎙️ Transcribing media...</div>'
                    )

                    transcript_path = process_input(input_path, "file")

                    with open(
                        transcript_path, "r", encoding="utf-8"
                    ) as file:
                        transcript = file.read()

                    status_box.html(
                        '<div class="mm-status">🤖 Generating AI insights...</div>'
                    )

                    analysis = summarize_meeting(transcript)

                    session = _create_session(
                        title=uploaded_file.name,
                        source_type="file"
                    )

                    session["transcript_path"] = transcript_path
                    session["transcript"] = transcript
                    session["analysis"] = analysis
                    session["chat_history"] = []
                    session["pdf_data"] = None

                    status_box.html(
                        '<div class="mm-status mm-status-done">✅ Analysis complete</div>'
                    )

                    st.rerun()

                except Exception as error:

                    status_box.empty()

                    if "429" in str(error):

                        st.error(
                            "⚠️ AI service temporarily unavailable\n\n"
                            "Your Gemini API quota has been exhausted. "
                            "Please try again after the quota resets."
                        )

                    else:

                        st.error(
                            "⚠️ Something went wrong. Please try again."
                        )

    # --------------------------------------------------------
    # YOUTUBE URL
    # --------------------------------------------------------

    else:

        st.caption("Paste a YouTube URL")

        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed"
        )

        if youtube_url:

            st.markdown('<div class="mm-primary-btn">', unsafe_allow_html=True)
            process_clicked = st.button(
                "⚡ Process Media",
                use_container_width=True,
                key="process_youtube_btn"
            )
            st.markdown('</div>', unsafe_allow_html=True)

            if process_clicked:

                status_box = st.empty()

                try:

                    status_box.html(
                        '<div class="mm-status">🎙️ Transcribing media...</div>'
                    )

                    transcript_path = process_input(youtube_url, "youtube")

                    with open(
                        transcript_path, "r", encoding="utf-8"
                    ) as file:
                        transcript = file.read()

                    status_box.html(
                        '<div class="mm-status">🤖 Generating AI insights...</div>'
                    )

                    analysis = summarize_meeting(transcript)

                    session = _create_session(
                        title=youtube_url[:40],
                        source_type="youtube"
                    )

                    session["transcript_path"] = transcript_path
                    session["transcript"] = transcript
                    session["analysis"] = analysis
                    session["chat_history"] = []
                    session["pdf_data"] = None

                    status_box.html(
                        '<div class="mm-status mm-status-done">✅ Analysis complete</div>'
                    )

                    st.rerun()

                except Exception as error:

                    status_box.empty()

                    if "429" in str(error):

                        st.error(
                            "⚠️ AI service temporarily unavailable\n\n"
                            "Your Gemini API quota has been exhausted. "
                            "Please try again after the quota resets."
                        )

                    else:

                        st.error(
                            "⚠️ Something went wrong. Please try again."
                        )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# RESULTS
# ============================================================

current_session = _get_current_session()

if current_session and current_session.get("transcript"):

    st.html(
        """
        <div class="section-title">📊 Results</div>
        <div class="section-description">
            Your processed content and AI-generated insights.
        </div>
        """
    )

    transcript_tab, analysis_tab, insights_tab = st.tabs(
        ["📝 Transcript", "🤖 AI Analysis", "📊 Insights"]
    )

    # --------------------------------------------------------
    # TRANSCRIPT TAB
    # --------------------------------------------------------

    with transcript_tab:

        st.text_area(
            "Timestamped Transcript",
            current_session["transcript"],
            height=460,
            label_visibility="collapsed"
        )

    # --------------------------------------------------------
    # ANALYSIS TAB
    # --------------------------------------------------------

    with analysis_tab:

        st.markdown(current_session["analysis"])

    # --------------------------------------------------------
    # INSIGHTS TAB
    # --------------------------------------------------------

    with insights_tab:

        sections = [
            ("📌", "Summary"),
            ("💡", "Key Discussion Points"),
            ("ℹ️", "Important Information"),
            ("✅", "Decisions / Conclusions"),
            ("🎯", "Action Items"),
        ]

        for icon, label in sections:

            st.html(
                f"""
                <div class="insight-card">
                    <div class="insight-card-title">{icon} {label}</div>
                </div>
                """
            )

        st.caption(
            "Full breakdown available in the 🤖 AI Analysis tab above."
        )


    # ==========================================================
    # PDF REPORT
    # ==========================================================

    st.divider()

    st.html(
        """
        <div class="section-title">📄 Meeting Report</div>
        <div class="section-description">
            Export your AI-generated meeting intelligence.
        </div>
        """
    )

    st.markdown('<div class="mm-card">', unsafe_allow_html=True)

    st.markdown('<div class="mm-primary-btn">', unsafe_allow_html=True)
    generate_clicked = st.button(
        "📄 Generate PDF Report",
        use_container_width=True,
        key="generate_pdf_btn"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_clicked:

        pdf_path = "data/output/meetmind_report.pdf"

        status_box = st.empty()

        try:

            status_box.html(
                '<div class="mm-status">📄 Generating PDF report...</div>'
            )

            create_pdf(
                current_session["transcript"],
                current_session["analysis"],
                pdf_path
            )

            with open(pdf_path, "rb") as pdf_file:
                current_session["pdf_data"] = pdf_file.read()

            status_box.html(
                '<div class="mm-status mm-status-done">✅ Analysis complete</div>'
            )

        except Exception as error:

            status_box.empty()
            st.error("⚠️ Something went wrong generating the PDF.")

    if current_session.get("pdf_data"):

        st.download_button(
            label="⬇️ Download MeetMind Report",
            data=current_session["pdf_data"],
            file_name="meetmind_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================================
    # RAG CHAT
    # ==========================================================

    st.divider()

    st.html(
        """
        <div class="section-title">💬 Chat with Your Content</div>
        <div class="section-description">
            Ask questions and retrieve answers directly from your
            processed content.
        </div>
        """
    )

    # ----------------------------------------------------------
    # CHAT HISTORY
    # ----------------------------------------------------------

    for message in current_session["chat_history"]:

        with st.chat_message(message["role"]):

            st.write(message["content"])

            if message["role"] == "assistant" and "sources" in message:

                num_sources = len(message.get("sources", []))

                with st.expander(f"📚 {num_sources} Sources"):

                    for i, (source, metadata) in enumerate(
                        zip(message["sources"], message["metadatas"]),
                        start=1
                    ):

                        st.markdown(
                            f"**Source {i} — "
                            f"{metadata['start_time']} - "
                            f"{metadata['end_time']}**"
                        )

                        st.write(source)

    # ----------------------------------------------------------
    # CHAT INPUT
    # ----------------------------------------------------------

    question = st.chat_input("Ask anything about your content...")

    if question:

        with st.chat_message("user"):
            st.write(question)

        current_session["chat_history"].append(
            {"role": "user", "content": question}
        )

        with st.chat_message("assistant"):

            try:

                with st.spinner("🔎 Searching your content..."):

                    answer, sources, metadatas = answer_question(
                        question,
                        current_session["chat_history"]
                    )

                st.write(answer)

                with st.expander(f"📚 {len(sources)} Sources"):

                    for i, (source, metadata) in enumerate(
                        zip(sources, metadatas), start=1
                    ):

                        st.markdown(
                            f"**Source {i} — "
                            f"{metadata['start_time']} - "
                            f"{metadata['end_time']}**"
                        )

                        st.write(source)

                current_session["chat_history"].append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "metadatas": metadatas
                    }
                )

            except Exception as error:

                if "429" in str(error):

                    st.error(
                        "⚠️ AI service temporarily unavailable\n\n"
                        "Your Gemini API quota has been exhausted. "
                        "Please try again after the quota resets."
                    )

                else:

                    st.error(
                        "⚠️ Something went wrong. Please try again."
                    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        🧠 MeetMind · AI-powered meeting & video intelligence
    </div>
    """
)
