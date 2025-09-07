import requests
from bs4 import BeautifulSoup
import re
import streamlit as st

def extract_article_text(url):
    try:
        # add user agent so we dont get blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

        # send requests to the page
        response = requests.get(url, headers=headers,timeout=10)

        if response.status_code != 200:
            return ""

        # parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # remove script and style elements that might contain irrelevant text
        for script_or_style in soup(['script','style','header','footer','nav']):
            script_or_style.extract()

        # get all paragraphs which usually contain the main article text
        paragraphs = soup.find_all('p')

        # join paragraphs to form the complete article text
        article_text = ' '.join([p.get_text().strip() for p in paragraphs])

        # clean up the text (remove extra whitespace)
        article_text = article_text.replace("Oops, something went wrong Unlock stock picks and a broker-level newsfeed that powers Wall", "")

        return article_text
    except Exception as e:
        st.warning(f"Could not extract text from {url}, Error: {str(e)}")
        return ""
