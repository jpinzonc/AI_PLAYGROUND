# Adapted from   https://www.youtube.com/watch?v=J8TgKxomS2g
# and https://github.com/phidatahq/phidata/blob/main/cookbook/llms/groq/rag/app.py
import streamlit as st
from functions.chat_functions import *

import pandas as pd
from io import StringIO
from langchain_openai.chat_models import ChatOpenAI
from llama_parse import LlamaParse

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'secret')))
from secret_info import llama_parser


st.set_page_config(
    page_title="Llama3: Talk to LLAMA",
    page_icon=":accept:",
)
st.title("Talk to LLAMA locally")

llm_model = st.sidebar.selectbox("Select an LLM: ", options=[None, "llama3", 'codellama'])
API_KEY = "NA" #Causes ChatOpenAI to look for local models. base-url is needed to use ollama
# llm_model = st.sidebar.selectbox("Select an LLM: ", options=[None, "llama3", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"])

if llm_model:
    uploadedfile = None
    llm3 = ChatOpenAI(api_key = API_KEY, model= llm_model, base_url="http://localhost:11434/v1", streaming=True)
    st.sidebar.success('Proceed to entering your prompt message!', icon='👉')
    upload = st.sidebar.selectbox("Do you want to add your own documents?", options=["No", 'Yes'])
    if upload == 'Yes':
        uploadedfile = st.sidebar.file_uploader('Upload Documents')
        
        embeddings_model = st.sidebar.selectbox(
                                                "Select Embeddings",
                                                options=["nomic-embed-text", "text-embedding-3-small"],
                                                help="When you change the embeddings model, the documents will need to be added again.",
                                                )
    # Store LLM generated responses
    st.sidebar.button('Cleat Chat', on_click = clear_chat_history)
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display or clear chat messages
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
                        st.write(uploadedfile)
                        parser = LlamaParse(api_key=llama_parser, result_type="markdown")
                        # for line in uploadedfile.readlines():
                        #     st.write(line)
                        string_data = parser.load_data(uploadedfile.readlines())
                        # string_data = uploadedfile.read()
                        # st.write(uploadedfile)
                        # if uploadedfile.name[-3:]=='pdf':
                        #     pdfb = uploadedfile.getvalue()
                        #     parser = LlamaParse(api_key=llama_parser, result_type="markdown")
                        #     st.write(uploadedfile)
                        #     with open(pdfb, "rb") as f:
                        #         file_bytes = f.read()
                        #         documents = parser.load_data(file_bytes)
                        #     # st.write(uploadedfile.upload_url())
                        #     # print(document[0].text[:1000])
                        #     # file_name = "paper.md"
                        #     # with open(file_name, 'w') as file:
                        #     #     file.write(document[0].text)
                        #     st.write('sOMETHIN')
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
else: 
    st.write('Model not selected')

