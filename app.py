import streamlit as st
from groq import Groq


groq_api_key = st.secrets["GROQ_API_KEY"]

if not groq_api_key:
    st.error("GROQ_API_KEY not found. Please check your .env file.")
    st.stop()


# ==============================
# Groq Client
# ==============================

client = Groq(api_key=groq_api_key)


# ==============================
# Page Configuration
# ==============================

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)


# ==============================
# Custom CSS
# ==============================

st.markdown(
    """
    <style>

    /* Title */
    .title {
        text-align: center;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    /* Summary box */
    .summary-box {
        background-color: #f7f9fc;
        border: 1px solid #e1e5eb;
        border-radius: 12px;
        padding: 20px;
        min-height: 300px;
        line-height: 1.6;
    }

    .summary-title {
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    /* Button */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-size: 16px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==============================
# Header
# ==============================

st.markdown(
    '<div class="title">📝 AI Text Summarizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Summarize long text quickly using AI</div>',
    unsafe_allow_html=True
)


# ==============================
# Two Column Layout
# ==============================

left_column, right_column = st.columns([3, 1])


# ==============================
# LEFT SIDE - INPUT
# ==============================

with left_column:

    st.markdown(
        '<div class="summary-title">📄 Enter Your Text</div>',
        unsafe_allow_html=True
    )

    text = st.text_area(
        "Paste your text below",
        height=250,
        placeholder="Paste your article, document, paragraph, or any long text here...",
        label_visibility="collapsed"
    )

    summarize_button = st.button(
        "✨ Summarize Text",
        use_container_width=True
    )


# ==============================
# RIGHT SIDE - OUTPUT
# ==============================

with right_column:

    st.markdown(
        '<div class="summary-title">📌 Summary</div>',
        unsafe_allow_html=True
    )

    if summarize_button:

        if not text.strip():

            st.warning("Please enter some text first.")

        else:

            with st.spinner("Generating summary..."):

                try:

                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an expert text summarizer. "
                                    "Summarize the given text clearly and concisely. "
                                    "Keep the important facts and key points. "
                                    "Do not add information that is not present "
                                    "in the original text."
                                )
                            },
                            {
                                "role": "user",
                                "content": (
                                    f"Summarize this text:\n\n{text}"
                                )
                            }
                        ],
                        model="openai/gpt-oss-120b"
                    )

                    summary = (
                        chat_completion
                        .choices[0]
                        .message
                        .content
                    )

                    st.markdown(
                        f"""
                        <div class="summary-box">
                            {summary}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error(f"Something went wrong: {e}")

    else:

        st.markdown(
            """
            <div class="summary-box">
                <p style="color:#888;">
                    Your AI-generated summary will appear here.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
