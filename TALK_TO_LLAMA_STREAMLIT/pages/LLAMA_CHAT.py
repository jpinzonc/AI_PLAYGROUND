# Adapted from   https://www.youtube.com/watch?v=J8TgKxomS2g
# and https://github.com/phidatahq/phidata/blob/main/cookbook/llms/groq/rag/app.py
import streamlit as st
from functions.chat_functions import *

import pandas as pd
from io import StringIO
from langchain_openai.chat_models import ChatOpenAI
import tempfile
import sys, os
from llama_parse import LlamaParse 

sys.path.append(os.path.abspath(os.path.join('..', 'secret')))
from secret_info import llama_parser

st.set_page_config(
    page_title="Llama3: Talk to LLAMA",
    page_icon=":accept:",
)
st.title("Talk to LLAMA locally")

with st.sidebar:
    llm_model = st.selectbox("Select an LLM: ", options=[None, "llama3", 'codellama'])
    API_KEY = "NA" # Causes ChatOpenAI to look for local models. base-url is needed to use ollama

    if llm_model:
        uploadedfile = None
        llm3 = ChatOpenAI(api_key = API_KEY, model= llm_model, base_url="http://localhost:11434/v1"
                          , streaming=True, temperature = 0)
        st.success('Proceed to entering your prompt message!', icon='👉')
        upload = st.selectbox("Do you want to add your own documents?", options=["No", 'Yes'])
        if upload == 'Yes':
            uploadedfile = st.file_uploader('Upload Documents', type=["pdf", 'md', 'txt'])
            
            embeddings_model = st.selectbox(
                                            "Select Embeddings",
                                            options=["nomic-embed-text", "text-embedding-3-small"],
                                            help="When you change the embeddings model, the documents will need to be added again.",
                                            )
        # Store LLM generated responses
        st.button('Cleat Chat', on_click = clear_chat_history, use_container_width=True)
    else: 
        st.write('Model not selected')

# Display or clear chat messages

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "WHAT DO YOU WANT TO TALK ABOUT?"}]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])  

prompt = st.chat_input()
# User-provided prompt
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if uploadedfile == None: 
                response = generate_llama3_response(prompt, llm3)
                response = response.content
            else: 
                if uploadedfile.name[-3:]=='pdf':
                    temp_dir = tempfile.mkdtemp()
                    path = os.path.join(temp_dir, uploadedfile.name)
                    with open(path, "wb") as f:
                        f.write(uploadedfile.getvalue())
                    string_data = LlamaParse(api_key=llama_parser, result_type="markdown").load_data(path)
                    string_data = string_data[0].text
                else: 
                    stringio = StringIO(uploadedfile.getvalue().decode("utf-8"))
                    string_data = stringio.read()
                response = get_response_with_document(string_data, prompt, llm3, embeddings_model)
                response = response['result']
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)


