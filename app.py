import streamlit as st
import pandas as pd
import openai

# Set up OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load Excel File
@st.cache
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
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write("### Answer:", response["choices"][0]["message"]["content"])
