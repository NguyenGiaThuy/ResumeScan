from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate


def get_model(model_id: str, region: str, model_kwargs: dict):
    return ChatBedrock(
        model_id=model_id,
        region=region,
        model_kwargs=model_kwargs,
    )


def process_pdfs_and_create_vectorstore(data_dir, bedrock_config):
    loader = DirectoryLoader(data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    if not docs:
        return None, None, None
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)
    embeddings = BedrockEmbeddings(**bedrock_config)
    vector_store = FAISS.from_documents(split_docs, embeddings)
    return docs, split_docs, vector_store


def create_prompt(messages: list):
    return ChatPromptTemplate.from_messages(messages)
