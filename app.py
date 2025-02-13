import streamlit as st
import pandas as pd
import anthropic  # Use Claude API
import os  

# Set up Claude API Key
api_key = os.getenv("CLAUDE_API_KEY")  
if not api_key:
    st.error("❌ Error: Claude API key is missing. Make sure it is set in secrets.toml!")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

# Load Excel File
@st.cache_data  
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
        # Debugging: Show first 5 characters of API Key
        st.write(f"🔍 Debug: API Key Detected: {api_key[:5]}*****")

        # Safe data handling
        prompt = f"Here is an Excel dataset:\n{df.head(10).to_string()}\n\nQuestion: {question}\nProvide an answer in detail:"

        try:
            response = client.messages.create(
                model="claude-3-opus-2024-02-08",
                max_tokens=300,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            st.write("### Answer:", response.content[0].text)

        except Exception as e:
            st.error(f"❌ Claude API Error: {str(e)}")
