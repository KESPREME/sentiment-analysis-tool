import streamlit as st
from transformers import pipeline
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Sentiment Analysis Tool",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# App title and description
st.title("Sentiment Analysis Tool")
st.write("Analyze the sentiment of any text with this tool.")

# Initialize the sentiment analysis model
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

sentiment_analyzer = load_model()

# Function to analyze sentiment
def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']

# User input section
st.header("Enter Text")
user_text = st.text_area("Type or paste text here:", height=150)
analyze_button = st.button("Analyze Sentiment")

# Process when button is clicked
if analyze_button and user_text:
    with st.spinner("Analyzing sentiment..."):
        sentiment, confidence = analyze_sentiment(user_text)
        
        # Display results
        st.header("Analysis Results")
        st.subheader(f"Sentiment: {sentiment}")
        st.subheader(f"Confidence: {confidence:.2%}")

        # Create visualization
        st.header("Visualization")
        fig, ax = plt.subplots()
        
        sentiments = ['POSITIVE', 'NEGATIVE']
        values = [
            confidence if sentiment == 'POSITIVE' else 0,
            confidence if sentiment == 'NEGATIVE' else 0
        ]
        
        ax.bar(sentiments, values, color=['green', 'red'])
        ax.set_ylim(0, 1)
        ax.set_ylabel('Confidence Score')
        ax.set_title('Sentiment Analysis Results')
        
        st.pyplot(fig)

from autocorrect import Speller

# Add autocorrect option
autocorrect_option = st.checkbox("Enable Autocorrect")

# Function to autocorrect text
def autocorrect_text(text):
    spell = Speller(lang='en')
    return spell(text)

# Apply autocorrection if enabled
if autocorrect_option and user_text:
    corrected_text = autocorrect_text(user_text)
    st.write(f"Corrected text: {corrected_text}")
    user_text = corrected_text
