# Schemas
from ..schemas import State, RedditUrlAnalysis
# Prompts
from ...prompts.templates import get_google_analysis_messages, get_bing_analysis_messages, get_reddit_analysis_messages
from ...prompts.templates import get_reddit_url_analysis_messages
# LangChain
from ...llm.client import get_llm

llm = get_llm()

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

def analyze_reddit_results( state: State ):
    print( "Analyzing Reddit results" )
    user_question = state.get( "user_question", "" )
    reddit_results = state.get( "reddit_results", "" )
    reddit_post_data = state.get( "reddit_post_data", "" )

    messages = get_reddit_analysis_messages( user_question, reddit_results, reddit_post_data )
    reply = llm.invoke( messages )

    print( f"Reddit analysis: { reply }" )
    
    return { "reddit_analysis": reply.content }