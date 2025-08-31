from dotenv import load_dotenv
# Types
from typing import Annotated, List
from typing_extensions import TypedDict
# Data validation
from pydantic import BaseModel, Field
# LangGraph
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
# LangChain
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model( "anthropic:claude-3-5-sonnet-latest" )

class State( TypedDict ):
    messages: Annotated[ list, add_messages ]
    user_question: str | None
    google_results: str | None
    bing_results: str | None
    reddit_results: str | None
    selected_reddit_urls: list[ str ] | None
    reddit_post_data: list | None
    google_analysis: str | None
    bing_analysis: str | None
    reddit_analysis: str | None
    final_answer: str | None

def google_search( state: State ):
    pass

def bing_search( state: State ):
    pass

def reddit_search( state: State ):
    pass

def analyze_reddit_posts( state: State ):
    pass

def retrieve_reddit_posts( state: State ):
    pass

def analyze_google_results( state: State ):
    pass

def analyze_bing_results( state: State ):
    pass

def analyze_reddit_results( state: State ):
    pass

def synthesize_analysis( state: State ):
    pass

graph_builder = StateGraph( State )

graph_builder.add_node( "google_search", google_search )
graph_builder.add_node( "bing_search", bing_search )
graph_builder.add_node( "reddit_search", reddit_search )
graph_builder.add_node( "analyze_reddit_posts", analyze_reddit_posts )
graph_builder.add_node( "retrieve_reddit_posts", retrieve_reddit_posts )
graph_builder.add_node( "analyze_google_results", analyze_google_results )
graph_builder.add_node( "analyze_bing_results", analyze_bing_results )
graph_builder.add_node( "analyze_reddit_results", analyze_reddit_results )
graph_builder.add_node( "synthesize_analysis", synthesize_analysis )

# On start, graph will run the google_search, bing_search, and reddit_search nodes in parallel
graph_builder.add_edge( START, "google_search" )
graph_builder.add_edge( START, "bing_search" )
graph_builder.add_edge( START, "reddit_search" )
# On successful completion of the google_search, bing_search, and reddit_search nodes, the graph will run the analyze_reddit_posts node
graph_builder.add_edge( "google_search", "analyze_reddit_posts" )
graph_builder.add_edge( "bing_search", "analyze_reddit_posts" )
graph_builder.add_edge( "reddit_search", "analyze_reddit_posts" )
# On successful completion of the analyze_reddit_posts node, the graph will run the retrieve_reddit_posts node
graph_builder.add_edge( "analyze_reddit_posts", "retrieve_reddit_posts" )
# On successful completion of the retrieve_reddit_posts node, the graph will run the analyze_google_results, analyze_bing_results, and analyze_reddit_results nodes in parallel
graph_builder.add_edge( "retrieve_reddit_posts", "analyze_google_results" )
graph_builder.add_edge( "retrieve_reddit_posts", "analyze_bing_results" )
graph_builder.add_edge( "retrieve_reddit_posts", "analyze_reddit_results" )
# On successful completion of the analyze_google_results, analyze_bing_results, and analyze_reddit_results nodes, the graph will run the synthesize_analysis node
graph_builder.add_edge( "analyze_google_results", "synthesize_analysis" )
graph_builder.add_edge( "analyze_bing_results", "synthesize_analysis" )
graph_builder.add_edge( "analyze_reddit_results", "synthesize_analysis" )
# On successful completion of the synthesize_analysis node, the graph will end
graph_builder.add_edge( "synthesize_analysis", END )

graph = graph_builder.compile()

def run_chatbot():
    print( "Starting chatbot..." )
    print( "Type 'exit' to end the chatbot" )

    # Initial state
    state = {
        "messages": [ { "role": "user", "content": user_input } ],
        "user_question": user_input,
        "google_results": None,
        "bing_results": None,
        "reddit_results": None,
        "selected_reddit_urls": None,
        "reddit_post_data": None,
        "google_analysis": None,
        "bing_analysis": None,
        "reddit_analysis": None,
        "final_answer": None,
    }

    while True:
        user_input = input( "You: " )
        if user_input.lower() == "exit":
            print( "Goodbye!" )
            break

        print( "\nStarting parallel research process..." )
        print( "Launching Google, Bing, and Reddit searches...\n" )

        final_state = graph.invoke( state )

        if final_state.get( "final_answer" ):
            print( f"\nFinal Answer:\n{ final_state.get( 'final_answer' ) }\n" )

        print( "-" * 80 )

if __name__ == "__main__":
    run_chatbot()