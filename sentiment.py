from textblob import TextBlob

def analyze_sentiment(text):

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity # -1 negative to 1 positive
    subjectivity = blob.sentiment.subjectivity # 0 objective to 1 subjective

    # classify sentiment based on polarity
    if polarity > 0.1:
        sentiment_label = "Positive"
    elif polarity < -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return polarity, subjectivity, sentiment_label

    
def calculate_combined_sentiment(article_texts):

    combined_text = " ".join(article_texts)
    if not combined_text:
        return None

    combined_polarity, combined_subjectivity, combined_sentiment_label = analyze_sentiment(combined_text)

    return{
        'polarity': combined_polarity,
        'subjectivity': combined_subjectivity,
        'sentiment': combined_sentiment_label,
    }
