import streamlit as st
import groq
import os
from dotenv import load_dotenv
from scraper import fetch_page, extract_text

# Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq Client
client = groq.Client(api_key=GROQ_API_KEY)

def summarize_text(text):
    """Use Groq LLM to summarize extracted text."""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Summarize the following text."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def answer_question(text, question):
    """Use Groq LLM to answer questions based on extracted text."""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Answer questions based on the provided text."},
            {"role": "user", "content": f"Text: {text}\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("🌍 AI-Powered Web Scraper with Groq API")

# User input for URL
url = st.text_input("Enter a website URL", "")

if st.button("Extract & Summarize"):
    st.write(f"Fetching data from {url}...")

    html_content = fetch_page(url)
    if html_content:
        extracted_text = extract_text(html_content)
        st.text_area("Extracted Text", extracted_text, height=200)

        # Summarize text
        summary = summarize_text(extracted_text)
        st.subheader("🔍 Summarized Content")
        st.write(summary)

# Q&A Section
st.subheader("💡 Ask a Question")
user_question = st.text_input("Type your question here")

if st.button("Get Answer") and user_question:
    if url:
        extracted_text = extract_text(fetch_page(url))
        answer = answer_question(extracted_text, user_question)
        st.write("🧠 AI Answer:", answer)
    else:
        st.warning("Please enter a valid URL first!")
