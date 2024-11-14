import os  
from openai import AzureOpenAI
import streamlit as st

def get_openai_response(prompt):
    try:
    #     client = AzureOpenAI(
    #     api_version = "2024-02-01",
    #     azure_endpoint = "https://dataset-creation-revai.openai.azure.com/",  
    #     api_key = 'AlCltfQ4Mw9Wc0ctEMhaYJX9Ts32DYJaBGDJHnnqyfSBqRwfZXJQJQQJ99AKACYeBjFXJ3w3AAABACOGfMhG',

    #     )
    #     response = client.completions.create(model ="gpt-35-turbo", prompt=prompt )
    #     return response.choices[0].text.strip()
        endpoint = os.getenv("ENDPOINT_URL", "https://genai-openai-revolution-ai-ries.openai.azure.com/")  
        deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")  
        search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://genairevolutionaries.search.windows.net")  
        search_key = os.getenv("SEARCH_KEY", "ZZeqTXekHfHQOGD8FutWpuvVQWkxEk3lTCTpAksyY5AzSeBFxiF1")  
        search_index = os.getenv("SEARCH_INDEX_NAME", "indexgenairev")  
        subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "8e4c0453b77a464b930ebc8ac986788c")
        
        # Initialize Azure OpenAI client with key-based authentication
        client = AzureOpenAI(  
            azure_endpoint=endpoint,  
            api_key=subscription_key,  
            api_version="2024-05-01-preview",  
        ) 
        
        # Prepare the chat prompt  
        chat_prompt = [
        {
            "role": "system",
            "content": "You are a helpful assistant answering questions"
        },
        {
            "role": "user",
            "content": prompt
        }
        ]
        
        # Generate the completion  
        completion = client.chat.completions.create(  
            model=deployment,  
            messages=chat_prompt,  
            # past_messages=10,  
            max_tokens=800,  
            temperature=0.7,  
            top_p=0.95,  
            frequency_penalty=0,  
            presence_penalty=0,  
            stop=None,  
            stream=False  
        ),
        extra_body={
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                "endpoint": f"{search_endpoint}",
                "index_name": "indexgenairev",
                "semantic_configuration": "default",
                "query_type": "semantic",
                "fields_mapping": {},
                "in_scope": True,
                "role_information": "You are a helpful assistant answering questions",
                "filter": None,
                "strictness": 2,
                "top_n_documents": 9,
                "authentication": {
                    "type": "api_key",
                    "key": f"{search_key}"
                }
            }
            }]
        }   
        print(completion) 
        return completion[0].choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
    
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Title of the app
st.title("Ask the Revolution-AI-ries")
st.write("Hello! I am an Gen AI-powered chatbot. Type your message below, and I will respond.")

user_input = st.text_input("How can I help?", "")

# Create a button to trigger the chatbot response
a = st.button("Send")
if a and user_input:
    # st.write(f"User prompt: {user_input}")
    bot_response = get_openai_response(user_input)
    if "python" in user_input.lower():
        bot_response +="\n\n References: Python_Doc_1.pdf"

    st.write(f"🤖: {bot_response}")
elif a and not user_input:
    st.write("Please enter a message to send.")
