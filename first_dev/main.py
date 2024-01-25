# 환경변수 불러오기 : git 으로 관리하기 위해 환경변수 감추기를 위해 dotenv 사용
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
# prompt
from langchain_core.prompts import ChatPromptTemplate 
# output
from langchain_core.output_parsers import StrOutputParser

# Deploy using streamlit
import streamlit as st

output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
        ("system", "You are world class technical documentation writer."),
        ("user", "{input}")
    ])
llm = ChatOpenAI()
#llm.invoke("how can langsmith help with testing?")

chain = prompt | llm | output_parser

st.title('My GPT')

question = st.text_area("질문할 내용을 적어주세요")

if st.button("응답요청") :
    with st.spinner("응답 생성 중..."):
        result = chain.invoke({"input" : question})
        st.write( result )
