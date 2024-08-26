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

st.header(":flag-co: Talk to LLAMA locally", divider="gray", anchor=False)

with st.sidebar:
    textext = ["pdf", 'md', 'txt']
    imgext = ['png', 'jpg', 'jpeg']
    st.write(st.session_state)
    ollama_models = os.getenv('ollama_models')
    ollama_models  = ollama_models.split(',')
    ollama_models.insert(0, None)
    llm_model = st.selectbox("Select an LLM: ", options= ollama_models)
    API_KEY = "NA" # Set to NA since we are not using Open AI, but Llama
    uploadedfile = dataimg = datatext = None  
    if llm_model: 
        if "file_uploader_key" not in st.session_state:
            st.session_state["file_uploader_key"] = 0
        if "uploaded_files" not in st.session_state:
            st.session_state["uploaded_files"] = []
        st.success('Start a conversation', icon='👉')
        if 'llama3' in llm_model:
            st.success('Or select other options', icon= '👇')
            uploadedfile = st.file_uploader('Upload Documents', type=textext +imgext
                                            , accept_multiple_files=False
                                            , on_change = delete_string
                                            , help='Upon change the process restarts'
                                            , key=st.session_state["file_uploader_key"])

            if uploadedfile: 
                st.session_state["uploaded_files"] = uploadedfile
                extn = uploadedfile.name[-3:].split('.')[-1].lower()
                datatext = True if extn in textext else None
                dataimg  = True if extn in imgext else None
                if datatext: 
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
        if 'llava' in llm_model:
            st.warning('Llava is designed for visual assessments, you can pass a path to an image to start the conversation', icon = ":material/ophthalmology:")  
            
        with st.expander(f'Fine Tune Model {llm_model}'):
            temp = st.slider('Temperature', min_value = 0.0, max_value = 2.0, step = 0.01, value = 0.25)
            top_p = st.slider('Top_P', min_value = 0.0, max_value = 1.0, step = 0.01, value = 0.2)
            llm3 = ChatOpenAI(api_key = API_KEY, model= llm_model, base_url="http://localhost:11434/v1"
                        , streaming=True, temperature = temp, top_p = top_p)

    # Store LLM generated responses
    st.button('CLEAR CHAT', on_click = clear_chat_history, use_container_width=True)  
# Display or clear chat messages

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", 
                                  "content": "WHAT DO YOU WANT TO TALK ABOUT?"}]
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
    defprompt = None
else: 
    defprompt = prompt = 'Why are sharks cool? '
    
# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        # st.write(dataimg,datatext)
        with st.spinner("Thinking..."):
            if dataimg:
                st.success('Loading image description')
                if 'image_data' in st.session_state:
                    st.success('IMAGE_DATA_EXISTS')
                    image_data = st.session_state.image_data
                    st.write(image_data)
                    response = generate_llama3_response(prompt + image_data, llm3)
                    response = response.content
                else: 
                    st.success('NEW_IMAGE_DATA_')
                    temp_dir = tempfile.mkdtemp()
                    path = os.path.join(temp_dir, uploadedfile.name)
                    with open(path, "wb") as f:
                        f.write(uploadedfile.getvalue())
                    image_prompt= f'''Please provide a detailed description of the following image. Start with a General Description section with 5-10 points detailing the whole image. Then include additional detailed descriptions for each: Titles, Subtitles, Sections, Metrics, and Graphs/Figures. Make sure you include details about: colors, font types, values and any other features within each of the above descriptions. For Titles and subtitles, please write the title, font type, color and location. For sections, describe the contents. For metrics, provide the name of the metric, value, color, any indicator present. For graphs/figures please include a separate description for each figure, include type of graph, colors, borders, labels, and values. Please place the output in bullet points separated by: General Description, Titles, Subtitles, Metrics, Graphs. Here is the image {uploadedfile}'''
                    llava = ChatOpenAI(api_key = API_KEY, model= 'llava', base_url="http://localhost:11434/v1"
                        , streaming=True, temperature = temp, top_p = top_p)
                    image_data = generate_llama3_response(image_prompt, llava)
                    # st.write(image_data)
                    if 'image_data' not in st.session_state:
                        st.session_state.image_data = image_data.content 
                        # st.write(prompt + st.session_state.image_data )
                    response = generate_llama3_response(prompt + st.session_state.image_data , llm3)
                    response = response.content
            elif datatext: 
                # st.success('DATA')
                if 'string_data' in st.session_state:
                    # st.success('STRING_DATA_EXISTS')
                    string_data = st.session_state.string_data
                    response = get_response_with_document(string_data, prompt, llm3, embeddings_model)
                elif uploadedfile.name[-3:]=='pdf':
                    # st.success('PDF')
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
                    # st.success('TXT')
                    stringio = StringIO(uploadedfile.getvalue().decode("utf-8"))
                    string_data = stringio.read()
                response = get_response_with_document(string_data, prompt, llm3, embeddings_model)      
                if 'string_data' not in st.session_state or st.session_state.string_data == None:
                    st.session_state.string_data = string_data                           
            else:
                if prompt == defprompt: 
                    st.info('Do you know why they are cool?')
                    # st.success('GENERANDO RESPUESTA')
                response = generate_llama3_response(prompt, llm3)
                response = response.content
            
            if response !=  'No Data':
                try: 
                    response = response['result']
                except: 
                    response = response
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