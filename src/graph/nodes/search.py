# Schemas
from ..schemas import State
# Operations
from ...operations.web_operations import serp_search
from ...operations.web_operations import reddit_search_api

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