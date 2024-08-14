# https://www.youtube.com/watch?v=bAI_jWsLhFM
# https://github.com/tonykipkemboi/ollama_streamlit_demos/blob/main/pages/02_%F0%9F%8C%8B_Multimodal.py
import ollama
import streamlit as st 
from openai import OpenAI

st.set_page_config(
    page_title="Chat playground",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    """
    The main function that runs the application.
    """
    st.subheader("Ollama Playground", divider="red", anchor=False)

if __name__ == "__main__":
    main()