#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('nvidia-smi')


# In[2]:


get_ipython().system('pip install -Uqqq pip --progress-bar off')
get_ipython().system('pip install -qqq torch==2.0.1 --progress-bar off')
get_ipython().system('pip install -qqq transformers==4.31.0 --progress-bar off')
get_ipython().system('pip install -qqq langchain==0.0.266 --progress-bar off')
get_ipython().system('pip install -qqq chromadb==0.4.5 --progress-bar off')
get_ipython().system('pip install -qqq pypdf==3.15.0 --progress-bar off')
get_ipython().system('pip install -qqq xformers==0.0.20 --progress-bar off')
get_ipython().system('pip install -qqq sentence_transformers==2.2.2 --progress-bar off')
get_ipython().system('pip install -qqq InstructorEmbedding==1.0.1 --progress-bar off')
get_ipython().system('pip install -qqq pdf2image==1.16.3 --progress-bar off')


# In[3]:


get_ipython().system('wget -q https://github.com/PanQiWei/AutoGPTQ/releases/download/v0.4.1/auto_gptq-0.4.1+cu118-cp310-cp310-linux_x86_64.whl')


# In[4]:


get_ipython().system('pip install -qqq auto_gptq-0.4.1+cu118-cp310-cp310-linux_x86_64.whl --progress-bar off')


# In[5]:


get_ipython().system('sudo apt-get install poppler-utils')


# In[6]:


import torch
from auto_gptq import AutoGPTQForCausalLM
from langchain import HuggingFacePipeline, PromptTemplate
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from pdf2image import convert_from_path
from transformers import AutoTokenizer, TextStreamer, pipeline

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"


# ## Data

# In[7]:


get_ipython().system('mkdir pdfs')


# In[8]:


get_ipython().system('gdown 1v-Rn1FVU1pLTAQEgm0N9oB6cExMoebZr -O pdfs/tesla-earnings-report.pdf')
get_ipython().system('gdown 1Xc890jrQvCExAkryVWAttsv1DBLdVefN -O pdfs/nvidia-earnings-report.pdf')
get_ipython().system('gdown 1Epz-SQ3idPpoz75GlTzzomag8gplzLv8 -O pdfs/meta-earnings-report.pdf')


# In[9]:


meta_images = convert_from_path("pdfs/meta-earnings-report.pdf", dpi=88)
meta_images[0]


# In[10]:


nvidia_images = convert_from_path("pdfs/nvidia-earnings-report.pdf", dpi=88)
nvidia_images[0]


# In[11]:


tesla_images = convert_from_path("pdfs/tesla-earnings-report.pdf", dpi=88)
tesla_images[0]


# In[12]:


get_ipython().system('rm -rf "db"')


# In[13]:


loader = PyPDFDirectoryLoader("pdfs")
docs = loader.load()
len(docs)


# In[14]:


embeddings = HuggingFaceInstructEmbeddings(
    model_name="hkunlp/instructor-large", model_kwargs={"device": DEVICE}
)


# In[15]:


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
texts = text_splitter.split_documents(docs)
len(texts)


# In[16]:


get_ipython().run_cell_magic('time', '', 'db = Chroma.from_documents(texts, embeddings, persist_directory="db")\n')


# ## Llama 2 13B

# In[17]:


model_name_or_path = "TheBloke/Llama-2-13B-chat-GPTQ"
model_basename = "model"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

model = AutoGPTQForCausalLM.from_quantized(
    model_name_or_path,
    revision="gptq-4bit-128g-actorder_True",
    model_basename=model_basename,
    use_safetensors=True,
    trust_remote_code=True,
    inject_fused_attention=False,
    device=DEVICE,
    quantize_config=None,
)


# In[18]:


get_ipython().system('nvidia-smi')


# In[19]:


DEFAULT_SYSTEM_PROMPT = """
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering 
something not correct. If you don't know the answer to a question, please don't share false information.
""".strip()


def generate_prompt(prompt: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    return f"""
[INST] <<SYS>>
{system_prompt}
<</SYS>>

{prompt} [/INST]
""".strip()


# In[20]:


streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)


# In[21]:


text_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=1024,
    temperature=0,
    top_p=0.95,
    repetition_penalty=1.15,
    streamer=streamer,
)


# In[22]:


llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})


# In[23]:


SYSTEM_PROMPT = "Use the following pieces of context to answer the question at the end." \
                " If you don't know the answer, just say that you don't know, don't try to make up an answer."

template = generate_prompt(
    """
{context}

Question: {question}
""",
    system_prompt=SYSTEM_PROMPT,
)


# In[24]:


prompt = PromptTemplate(template=template, input_variables=["context", "question"])


# In[25]:


qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt},
)


# ## Chat with Multiple PDFs

# In[26]:


result = qa_chain("What is the per share revenue for Meta during 2023?")


# In[27]:


len(result["source_documents"])


# In[28]:


print(result["source_documents"][0].page_content)


# In[29]:


result = qa_chain("What is the per share revenue for Tesla during 2023?")


# In[30]:


result = qa_chain("What is the per share revenue for Nvidia during 2023?")


# In[31]:


print(result["source_documents"][1].page_content)


# In[32]:


result = qa_chain("What is the estimated YOY revenue for Meta during 2023?")


# In[33]:


result = qa_chain("What is the estimated YOY revenue for Tesla during 2023?")


# In[34]:


result = qa_chain("What is the estimated YOY revenue for Nvidia during 2023?")


# In[35]:


result = qa_chain(
    "Which company is more profitable during 2023 Meta, Nvidia or Tesla and why?"
)


# In[36]:


result = qa_chain(
    "Choose one company to invest (Tesla, Nvidia or Meta) to maximize your profits for the long term (10+ years)?"
)


# ## References
# 
# - [Tesla Quarterly Report (Jul 21, 2023)](https://ir.tesla.com/_flysystem/s3/sec/000095017023033872/tsla-20230630-gen.pdf)
# - [Meta Q2 2023 Earnings (Jul 26, 2023)](https://s21.q4cdn.com/399680738/files/doc_financials/2023/q2/Meta-06-30-2023-Exhibit-99-1-FINAL.pdf)
# - [Nvidia Fiscal Q1 2024](https://s201.q4cdn.com/141608511/files/doc_financials/2024/q1/ecefb2b2-efcb-45f3-b72b-212d90fcd873.pdf)
