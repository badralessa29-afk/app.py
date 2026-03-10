import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI PDF Research Agent", page_icon="📄")

# قراءة المفتاح من Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI PDF Research Agent")

# رفع ملف PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# سؤال المستخدم
question = st.text_input("Ask a question about the PDF")

# استخراج النص من ملف PDF
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()

# زر التحليل
if st.button("Analyze"):
    if uploaded_file is None:
        st.error("Please upload a PDF first.")
    elif not question.strip():
        st.error("Please enter a question.")
    else:
        try:
            pdf_text = extract_pdf_text(uploaded_file)

            if not pdf_text:
                st.error("Could not extract text from this PDF.")
            else:
                prompt = f"""
You are an AI assistant that analyzes PDF documents.
Answer based only on the PDF content below.

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
