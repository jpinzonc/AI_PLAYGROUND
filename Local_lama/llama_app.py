# Adapted from   https://www.youtube.com/watch?v=J8TgKxomS2g
import streamlit as st
# Remove these: 
# import replicate
# import os
# Load the model using Ollama from langchain
from langchain_community.llms import Ollama
from langchain_openai.chat_models import ChatOpenAI
import pandas as pd
from io import StringIO
# Generate the model
# llm3 = Ollama(model ='llama3')
# Modified following https://www.youtube.com/watch?v=02cdCd43Ccc 
API_KEY = "NA" #Causes ChatOpenAI to look for local models. base-url is needed to use ollama
Model = 'llama3'
llm3 = ChatOpenAI(api_key = API_KEY,model= Model, base_url="http://localhost:11434/v1", streaming=True)
# gpt_llm.invoke('what is a bot')
# App title
# Change the tile to Llama 3
# st.set_page_config(page_title="🦙💬 Llama 3 Chatbot - Local with Ollama")

# Replicate Credentials
with st.sidebar:
    #### Remove Replicate secciont
    # st.title('🦙💬 Llama 3 Chatbot')
    # if 'REPLICATE_API_TOKEN' in st.secrets:
    #     st.success('API key already provided!', icon='✅')
    #     replicate_api = st.secrets['REPLICATE_API_TOKEN']
    # else:
    #     replicate_api = st.text_input('Enter Replicate API token:', type='password')
    #     if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
    #         st.warning('Please enter your credentials!', icon='⚠️')
    #     else:
    st.success('Proceed to entering your prompt message!', icon='👉')
    uploadedfile = st.file_uploader('upload_a_file')

    # st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')
# os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
# Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama3_response(prompt_input, llm3):
    # This is testing the connetion to the model works: 
    output = llm3.invoke(prompt_input)
    # string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    # for dict_message in st.session_state.messages:
    #     if dict_message["role"] == "user":
    #         string_dialogue += "User: " + dict_message["content"] + "\n\n"
    #     else:
    #         string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    # output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
    #                        input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
    #                               "temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})
    return output.content

qa = None 
prompt = st.chat_input()
print('UPFILE', uploadedfile)
def get_response_with_document(uploaded_file, prompt, model):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    spliter = RecursiveCharacterTextSplitter(chunk_size = 200,chunk_overlap = 50)
    chunks = spliter.split_text(string_data)
    st.write(string_data[:100])
    # print(chunks[:50])
    from langchain_community.embeddings import OllamaEmbeddings
    # from langchain.vectorstores import FAISS
    from langchain_community.vectorstores import FAISS
    # embeddings = OllamaEmbeddings(base_url = 'http://localhost:11434', model="llama3")
    #Using nomid-emde-text model allow for faster embedings, the above on llama never finished. 
    embeddings = OllamaEmbeddings(model='nomic-embed-text')
    # Get your docsearch ready
    docsearch = FAISS.from_texts(chunks[:50], embeddings)
    from langchain.chains import RetrievalQA
    qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=docsearch.as_retriever())
    # Run a query
    result = generate_llama3_response(prompt, qa)
    return result

# User-provided prompt
if prompt: #!= st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if uploadedfile == None: 
                response = generate_llama3_response(prompt, llm3)
            else: 
                response = get_response_with_document(uploadedfile, prompt, llm3)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)