#%% 
#https://blog.devgenius.io/chatgpt-how-to-use-it-with-python-5d729ac34c0d
#https://github.com/openai/openai-python
# !pip install openai

#%% 
from secret.secret_info import openai_key

# %%
import openai 
# %%
openai.api_key =  openai_key
def chat_GPT(msg):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": msg},
            ]
            )
    result = ''
    for choice in response.choices:
        result += choice.message.content
    return result

def chat_GPt_complet(prompt):
    # Set up the model and prompt
    model_engine = "text-davinci-003"
    # Generate a response
    completion = openai.Completion.create(
                                engine=model_engine,
                                prompt=prompt,
                                max_tokens=1024,
                                n=1,
                                stop=None,
                                temperature=0.5,
                                )
    response = completion.choices[0].text
    return response

# %%
msg = "write 5 hihglights for Ally Auto bank"
print(chat_GPT(msg))
# %%
chat_GPt_complet(msg)
# %%
models = openai.Model.list()
models
# %%
# WITH RESPOMSES:
# https://medium.com/geekculture/a-simple-guide-to-chatgpt-api-with-python-c147985ae28
import openai
openai.api_key = openai_key
# %%
counter = 0
while True:
    content = input('User')

    messages = [{"role": "user", "content": content}]
    if counter >0 :
        messages.append({"role" : "user", "content" : content})
    try:
        messages.append({"role" : "assistant", "content" : chat_response})
    except: 
        messages = messages
    completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
                                                messages = messages,
                                                temperature = 0,
                                             )
    chat_response = completion.choices[0].message.content
    print(f'USER {content}')
    print(f'ChatGPT: {chat_response}')
    counter +=1
# %%
######## Use own data on CHAT GPT
# https://beebom.com/how-train-ai-chatbot-custom-knowledge-base-chatgpt-api/
## !pip install gradio
#20230327 - FIND OUT THE API KEY is FOR 5 dollars and expires in July 2023
# %%
import gradio
# %%
list(range(10, 1, -1))
# %%
s = 'a;b;c;'
# %%
s.split(';')
# %%
l = [1,2,3,4]

# %%
l.remove(2)
# %%
l
# %%
5!=6
# %%
l
# %%
l[-2]
# %%
