import streamlit as st
import pandas as pd
import anthropic
import os  # Import os to read environment variables

# Load API Key from Environment Variable
api_key = os.getenv("CLAUDE_API_KEY")

# Ensure API Key is set
if not api_key:
    st.error("❌ API key is missing! Please add your CLAUDE_API_KEY as a GitHub Secret or in Streamlit Secrets.")
    st.stop()

# Initialize Claude API client
client = anthropic.Anthropic(api_key=api_key)

# Function to load Excel File
@st.cache_data
def load_data(file):
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        return None

# Streamlit UI
st.title("📊 Ceres Competitive Research Database")
st.write("Upload an Excel file and ask questions about the data.")

# Upload Excel File
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)

    if df is not None:
        st.write("### Data Preview:")
        st.dataframe(df)

        question = st.text_input("💬 Ask a question about your data:")

        if question:  # <-- The previous error was likely due to missing indentation here
            # Convert DataFrame to string with a reasonable character limit
            data_preview = df.to_string(max_rows=50, max_cols=10)  # Limits excessive token usage

            prompt = f"Here is a dataset:\n{data_preview}\n\nAnswer the following question: {question}"

            try:
                response = client.messages.create(
                    model="claude-3-opus-2024-02-08",  # Updated to latest Claude model
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                st.write("### ✅ Answer:", response.content[0].text)
            except anthropic.APIError as e:
                st.error(f"❌ Claude API request failed: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
