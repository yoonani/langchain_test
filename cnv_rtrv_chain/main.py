from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
# prompt
from langchain_core.prompts import ChatPromptTemplate 
# output
from langchain_core.output_parsers import StrOutputParser

# WebBasedLoader
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")

docs = loader.load()

# create chain
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

# retriever
from langchain.chains import create_retrieval_chain

retriever = vector.as_retriever()


# conversation retrieval chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

llm = ChatOpenAI()

# First we need a prompt that we can pass into an LLM to generate this search query
# recent input : input
# conversation history : chat_history
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])

# create_history_aware_retriever
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

# test
from langchain_core.messages import HumanMessage, AIMessage

chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
retriever_chain.invoke({
    "chat_history": chat_history,
    "input": "Tell me how"
})


from langchain.chains.combine_documents import create_stuff_documents_chain

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")
document_chain = create_stuff_documents_chain(llm, prompt)


retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
print(
    retrieval_chain.invoke({
        "chat_history": chat_history,
        "input": "Tell me how"
    })
)


output_parser = StrOutputParser()
#llm.invoke("how can langsmith help with testing?")

chain = prompt | llm | output_parser


