"""
News Article Summarization App using Hugging Face Transformers
Powered by Streamlit
"""

import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Cache model loading to improve performance
@st.cache_resource
def load_model(model_name):
    """Load model and tokenizer with caching"""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

# Page configuration
st.set_page_config(
    page_title="News Summarizer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
    .summary-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066cc;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("📰 News Article Summarizer")
st.markdown("**Transform long articles into concise summaries instantly**")
st.divider()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model selection
    model_choice = st.radio(
        "Select Summarization Model:",
        options=["T5-small", "BART (Large CNN)"],
        help="T5 is faster, BART is more accurate"
    )
    
    # Model mapping
    if model_choice == "T5-small":
        model_name = "t5-small"
        use_t5 = True
    else:
        model_name = "facebook/bart-large-cnn"
        use_t5 = False
    
    # Summary parameters
    st.subheader("📊 Summary Parameters")
    min_length = st.slider(
        "Minimum Summary Length (words):",
        min_value=10,
        max_value=50,
        value=30,
        step=5
    )
    
    max_length = st.slider(
        "Maximum Summary Length (words):",
        min_value=50,
        max_value=150,
        value=100,
        step=10
    )
    
    num_beams = st.slider(
        "Beam Search Width:",
        min_value=2,
        max_value=8,
        value=4,
        help="Higher = better quality but slower"
    )
    
    st.divider()
    st.info("💡 **Tip:** Paste a news article in the text area and click Summarize!")

# Main content area
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Input Article")
    user_article = st.text_area(
        "Paste your news article here:",
        height=300,
        placeholder="Paste a news article (min 50 words recommended)...",
        label_visibility="collapsed"
    )

with col2:
    st.subheader("✨ Generated Summary")
    summary_placeholder = st.empty()

st.divider()

# Main action button
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    summarize_button = st.button(
        "🚀 Summarize Article",
        use_container_width=True,
        type="primary"
    )

with col_btn2:
    clear_button = st.button(
        "🗑️ Clear All",
        use_container_width=True
    )

# Session state management
if "summary_result" not in st.session_state:
    st.session_state.summary_result = None

if "article_text" not in st.session_state:
    st.session_state.article_text = None

if clear_button:
    st.session_state.summary_result = None
    st.session_state.article_text = None
    st.rerun()

# Summarization logic
if summarize_button:
    # Validation
    if not user_article or len(user_article.strip()) < 50:
        st.error("❌ Please paste an article with at least 50 words.")
    else:
        try:
            # Show loading spinner
            with st.spinner("🔄 Loading model and generating summary..."):
                
                # Load model and tokenizer using cache
                st.info("📥 Loading model (first run may take a minute)...")
                tokenizer, model = load_model(model_name)
                
                # Move to CPU (no GPU assumption)
                device = torch.device("cpu")
                model.to(device)
                model.eval()
                
                # Prepare input
                article_text = user_article.strip()
                
                # Add prefix for T5 models
                if use_t5:
                    article_text = "summarize: " + article_text
                
                # Tokenize and truncate to max 512 tokens
                inputs = tokenizer(
                    article_text,
                    max_length=512,
                    truncation=True,
                    return_tensors="pt"
                )
                
                # Move inputs to device
                inputs = {k: v.to(device) for k, v in inputs.items()}
                
                # Generate summary
                summary_ids = model.generate(
                    inputs["input_ids"],
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=num_beams,
                    early_stopping=True
                )
                
                # Decode summary
                summary = tokenizer.batch_decode(
                    summary_ids,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=True
                )[0]
                
                # Store in session state
                st.session_state.summary_result = summary
                st.session_state.article_text = user_article
        
        except Exception as e:
            st.error(f"❌ Error during summarization: {str(e)}")
            st.info("Make sure you have enough memory and internet to download the model.")

# Display summary if available
if st.session_state.summary_result:
    with summary_placeholder.container():
        st.markdown(
            f'<div class="summary-box"><p><strong>Summary:</strong></p><p>{st.session_state.summary_result}</p></div>',
            unsafe_allow_html=True
        )
        
        # Summary statistics
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            original_words = len(st.session_state.article_text.split())
            st.metric("Original Length", f"{original_words} words")
        
        with col_stat2:
            summary_words = len(st.session_state.summary_result.split())
            st.metric("Summary Length", f"{summary_words} words")
        
        with col_stat3:
            compression = round((1 - summary_words / original_words) * 100, 1)
            st.metric("Compression", f"{compression}%")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: gray; font-size: 12px;">
    <p>Built with ❤️ using Streamlit & Hugging Face Transformers</p>
    <p>Models: T5-small | BART-large-cnn</p>
    </div>
    """, unsafe_allow_html=True)
