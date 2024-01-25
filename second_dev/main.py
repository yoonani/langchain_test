from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
# prompt
from langchain_core.prompts import ChatPromptTemplate 
# output
from langchain_core.output_parsers import StrOutputParser

# WebBaseLoader를 위해 bs4 필요
from langchain_community.document_loaders import WebBaseLoader 
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")

docs = loader.load()
