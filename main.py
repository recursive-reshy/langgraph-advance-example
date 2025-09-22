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
# Web Operations
from web_operations import serp_search, reddit_post_retrieval
from web_operations import reddit_search_api
# Prompts
from prompts import (
    get_reddit_url_analysis_messages, 
    get_google_analysis_messages, 
    get_bing_analysis_messages, 
    get_reddit_analysis_messages, 
    get_synthesis_messages
)

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

class RedditUrlAnalysis( BaseModel ):
    selected_urls: list[ str ] = Field( description = "The URLs of the Reddit posts that are most relevant to the user's question" )

def google_search( state: State ):
    user_question = state.get( "user_question", "" )
    print( f"Google searching for: { user_question }" )

    google_results = serp_search( user_question )

    return { "google_results": google_results }

def bing_search( state: State ):
    user_question = state.get( "user_question", "" )
    print( f"Bing searching for: { user_question }" )

    bing_results = serp_search( user_question, engine = "bing" )

    return { "bing_results": bing_results }

def reddit_search( state: State ):
    user_question = state.get( "user_question", "" )
    print( f"Reddit searching for: { user_question }" )

    reddit_results = reddit_search_api( user_question )

    return { "reddit_results": reddit_results }

def analyze_reddit_posts( state: State ):
    user_question = state.get( "user_question", "" )
    reddit_results = state.get( "reddit_results", "" )

    if not reddit_results:
        return { "selected_reddit_urls": [] }

    structured_llm = llm.with_structured_output( RedditUrlAnalysis )
    messages = get_reddit_url_analysis_messages( user_question, reddit_results )

    print( "Analyzing Reddit posts" )

    try:
        analysis = structured_llm.invoke( messages )
        selected_urls = analysis.selected_urls

        print( "Selected URLS" )

        for i, url in enumerate( selected_urls, 1 ):
            print( f"{ i }. { url }" )
        
    except Exception as e:
        print( f"Error analyzing Reddit posts: { e }" )
        selected_urls = []

    return { "selected_reddit_urls": [] }

def retrieve_reddit_posts( state: State ):
    selected_urls = state.get( "selected_reddit_urls", [] )

    if not selected_urls:
        return { "reddit_post_data": [] }

    print( f"Processing { len( selected_urls ) } Reddit posts" )
    reddit_post_data = reddit_post_retrieval( selected_urls )

    if reddit_post_data:
        print( f"Successfully got { len( reddit_post_data ) } posts" )
    else:
        print( "No Reddit posts found" )
        reddit_post_data = []

    return { "reddit_post_data": reddit_post_data }

def analyze_google_results( state: State ):
    print( "Analyzing Google results" )
    user_question = state.get( "user_question", "" )
    google_results = state.get( "google_results", "" )

    messages = get_google_analysis_messages( user_question, google_results )
    reply = llm.invoke( messages )

    print( f"Google analysis: { reply }" )

    return { "google_analysis": reply.content }

def analyze_bing_results( state: State ):
    print( "Analyzing Bing results" )
    user_question = state.get( "user_question", "" )
    bing_results = state.get( "bing_results", "" )

    messages = get_bing_analysis_messages( user_question, bing_results )
    reply = llm.invoke( messages )

    print( f"Bing analysis: { reply }" )
    
    return { "bing_analysis": reply.content }

def analyze_reddit_results( state: State ):
    print( "Analyzing Reddit results" )
    user_question = state.get( "user_question", "" )
    reddit_results = state.get( "reddit_results", "" )
    reddit_post_data = state.get( "reddit_post_data", "" )

    messages = get_reddit_analysis_messages( user_question, reddit_results, reddit_post_data )
    reply = llm.invoke( messages )

    print( f"Reddit analysis: { reply }" )
    
    return { "reddit_analysis": reply.content }

def synthesize_analysis( state: State ):
    print( "Synthesizing analysis" )
    user_question = state.get( "user_question", "" )
    google_analysis = state.get( "google_analysis", "" )
    bing_analysis = state.get( "bing_analysis", "" )
    reddit_analysis = state.get( "reddit_analysis", "" )

    messages = get_synthesis_messages( user_question, google_analysis, bing_analysis, reddit_analysis )
    reply = llm.invoke( messages )

    return { "final_answer": reply.content, "messages": [ { "role": "assistant", "content": reply.content } ] }

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

    while True:
        user_input = input( "You: " )
        if user_input.lower() == "exit":
            print( "Goodbye!" )
            break

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

        print( "\nStarting parallel research process..." )
        print( "Launching Google, Bing, and Reddit searches...\n" )

        final_state = graph.invoke( state )

        if final_state.get( "final_answer" ):
            print( f"\nFinal Answer:\n{ final_state.get( 'final_answer' ) }\n" )

        print( "-" * 80 )

if __name__ == "__main__":
    run_chatbot()