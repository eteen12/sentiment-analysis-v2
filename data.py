import time

import pandas as pd 
import streamlit as st
import yfinance as yf
from scraper import extract_article_text
from sentiment import analyze_sentiment, calculate_combined_sentiment

def analyze_stock_news_sentiment(ticker_symbol, num_articles=5):
    news_articles = get_stock_news(ticker_symbol,num_articles)

    if not news_articles:
        return 0.0, 0.0, "Neutral", pd.DataFrame(), None
    
    # make a progress bar for the scraping
    progress_bar = st.progress(0)
    status_text = st.empty()

    # process the results
    results = []
    all_article_texts = []

    for i, article in enumerate(news_articles):
        article_data = process_article(article, i, len(news_articles), status_text)
        results.append(article_data)

        # add full text to collection for combined analysis
        if article_data['raw_text']:
            all_article_texts.append(article_data['raw_text'])

        # update the progress bar
        progress_bar.progress((i + 1) / len(news_articles))

    # clear the progress indicators
    progress_bar.empty()
    status_text.empty()

    # Covert to Dataframe and remove the raw text column (not needed for the display)
    for result in results:
        if 'raw_text' in result:
            del result['raw_text']
    news_df = pd.DataFrame(results)

    # calculate aggregate sentiment metrics
    if not news_df.empty:
        avg_polarity = news_df['full_text_polarity'].mean()
        avg_subjectivity = news_df['full_text_subjectivity'].mean()

        # Determine overall sentiment based on full text analysis
        if avg_polarity > 0.1:
            overall_sentiment = "Positive"
        elif avg_polarity < -0.1:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Neutral"
    else:
        avg_polarity = 0.0
        avg_subjectivity = 0.0
        overall_sentiment = "Neutral"
    
    # perform the sentiment analysis on all articles together
    combined_sentiment = calculate_combined_sentiment(all_article_texts)

    return avg_polarity, avg_subjectivity, overall_sentiment, news_df, combined_sentiment

def perform_stock_news_analysis(ticker):
    if not ticker:
        st.warning("Please enter a stock ticker before analyzing")
        return None

    # check if we already have results for this ticker
    if st.session_state.ticker == ticker and st.session_state.analysis_performed:
        # use the saved results
        return(
            st.session_state.avg_polarity,
            st.session_state.avg_subjectivity,
            st.session_state.overall_sentiment,
            st.session_state.news_df,
            st.session_state.combined_sentiment
        )
    else:
        # show analysis is in progress
        with st.spinner(f"fetching and analyzing recent news for {ticker}..."):
            # get number of articles to analyse 
            num_articles = st.session_state.get('num_articles', 3)

            # perform the analysis
            avg_polarity, avg_subjectivity, overall_sentiment, news_df, combined_sentiment = analyze_stock_news_sentiment(ticker, num_articles)

            # save the results to session state
            st.session_state.ticker = ticker
            st.session_state.avg_polarity = avg_polarity
            st.session_state.avg_subjectivity = avg_subjectivity
            st.session_state.overall_sentiment = overall_sentiment
            st.session_state.news_df = news_df
            st.session_state.analysis_performed = True

            # check if we got any news
            if news_df.empty:
                st.warning(f"No news articles found for ticker {ticker}. Please check the ticker symbol and try again")
                return None
            return avg_polarity,avg_subjectivity,overall_sentiment,news_df,combined_sentiment


def process_article(article,index,total_articles, status_text):
    status_text.text(f"Processing article {index + 1} of {total_articles}...")

    article_url = article.get('link','')
    title = article.get('title','')
    summary = article.get('summary','')
    publisher = article.get('publisher', 'Unknown Publisher')

    #For headline sentiment
    headline_text = f"{title} {summary}"
    headline_polarity,headline_subjectivity, headline_sentiment = analyze_sentiment(headline_text)
   

    # Get the full text if the URL is there
    article_full_text = ""
    if article_url:
        status_text.text(f"Extracting text from article {index + 1}...")
        article_full_text = extract_article_text(article_url)
        time.sleep(0.5) # To avoid overloading servers

    if article_full_text:
        full_text_polarity, full_text_subjectivity, full_text_sentiment = analyze_sentiment(article_full_text)
    else:
        # Use headline sentiment if full text is not available
        full_text_polarity, full_text_subjectivity, full_text_sentiment = headline_polarity, headline_sentiment, headline_subjectivity
        article_full_text = "Could not extract full article text"

    return{
        'title': title,
        'publisher': publisher,
        'published': article.get('published','Unknown'),
        'link': article_url,
        'headline_polarity': headline_polarity,
        'headline_subjectivity': headline_subjectivity,
        'headline_sentiment': headline_sentiment,
        'full_text_polarity': full_text_polarity,
        'full_text_subjectivity': full_text_subjectivity,
        'full_text_sentiment': full_text_sentiment,
        'article_text': article_full_text[:500] + ("..." if len(article_full_text) > 500 else article_full_text),
        'published': article.get('providerPublishTime','Unknown'),
        'raw_text':article_full_text
        
    }

def get_stock_news(ticker_symbol,num_articles=5):
    try:
        news = yf.Search(ticker_symbol, news_count=num_articles).news
        print(news)

        if news and len(news) > 0:
            return news[:num_articles]
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching news for {ticker_symbol}: {e}")
        return []