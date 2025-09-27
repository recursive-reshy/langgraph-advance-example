from dotenv import load_dotenv
# Chatbot
from chatbot import run_chatbot
# Graph Builder
from src.graph.graph_builder import create_graph

load_dotenv()

graph = create_graph()

if __name__ == "__main__":
    run_chatbot( graph )