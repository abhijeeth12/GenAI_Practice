from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

prompt  = ChatPromptTemplate(
    [
        ("system","You are a helpful chatbot, please answer queries"),
        ("user","Question:{question}")
    ]
)

st.title('LangChain Ollama Model')
input_text = st.text_input("Enter Your Query: ")

output_parser = StrOutputParser();
#Ollama LLAMA2 LLM
llm = Ollama(model="llama3")
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))