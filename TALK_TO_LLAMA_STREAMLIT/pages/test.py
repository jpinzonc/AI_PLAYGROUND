import streamlit as st
from time import sleep

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 1

uploaded_file = st.file_uploader(
    "Please upload an image",
    type=["pdf", "jpeg", "png"],
    key=st.session_state["uploader_key"],
)

st.write(uploaded_file)

# if uploaded_file is None:
#     with st.spinner("Processing"):
#         sleep(3)

#     # Clear the file uploader
#     st.session_state["uploader_key"] += 1
#     st.rerun()