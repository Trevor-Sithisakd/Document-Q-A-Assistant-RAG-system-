import streamlit as st 
import requests


API_BASE = "http://localhost:8000"


def call_api(path: str, **kwargs) -> dict:
    try:
        response = requests.post(f"{API_BASE}{path}", timeout=120, **kwargs)
    except requests.RequestException as exc:
        st.error(f"Could not reach the backend at {API_BASE}: {exc}")
        st.stop()

    if not response.ok:
        error_detail = response.text.strip() or "No response body returned."
        try:
            error_json = response.json()
            if isinstance(error_json, dict) and "detail" in error_json:
                error_detail = str(error_json["detail"])
            else:
                error_detail = str(error_json)
        except ValueError:
            pass

        st.error(f"API request failed ({response.status_code}): {error_detail}")
        st.stop()

    try:
        return response.json()
    except ValueError:
        st.error(
            "The backend returned a success status but not valid JSON. "
            f"Response body: {response.text[:500] or '[empty body]'}"
        )
        st.stop()

st.title("Enterprise Document Q&A Assistant")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file and st.button("Process Document"):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    result = call_api("/ingest", files=files)
    st.write(result)

question = st.text_input("Ask a question about the uploaded documents")

if st.button("Get Answer") and question:
    result = call_api(
        "/query",
        json={"question": question, "top_k": 4}
    )

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Citations")
    for citation in result["citations"]:
        st.write(f"{citation['source']} - page {citation['page']}")

    st.subheader("Latency")
    st.write(f"{result['latency_ms']} ms")
