# Import streamlit for app dev
import streamlit as st
import os
# Import transformer classes for generation
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
# Import torch for datatype attributes
import torch
# Import the prompt wrapper...but for llama index
from llama_index.prompts.prompts import SimpleInputPrompt
# Import the llama index HF Wrapper
from llama_index.llms import HuggingFaceLLM
# Bring in embeddings wrapper
from llama_index.embeddings import LangchainEmbedding
# Bring in HF embeddings - need these to represent document chunks
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
# Bring in stuff to change service context
from llama_index import set_global_service_context
from llama_index import ServiceContext
# Import deps to load documents
from llama_index import VectorStoreIndex, download_loader
from pathlib import Path
import key
# streamlit run C:\Users\JulienG\Documents\code\ChatBot_Schizo\back\llama_test.py

# Define variable to hold llama2 weights naming
name = "meta-llama/Llama-2-7b-chat-hf"
# Set auth token variable from hugging face
auth_token = key.auth_token


# Check if a GPU is available
if torch.cuda.is_available():
    # Set the current device to the GPU
    torch.cuda.empty_cache()
    torch.cuda.set_device(0)

@st.cache_resource
def get_tokenizer_model():
    # Create tokenizer
    tokenizer = AutoTokenizer.from_pretrained(name, cache_dir='./model/', use_auth_token=auth_token)
    # Create model
    model = AutoModelForCausalLM.from_pretrained(name, cache_dir='./model/'
                                                 , use_auth_token=auth_token, torch_dtype=torch.bfloat16,
                                                 rope_scaling={"type": "dynamic", "factor": 2})
    return tokenizer, model


tokenizer, model = get_tokenizer_model()


# Create a system prompt
system_prompt = """<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. 
<</SYS>>
"""
# Throw together the query wrapper
query_wrapper_prompt = SimpleInputPrompt("{query_str} [/INST]")


llm = HuggingFaceLLM(context_window=4096,
                    max_new_tokens=256,
                    system_prompt=system_prompt,
                    query_wrapper_prompt=query_wrapper_prompt,
                    model=model,
                    tokenizer=tokenizer,
                    model_kwargs={"torch_dtype": torch.float16})


# Create and dl embeddings instance
embeddings = LangchainEmbedding(
    HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
)

# Create new service context instance
service_context = ServiceContext.from_defaults(
    chunk_size=512,
    llm=llm,
    embed_model=embeddings,

)
# And set the service context
set_global_service_context(service_context)

# Download PDF Loader
PyMuPDFReader = download_loader("PyMuPDFReader")
# Create PDF Loader
loader = PyMuPDFReader()
# Load documents
documents = loader.load(file_path=str(Path(
    'C:/Users/JulienG/Documents/code/ChatBot_Schizo/back/cognitive_neuropsycho_schizo.pdf')), metadata=True)

# Create an index - we'll be able to query this in a sec
index = VectorStoreIndex.from_documents(documents)
# Setup index query engine using LLM
query_engine = index.as_query_engine()
torch.cuda.empty_cache()


# Create a text input box for the user
prompt = st.text_input('Input your prompt here')
# Create centered main title
st.title('Llama')
# If the user hits enter
if prompt:
    response = query_engine.query(prompt)
    # ...and write it out to the screen
    st.write(response)

    # Display raw response object
    with st.expander('Response Object'):
        st.write(response)
    # Display source text
    with st.expander('Source Text'):
        st.write(response.get_formatted_sources())
