# Adapted from   https://www.youtube.com/watch?v=J8TgKxomS2g
# and https://github.com/phidatahq/phidata/blob/main/cookbook/llms/groq/rag/app.py
import streamlit as st

st.set_page_config(
    page_title="Llama3: Llama3 Playground",
    page_icon=":accept:",
)
st.divider()
st.title("Llama interactions")
st.write(" This app has two exaples: ")
st.write("1. Llama Chat to talk to the documents. ")
st.write("2. Llama Rag")
st.divider()