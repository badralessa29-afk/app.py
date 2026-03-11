import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI PDF Research Agent", page_icon="📄")

st.title("AI PDF Research Agent")

# رابط webhook من n8n
N8N_WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]

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
                payload = {
                    "question": question,
                    "pdf_text": pdf_text
                }

                response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=120)

                if response.status_code == 200:
                    data = response.json()

                    st.subheader("AI Response")
                    st.write(data.get("answer", "No answer returned from n8n."))
                else:
                    st.error(f"n8n returned status code {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Error: {e}")
