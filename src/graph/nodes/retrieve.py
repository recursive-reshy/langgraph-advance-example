# Schemas
from ..schemas import State
# Operations
from ...operations.web_operations import reddit_post_retrieval

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