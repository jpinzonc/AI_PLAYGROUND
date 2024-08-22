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
    page_icon="shark",
)
def delete_string():
    try: 
        del st.session_state.string_data
    except: 
        print('Nothing to delete')

st.header(":flag-co: Talk to LLAMA locally", divider="gray", anchor=False)

with st.sidebar:
    ollama_models = os.getenv('ollama_models')
    ollama_models  = ollama_models.split(',')
    ollama_models.insert(0, None)
    llm_model = st.selectbox("Select an LLM: ", options= ollama_models)
    API_KEY = "NA" # Set to NA since we are not using Open AI, but Llama
    if llm_model: 
        st.success('Start a conversation', icon='👉')
        st.success('Or select other options', icon= '👇')
        uploadedfile = st.file_uploader('Upload Documents', type=["pdf", 'md', 'txt'], accept_multiple_files=False, on_change = delete_string, help='Upon change the process restarts')
        embeding_models = os.getenv('embed_models').split(',')
        if len(embeding_models) > 1:
            embeddings_model = st.selectbox(
                                        "Select Embeddings",
                                        options=os.getenv('embed_models').split(','),
                                        help="When you change the embeddings model, the documents will need to be added again.",
                                        )
        else: 
            embeddings_model = embeding_models[0]
            st.info(f'''For embedings, using: 
                    **{embeddings_model}**''')
        
        if uploadedfile == None:
            delete_string()
        
        with st.expander(f'Fine Tune Model {llm_model}'):
            temp = st.slider('Temperature', min_value = 0.0, max_value = 2.0, step = 0.01, value = 0.5)
            top_p = st.slider('Top_P', min_value = 0.0, max_value = 1.0, step = 0.01, value = 0.5)
            llm3 = ChatOpenAI(api_key = API_KEY, model= llm_model, base_url="http://localhost:11434/v1"
                        , streaming=True, temperature = temp, top_p = top_p)

    # Store LLM generated responses
    st.button('CLEAR CHAT', on_click = clear_chat_history, use_container_width=True)  
# Display or clear chat messages

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "WHAT DO YOU WANT TO TALK ABOUT?"}]
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "😎"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])  

prompt = st.chat_input(placeholder = 'Enter your question here!')
# User-provided prompt
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
else: 
    prompt = 'Why are sharks cool? '
# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if uploadedfile == None:
                response = generate_llama3_response(prompt, llm3)
                response = response.content
            else: 
                if 'string_data' in st.session_state:
                    string_data = st.session_state.string_data
                    response = get_response_with_document(string_data, prompt, llm3, embeddings_model)
                elif uploadedfile.name[-3:]=='pdf':
                    temp_dir = tempfile.mkdtemp()
                    path = os.path.join(temp_dir, uploadedfile.name)
                    with open(path, "wb") as f:
                        f.write(uploadedfile.getvalue())
                    #string data is a list
                    string_data = LlamaParse(api_key=llama_parser, result_type="markdown").load_data(path)
                    if string_data == []:
                        st.error('Document appears to be empty')
                        string_data = ''
                    else: 
                        string_dataf = ''
                        for i, str_ in enumerate(string_data):
                            string_dataf = string_dataf + string_data[i].text
                        string_data = string_dataf
                else: 
                    stringio = StringIO(uploadedfile.getvalue().decode("utf-8"))
                    string_data = stringio.read()
                
                response = get_response_with_document(string_data, prompt, llm3, embeddings_model)                
                if response !=  'No Data':
                    response = response['result']
                    if 'string_data' not in st.session_state or st.session_state.string_data == None:
                        st.session_state.string_data = string_data
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

# else: 
#     uploadedfile = None
#     st.info('Model not selected - Select a model to start')