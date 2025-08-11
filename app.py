import streamlit as st
from backend.llama_index_setup import query_index

st.set_page_config(page_title="Study Portal", layout="wide")

st.title("🎓 Smart College Portal with AI Assistant")
st.markdown("Ask about roadmaps, notes")

query = st.text_input("Enter your question:")
if st.button("Ask") and query:
    with st.spinner("Thinking..."):
        response = query_index(query)
        st.write(response)
