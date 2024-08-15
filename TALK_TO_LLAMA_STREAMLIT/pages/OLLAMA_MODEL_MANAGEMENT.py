# https://www.youtube.com/watch?v=bAI_jWsLhFM
# https://github.com/tonykipkemboi/ollama_streamlit_demos/blob/main/pages/02_%F0%9F%8C%8B_Multimodal.py
import streamlit as st
import ollama, os
from time import sleep
# from utilities.icon import page_icon

st.set_page_config(
    page_title="Model management",
    # page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    # page_icon("⚙️")
    st.subheader("Model Management for Ollama", divider="red", anchor=False)

    st.subheader("Download Models", anchor=False)
    model_name = st.text_input(
        "Enter the name of the model to download ↓", placeholder="mistral"
    )
    if st.button(f"📥 :green[**Download**] :red[{model_name}]"):
        if model_name:
            try:
                ollama.pull(model_name)
                st.success(f"Downloaded model: {model_name}", icon="🎉")
                st.balloons()
                sleep(1)
                st.rerun()
            except Exception as e:
                st.error(
                    f"""Failed to download model: {
                    model_name}. Error: {str(e)}""",
                    icon="😳",
                )
        else:
            st.warning("Please enter a model name.", icon="⚠️")

    st.divider()

    st.subheader("Create model", anchor=False)
    modelfile = st.text_area(
        "Enter the modelfile",
        height=100,
        placeholder="""FROM mistral
SYSTEM You are mario from super mario bros.""",
    )
    model_name = st.text_input(
        "Enter the name of the model to create", placeholder="mario"
    )
    if st.button(f"🆕 Create Model {model_name}"):
        if model_name and modelfile:
            try:
                ollama.create(model=model_name, modelfile=modelfile)
                st.success(f"Created model: {model_name}", icon="✅")
                st.balloons()
                sleep(1)
                st.rerun()
            except Exception as e:
                st.error(
                    f"""Failed to create model: {
                         model_name}. Error: {str(e)}""",
                    icon="😳",
                )
        else:
            st.warning("Please enter a **model name** and **modelfile**", icon="⚠️")

    st.divider()

    st.subheader("Delete Models", anchor=False)

    ollama_models = os.getenv('ollama_models')
    
    if ollama_models:
        selected_models = st.multiselect("Select models to delete", ollama_models.split(','))
        if st.button("🗑️ :red[**Delete Selected Model(s)**]"):
            for model in selected_models:
                try:
                    ollama.delete(model)
                    st.success(f"Deleted model: {model}", icon="🎉")
                    st.balloons()
                    sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(
                        f"""Failed to delete model: {
                        model}. Error: {str(e)}""",
                        icon="😳",
                    )
    else:
        st.info("No models available for deletion.", icon="🦗")


if __name__ == "__main__":
    main()