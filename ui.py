import streamlit as st
from datetime import datetime

def create_main_section():
    st.title("Stock Sentiment Analysis")
    st.write("Enter a stock ticker to get sentiment analysis based on recent news"),
    st.markdown("---")

def display_combined_sentiment(combined_sentiment):
    if not combined_sentiment:
        return

    st.subheader("Combined sentiment analysis")
    st.write("This analysis combines all the text of all the articles to get a combined sentiment analysis")

    combined_cols = st.columns(3)
    with combined_cols[0]:
        st.metric(
            label="Combined Sentiment",
            value=f"{combined_sentiment['sentiment']}"
        )
    with combined_cols[1]:
        st.metric(
            label="Combined Polarity",
            value=f"{combined_sentiment['polarity']:.2f}"
        )
    with combined_cols[2]:
        st.metric(
            label="Combined Subjectivity",
            value=f"{combined_sentiment['subjectivity']:.2f}"   
        )