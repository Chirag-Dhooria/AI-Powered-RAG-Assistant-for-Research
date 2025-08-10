import os
import gradio as gr
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.extensions.langchain import WatsonxLLM
from langchain_ibm import WatsonxEmbeddings
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from ibm_watsonx_ai.foundation_models import ModelInference


def get_llm():
    model_id = 'mistralai/mistral-small-3-1-24b-instruct-2503'
    parameters = {
        GenParams.MAX_NEW_TOKENS: 256,  # this controls the maximum number of tokens in the generated output
        GenParams.TEMPERATURE: 0.5, # this randomness or creativity of the model's responses
    }
    credentials = {
        "url": "https://us-south.ml.cloud.ibm.com"
    }
    project_id = "skills-network"
    model = ModelInference(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=project_id
    )
    mixtral_llm = WatsonxLLM(model = model)
    return mixtral_llm


def document_loader(pdf_url):
    loader = PyPDFLoader(pdf_url)
    doc = loader.load()
    return doc

def text_splitter(data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
    )
    text = text_splitter.split_documents(data)
    return text

def watsonx_embedding():
    embed_params = {
        EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
        EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
    }

    watsonx_embedding = WatsonxEmbeddings(
        model_id="ibm/slate-125m-english-rtrvr",
        url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
        params=embed_params,
    )
    return watsonx_embedding


def vector_database(chunks):
    embedding_model = watsonx_embedding()
    vectordb = Chroma.from_documents(chunks , embedding_model)
    return vectordb 

def retriever(file):
    splits = document_loader(file)
    chunks = text_splitter(splits)
    vector_db = vector_database(chunks)
    retriever = vector_db.as_retriever()
    return retriever

def retriever_qa(file,query):
    llm = get_llm()
    retriever_obj = retriever(file)
    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type="stuff",
        retriever = retriever_obj,
        return_source_documents = False
    )
    response = qa.invoke(query)
    return response['result']

rag_application = gr.Interface(
    fn = retriever_qa,
    allow_flagging = 'never',
    inputs = [
        gr.File(label="Upload PDF File", file_count="single", file_types=['.pdf'], type="filepath"), 
        gr.Textbox(label="Input Query", lines=2, placeholder="Type your question here...")
    ],
    outputs=gr.Textbox(label="Answer", interactive=False, lines=15),
    title="Quest Analytics: AI RAG Assistant ",
    description="Upload a PDF document and ask any question. The chatbot will try to answer using the provided document."
)

rag_application.launch(server_name="127.0.0.1", server_port= 7860)
