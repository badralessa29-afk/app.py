import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI PDF Research Agent", page_icon="📄")

st.title("AI PDF Research Agent")

# الأفضل لاحقًا تحط المفتاح في Secrets
api_key = st.text_input("Enter OpenAI API Key", type="password")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")
question = st.text_input("Ask a question about the PDF")

def extract_pdf_text(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

if st.button("Analyze"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif uploaded_file is None:
        st.error("Please upload a PDF file first.")
    elif not question.strip():
        st.error("Please enter your question.")
    else:
        try:
            pdf_text = extract_pdf_text(uploaded_file)

            if not pdf_text:
                st.error("Could not extract text from this PDF.")
            else:
                client = OpenAI(api_key=api_key)

                prompt = f"""
You are a helpful PDF research assistant.
Answer only based on the PDF content below.

PDF content:
{pdf_text}

User question:
{question}
"""

                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=prompt
                )

                st.subheader("AI Response")
                st.write(response.output_text)

        except Exception as e:
            st.error(f"Error: {e}")
