from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

app = FastAPI(
    title="Langchain-based-project Server",
    version="1.0",
    description="Testing"
)

add_routes(
    app,
    ChatOpenAI(),
    path = "/openai"
)

model = ChatOpenAI()
llm = Ollama(model="llama3")
prompt1 = ChatPromptTemplate.from_template("Write essay on {topic} with 100 words")
prompt2 = ChatPromptTemplate.from_template("Write poem on {topic} with 100 words")

add_routes(
    app,
    prompt1|model,
    path = '/essay'
)
add_routes(
    app,
    prompt2|llm,
    path = '/poem'
)
if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)
