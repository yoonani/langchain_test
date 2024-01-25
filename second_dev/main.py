from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
# prompt
from langchain_core.prompts import ChatPromptTemplate 
# output
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
        ("system", "You are world class technical documentation writer."),
        ("user", "{input}")
    ])
llm = ChatOpenAI()
output_parser = StrOutputParser()
#llm.invoke("how can langsmith help with testing?")

chain = prompt | llm | output_parser



# WebBaseLoader를 위해 bs4 필요
from langchain_community.document_loaders import WebBaseLoader 
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")

docs = loader.load()

# vectorstore 

# environment variable set
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# 문서를 vectorstore에 포함(삼키기, ingest)하기 위해 FAISS 사용
from langchain_community.vectorstores import FAISS 
from langchain.text_splitter import RecursiveCharacterTextSplitter 

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)


# prompt 만들기
from langchain.chains.combine_documents import create_stuff_documents_chain

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

# 실행 및 context 파악
from langchain_core.documents import Document

document_chain.invoke({
    "input": "how can langsmith help with testing?",
    "context": [Document(page_content="langsmith can let you visualize test results")]
})

# retrieval chain
from langchain.chains import create_retrieval_chain

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# invoke chain
response = retrieval_chain.invoke({"input": "how can langsmith help with testing?"})
print(response["answer"])

# LangSmith offers several features that can help with testing:...
