# Chat Model
# Prompt Template
# Memory
# Retriever

import dotenv 
dotenv.load_dotenv()

# ChatModel
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

chat = ChatOpenAI()
# chat(
#     [
#         HumanMessage(
#             content="What is the purpose of model regularization?"
#         )
#     ]

# )

messages = [
    SystemMessage(
        content="AI 분야의 전문가로서 글을 작성합니다."
    ),
    HumanMessage(content="모델 정규화의 목적은 무엇입니까?"),
]
# chat(messages)

# buffer : history memory
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("hi!")
memory.chat_memory.add_ai_message("whats up?")
print( memory.load_memory_variables({}) )


# We can also keep a sliding window of the most recent k interactions using : ConversationBufferWindowMemory.
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=2)
memory.save_context({"input": "hi"}, {"output": "whats up"})
memory.save_context({"input": "not much you"}, {"output": "not much"})
print( memory.load_memory_variables({}) )