import streamlit as st
import pandas as pd
import anthropic
import os  # Import os to read environment variables

# Load API Key from Environment Variable
api_key = os.getenv("CLAUDE_API_KEY")

# Ensure API Key is set
if not api_key:
    st.error("API key is missing! Please add your CLAUDE_API_KEY as a GitHub Secret.")
    st.stop()

# Initialize Claude API client
client = anthropic.Anthropic(api_key=api_key)

# Function to load Excel File
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    return df

# Streamlit UI
st.title("📊 Ceres Competitive Research Database")
st.write("Upload an Excel file and ask questions about the data.")

# Upload Excel File
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)
    st.write("### Data Preview:", df.head())

    question = st.text_input("Ask a question about your data:")
    
    if question:
        prompt = f"Based on this dataset:\n{df.to_string()}\nAnswer the following: {question}"
        
        try:
            response = client.messages.create(
                model="claude-3-opus",  # Updated to the latest working Claude model
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            st.write("### Answer:", response.content[0].text)
        except Exception as e:
            st.error(f"Error in Claude API request: {str(e)}")
