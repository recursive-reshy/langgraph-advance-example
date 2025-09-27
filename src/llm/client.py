# LangChain
from langchain.chat_models import init_chat_model

llm = init_chat_model( "anthropic:claude-3-5-sonnet-latest" )

def get_llm():
    return llm