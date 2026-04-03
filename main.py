import streamlit as st
import os
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

st.set_page_config(page_title="K8s Claude-4 Expert", layout="wide")

api_key = os.getenv("ANTHROPIC_API_KEY")
model_name = os.getenv("CLAUDE_MODEL_NAME", "claude-sonnet-4-20250514")

if not api_key:
    st.error(".env dosyasında ANTHROPIC_API_KEY bulunamadı!")
    st.stop()

with st.sidebar:
    st.header("⚙️ RAG Yapılandırması")
    url = st.text_input("K8s Doküman URL'i:", placeholder="https://kubernetes.io/docs/...")
    process_btn = st.button("Kaynağı Analiz Et")
    st.info(f"Kullanılan Model: {model_name}")

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if process_btn and url:
    with st.spinner("Claude-4 için içerik hazırlanıyor..."):
        loader = WebBaseLoader(url)
        data = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=150)
        docs = text_splitter.split_documents(data)
        
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        st.session_state.vector_db = Chroma.from_documents(docs, embeddings)
        st.success("Doküman vektör veritabanına eklendi!")

st.title("☸️ Kubernetes Learning Assistant")
st.caption("Claude Sonnet-4 ile dinamik dökümantasyon analizi")

if st.session_state.vector_db:
    user_query = st.chat_input("Sorunuzu buraya yazın...")
    
    if user_query:
        with st.chat_message("user"):
            st.markdown(user_query)
        
        with st.chat_message("assistant"):
            llm = ChatAnthropic(model=model_name, api_key=api_key, temperature=0)
            retriever = st.session_state.vector_db.as_retriever(search_kwargs={"k": 4})
        
            prompt = ChatPromptTemplate.from_template("""
            Sen bir Kubernetes uzmanısın. Sadece aşağıdaki döküman içeriğini kullanarak soruyu cevapla. 
            Eğer cevap dökümanda yoksa, dökümanda olmadığını belirt.

            Döküman İçeriği:
            {context}

            Kullanıcı Sorusu: {question}
            """)

            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

            with st.spinner("Claude dökümanı analiz ediyor..."):
                response = rag_chain.invoke(user_query)
                st.markdown(response)
   
else:
    st.warning("Lütfen sol tarafa bir Kubernetes dokümantasyon URL'i girerek başlayın.")