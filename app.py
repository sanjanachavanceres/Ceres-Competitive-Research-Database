import streamlit as st
import pandas as pd
import anthropic  # Use Claude API instead of OpenAI
import os  # Import os for environment variables

# Set up Claude API Key
api_key = os.getenv("CLAUDE_API_KEY")  # Get API key from GitHub Secrets
client = anthropic.Anthropic(api_key=api_key)

# Load Excel File
@st.cache_data  # Updated from @st.cache to @st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    return df

# Streamlit UI
st.title("📊 Ceres Competitive Research Database")
st.write("Upload an Excel file and ask questions about the data.")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)
    st.write("### Data Preview:", df.head())

    question = st.text_input("Ask a question about your data:")
    
    if question:
        prompt = f"Based on this dataset:\n{df.to_string()}\nAnswer: {question}"
        response = client.messages.create(
            model="claude-3-opus-2024-02-08",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        st.write("### Answer:", response.content[0].text)
