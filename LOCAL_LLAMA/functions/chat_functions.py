import streamlit as st 
from io import StringIO
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA



def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def generate_llama3_response(prompt_input, model):
    # This is testing the connetion to the model works: 
    output = model.invoke(prompt_input)
    # print(output)
    return output

def get_response_with_document(string_data, prompt, model, emb_model):

    spliter = RecursiveCharacterTextSplitter(chunk_size = 200,chunk_overlap = 50)
    chunks = spliter.split_text(string_data)
    #st.write(string_data[:100])
    # print(chunks[:50])
    embeddings = OllamaEmbeddings(model=emb_model)
    # Get your docsearch ready
    docsearch = FAISS.from_texts(chunks[:50], embeddings)
    qa_model = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=docsearch.as_retriever())
    # Run a query
    result = generate_llama3_response(prompt, qa_model)
    return result