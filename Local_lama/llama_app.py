# Adapted from   https://www.youtube.com/watch?v=J8TgKxomS2g
# and https://github.com/phidatahq/phidata/blob/main/cookbook/llms/groq/rag/app.py
import streamlit as st
# Load the model using Ollama from langchain
from langchain_community.llms import Ollama
from langchain_openai.chat_models import ChatOpenAI
import pandas as pd
from io import StringIO

st.set_page_config(
    page_title="Llama3: Talk to your documents",
    page_icon=":accept:",
)
st.title("Talk to your documents locally")

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def generate_llama3_response(prompt_input, model):
    # This is testing the connetion to the model works: 
    output = model.invoke(prompt_input)
    print(output)
    return output

def get_response_with_document(uploaded_file, prompt, model, emb_model):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    spliter = RecursiveCharacterTextSplitter(chunk_size = 200,chunk_overlap = 50)
    chunks = spliter.split_text(string_data)
    #st.write(string_data[:100])
    # print(chunks[:50])
    from langchain_community.embeddings import OllamaEmbeddings
    # from langchain.vectorstores import FAISS
    from langchain_community.vectorstores import FAISS
    # embeddings = OllamaEmbeddings(base_url = 'http://localhost:11434', model="llama3")
    #Using nomid-emde-text model allow for faster embedings, the above on llama never finished. 
    embeddings = OllamaEmbeddings(model=emb_model)
    # Get your docsearch ready
    docsearch = FAISS.from_texts(chunks[:50], embeddings)
    from langchain.chains import RetrievalQA
    qa_model = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=docsearch.as_retriever())
    # Run a query
    result = generate_llama3_response(prompt, qa_model)
    return result

llm_model = st.sidebar.selectbox("Select an LLM: ", options=[None, "llama3", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"])
API_KEY = "NA" #Causes ChatOpenAI to look for local models. base-url is needed to use ollama

if llm_model:
    uploadedfile = None
    llm3 = ChatOpenAI(api_key = API_KEY,model= llm_model, base_url="http://localhost:11434/v1", streaming=True)
    st.sidebar.success('Proceed to entering your prompt message!', icon='👉')
    upload = st.sidebar.selectbox("Do you want to add your own documents?", options=["No", 'Yes'])
    if upload == 'Yes':
        uploadedfile = st.file_uploader('Upload Documents herez')
        print('UPFILE', uploadedfile)
        embeddings_model = st.sidebar.selectbox(
        "Select Embeddings",
        options=["nomic-embed-text", "text-embedding-3-small"],
        help="When you change the embeddings model, the documents will need to be added again.",)
    # Store LLM generated responses
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
                    response = get_response_with_document(uploadedfile, prompt, llm3, embeddings_model)
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

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)