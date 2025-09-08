import streamlit as st
import pandas as pd

def setup_page():
    st.set_page_config(
        page_title="Stock Sentiment Analysis",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    create_sidebar()

def initialize_session_state():
    # init session state var's if they dont exist
    if 'ticker' not in st.session_state:
        st.session_state.ticker = ""
    if 'avg_polarity' not in st.session_state:
        st.session_state.avg_polarity = 0.0
    if 'avg_subjectivity' not in st.session_state:
        st.session_state.avg_subjectivity = 0.0
    if 'overall_sentiment' not in st.session_state:
        st.session_state.overall_sentiment = "Neutral"
    if 'news_df' not in st.session_state:
        st.session_state.news_df = pd.DataFrame()
    if 'combined_sentiment' not in st.session_state:
        st.session_state.combined_sentiment = None
    if 'analysis_performed' not in st.session_state:
        st.session_state.analysis_performed = False
    if 'num_articles' not in st.session_state:
        st.session_state.num_articles = 3 


def create_sidebar():
    st.sidebar.header("Settings")

    st.sidebar.slider(
        "Number of articles to analyze",
        min_value=1,
        max_value=10,
        value=st.session_state.get('num_articles',3),
        key="num_articles"
    )