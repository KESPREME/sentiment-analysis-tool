import streamlit as st
import matplotlib.pyplot as plt

# Try importing transformers and autocorrect, show error if missing
try:
    from transformers import pipeline
except ImportError:
    st.error("The 'transformers' library is not installed. Please add 'transformers' to your requirements.txt.")
    st.stop()

try:
    from autocorrect import Speller
except ImportError:
    st.error("The 'autocorrect' library is not installed. Please add 'autocorrect' to your requirements.txt.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Sentiment Analysis Tool",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("Sentiment Analysis Tool")
st.write("Analyze the sentiment of any text with this tool. Supports Positive, Neutral, and Negative sentiment.")

# Load model with 3-way sentiment (POSITIVE, NEUTRAL, NEGATIVE)
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest"
    )

sentiment_analyzer = load_model()

# Autocorrect option
autocorrect_option = st.checkbox("Enable Autocorrect")

def autocorrect_text(text):
    spell = Speller(lang='en')
    return spell(text)

# Analyze sentiment function
def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    label = result['label'].capitalize()
    score = result['score']
    return label, score

# User input
st.header("Enter Text")
user_text = st.text_area("Type or paste text here:", height=150)
if autocorrect_option and user_text:
    corrected_text = autocorrect_text(user_text)
    st.write(f"Corrected text: {corrected_text}")
    user_text = corrected_text

analyze_button = st.button("Analyze Sentiment")

# Process when button is clicked
if analyze_button and user_text:
    with st.spinner("Analyzing sentiment..."):
        sentiment, confidence = analyze_sentiment(user_text)

        # Display results
        st.header("Analysis Results")
        st.subheader(f"Sentiment: {sentiment}")
        st.subheader(f"Confidence: {confidence:.2%}")

        # Personalized feedback
        if sentiment == "Positive":
            st.success("This is a positive statement! 😊")
        elif sentiment == "Negative":
            st.error("This is a negative statement. 😞")
        else:
            st.info("The sentiment is neutral. 😐")

        # Visualization
        st.header("Visualization")
        sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        sentiment_counts[sentiment] = 1

        fig, ax = plt.subplots()
        ax.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['green', 'red', 'gray'])
        ax.set_ylim(0, 1)
        ax.set_ylabel('Count')
        ax.set_title('Sentiment Distribution')
        st.pyplot(fig)

st.markdown("""
---
**Tip:** If you see an error about missing libraries, add `transformers`, `torch`, `matplotlib`, and `autocorrect` to your `requirements.txt` file.
""")
