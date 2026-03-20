import streamlit as st 
import requests


API_BASE = "http://localhost:8000"

st.title("Enterprise Document Q&A Assistant")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file and st.button("Process Document"):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    response = requests.post(f"{API_BASE}/ingest", files=files)
    st.write(response.json())

question = st.text_input("Ask a question about the uploaded documents")

if st.button("Get Answer") and question:
    response = requests.post(
        f"{API_BASE}/query",
        json={"question": question, "top_k": 4}
    )
    result = response.json()

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Citations")
    for citation in result["citations"]:
        st.write(f"{citation['source']} - page {citation['page']}")

    st.subheader("Latency")
    st.write(f"{result['latency_ms']} ms")