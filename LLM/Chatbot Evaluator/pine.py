import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os
import fitz

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")

if not google_api_key or not pinecone_api_key or not pinecone_env:
    st.error("One or more environment variables are missing.")
    st.stop()
pc = Pinecone(api_key=pinecone_api_key, environment=pinecone_env)

def get_pdf_text(pdf_bytes):
    text = ""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def get_text_chunks(full_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(full_text)
    return chunks

def get_vector_store(text_chunks, domain):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", api_key=google_api_key)
    vectors = []
    metadata = []

    # Compute vectors for each chunk
    for chunk in text_chunks:
        try:
            vector = embeddings.embed_query(chunk)
            vectors.append(vector)
            metadata.append({'text': chunk})
        except Exception as e:
            st.error(f"Error embedding text chunk: {e}")
            continue

    index_name = f"{domain}-pdf-vector"
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=len(vectors[0]),  # Ensure dimension matches vector size
            spec=ServerlessSpec(cloud='aws', region='us-east-1')  
        )
    
    index = pc.Index(index_name)
    prev_id=index.describe_index_stats()['total_vector_count']
    if prev_id==0:
        ids = [str(i) for i in range(len(vectors))]
    else:
        ids = [str(prev_id + 1 + i) for i in range(len(vectors))]
    
    index.upsert(vectors=zip(ids, vectors, metadata))


st.set_page_config(page_title="Upload PDF Documents")
st.header("Upload PDF Documents")

domain = st.selectbox("Select Domain", ["flight", "banks", "restaurants"])
pdf_docs = st.file_uploader("Upload your PDF files", type="pdf", accept_multiple_files=True)

if pdf_docs and domain:
    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            for pdf in pdf_docs:
                pdf_bytes = pdf.read()
                raw_text = get_pdf_text(pdf_bytes)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks, domain)
                st.success(f"Uploaded and processed {pdf.name} successfully!")