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

def display_article_details(row):
    
    pub_time = row['published']
    if isinstance(pub_time, int):
        pub_time = datetime.fromtimestamp(pub_time).strftime('%Y-%m-%d %H:%M:%S')

    st.write(f"**Publisher:** {row['publisher']} - {pub_time}")

    st.write("### Sentiment Analysis")

    st.write(f"**Sentiment:** {row['full_text_sentiment']}")
    st.write(f"**Polarity:** {row['full_text_polarity']:.2f}")
    st.write(f"**Subjectivity:** {row['full_text_subjectivity']:.2f}")

     # Article text preview and link
    st.write("### Article Preview")
    st.write(row['article_text'])
    st.write(f"**Full Article:** [{row['title']}]({row['link']})")                                                                                                                       

def display_news_articles(ticker, news_df):

    st.subheader(f"Recent News Articles for {ticker}")

    for i, row in news_df.iterrows():
        with st.expander(f"{row['title']}"):
            display_article_details(row)

def display_analysis_results(ticker, avg_polarity, avg_subjectivity, overall_sentiment, news_df, combined_sentiment):
    # Display combined sentiment analysis if available
    display_combined_sentiment(combined_sentiment)

    # Display news articles with their sentiment
    display_news_articles(ticker, news_df)

