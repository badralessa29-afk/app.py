import streamlit as st
import requests

st.title("AI PDF Research Agent")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
question = st.text_input("Ask a question about the PDF")

WEBHOOK_URL = "https://baderalessa.app.n8n.cloud/webhook/pdf-agent"

if st.button("Analyze"):
    if uploaded_file and question:
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
        }

        data = {
            "question": question
        }

        response = requests.post(WEBHOOK_URL, files=files, data=data)

        st.subheader("AI Response")
        st.write(response.text)
    else:
        st.warning("Please upload a PDF and ask a question.")
