# .env 읽기
from dotenv import load_dotenv
load_dotenv()

# OpenAI Chat
from langchain_openai import ChatOpenAI
# Prompt Building
from langchain_core.prompts import ChatPromptTemplate
# output
from langchain_core.output_parsers import StrOutputParser 
# Front end for streamlit
import streamlit as st

llm = ChatOpenAI()

st.title('My Co-pilot for my work')

role_definition = st.text_input("Co-pilot의 역할을 적어주세요")
st.caption("예) 정책 수립자의 입장에서 질문을 영어로 번역하여 영어로 응답하고 이를 한글로 번역해주세요")

prompt = ChatPromptTemplate.from_messages([
    ("system", role_definition),
    ("user", "{input}")
])
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

question = st.text_area("질문할 내용을 적어주세요")

if st.button("응답요청") :
    with st.spinner("응답 생성 중..."):
        result = chain.invoke({"input" : question})
        st.write( result )

