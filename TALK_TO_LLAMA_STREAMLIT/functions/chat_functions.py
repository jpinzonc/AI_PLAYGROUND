import streamlit as st 
from io import StringIO
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

def clear_chat_history():
    '''
    Resets the session_state of the application to original. 
    '''
    st.session_state.messages = [{"role": "assistant", "content": "WHAT DO YOU WANT TO TALK ABOUT?"}]
    st.session_state.file = None
    try: 
        del st.session_state.file_uploader_key 
    except: 
        pass
    try: 
        del st.session_state.uploaded_files
    except: 
        pass
    try: 
        del st.session_state.string_data
    except: 
        pass
    try: 
        del st.session_state.image_data
    except: 
        pass
    try: 
        st.session_state["file_uploader_key"] += 1
        
    except: 
        pass

def delete_string():
    try: 
        del st.session_state.string_data
    except: 
        print('Nothing to delete')

def generate_llama3_response(prompt_input, model):
    '''
    It uses the model to generate a response to the input provided in prompt_input.

    Args:
        prompt_input  
        model.  

    Returns: 
         str: output as the final result of the function.
    '''
    output = model.invoke(prompt_input)
    return output

def get_response_with_document(string_data, prompt, model, emb_model):
    '''
    Get a response to a given prompt by searching through a document and retrieving relevant information.

    Args:
        string_data (str): The text of the document.
        prompt (str): The query prompt.
        model (str): The name of the language model used for generation.
        emb_model (str): The name of the embeddings model used for retrieval.

    Returns:
        str: The response to the given prompt.
    '''
    result =  'No Data'
    if string_data != '':
        try: 
            spliter = RecursiveCharacterTextSplitter(chunk_size = 200,chunk_overlap = 50)
            chunks = spliter.split_text(string_data)
            #st.write(string_data[:100])
            # print(chunks[:50])
            embeddings = OllamaEmbeddings(model=emb_model)
            # Get your docsearch ready
            docsearch = FAISS.from_texts(chunks, embeddings)
            qa_model = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=docsearch.as_retriever())
            # Run a query
            result = generate_llama3_response(prompt, qa_model)
        except: 
            result = 'No Data'
    return result

def ollama_available_models():
    models_info = ollama.list()
    available_models = [m["name"] for m in models_info["models"]]
    return available_models