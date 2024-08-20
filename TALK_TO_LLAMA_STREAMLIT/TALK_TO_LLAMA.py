# Adapted from   https://www.youtube.com/watch?v=J8TgKxomS2g
# and https://github.com/phidatahq/phidata/blob/main/cookbook/llms/groq/rag/app.py
import streamlit as st
import os
from functions.chat_functions import *


st.set_page_config(
    page_title="Llama3: Llama3 Playground",
    page_icon='shark',
)
st.divider()
st.title("Llama interactions")
st.write(" This app has two exaples: ")
st.write("1. Llama Chat to talk to the documents. ")
st.write("2. Llama Rag")
st.write("3. Ollama model Management")

available_models = ollama_available_models()
emb_models =[model for model in available_models if 'embed' in model] #"nomic-embed-text:latest", "snowflake-arctic-embed:latest", "text-embedding-3-small"]
llms = [model for model in available_models if model not in emb_models]

os.environ['all_models'] = ",".join(available_models)
os.environ['ollama_models'] = ",".join(llms)
os.environ['embed_models'] = ",".join(emb_models)
st.divider()