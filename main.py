import streamlit as st 
import pandas as pd
from config import setup_page, initialize_session_state
from data import perform_stock_news_analysis
from ui import display_analysis_results

setup_page()
initialize_session_state()


def main():

    st.header("Analyze Stock Sentiment")
    
    ticker = st.text_input(
        "Enter stock symbol:",
        value=st.session_state.get('ticker',''),
        placeholder="BX,BLK,JPM....",
        help="Enter the ticker symbol you want to analyze"
    ).upper()

    # update session state when it changes
    if ticker:
        st.session_state.ticker = ticker

    col1, col2 = st.columns(2)
    with col1:
        analyze_button = st.button("Analyze")

    with col2:
        if st.button("Clear Results"):
            st.session_state.analysis_performed = False
            st.session_state.ticker = ""
            st.session_state.news_df = pd.DataFrame()
            st.session_state.combined_sentiment = None
            st.rerun()  
                
    # perform analysis when button is pressed or if we have saved results
    if analyze_button:
        results = perform_stock_news_analysis(ticker)
        if results:
            display_analysis_results(ticker, *results)
    elif st.session_state.analysis_performed and st.session_state.ticker:
        # display
        display_analysis_results(
            st.session_state.ticker,
            st.session_state.avg_polarity,
            st.session_state.avg_subjectivity,
            st.session_state.overall_sentiment,
            st.session_state.news_df,
            st.session_state.combined_sentiment
        )


if __name__ == "__main__":
    main()