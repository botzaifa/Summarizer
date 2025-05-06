import streamlit as st
from models.summarizer import TextSummarizer
from pathlib import Path

# Page config
st.set_page_config(page_title="Text Summarizer", layout="wide")

# Load custom CSS
def load_css(css_path: str):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/styles.css")

# Load summarizer model
@st.cache_resource
def load_model():
    return TextSummarizer(model_name="t5-base")

summarizer = load_model()

# App Title and Description
st.markdown("<h1 class='title'>📝 Text Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Summarize long documents instantly using a fine-tuned T5 model. Get concise, clear output in seconds.</p>", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([2, 1])

# Check if session state already has the key for input_text
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

with col1:
    # Use st.text_area with session_state tracking
    input_text = st.text_area("📄 Enter your text below:", height=300, placeholder="Paste your article, blog, or report here...", value=st.session_state.input_text)

    # Store the value in session_state when the text area value changes
    st.session_state.input_text = input_text

with col2:
    submit = st.button("Generate Summary")

if submit:
    if not input_text.strip():
        st.warning("Please provide some text to summarize.")
    else:
        with st.spinner("Generating summary..."):
            # Directly pass input text to the summarizer
            output = summarizer.summarize(input_text)

        st.markdown("---")
        st.markdown("### ✨ Summary Output")
        st.markdown(f"<div class='summary-box'>{output}</div>", unsafe_allow_html=True)
