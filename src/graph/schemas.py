# Types
from typing import Annotated
from typing_extensions import TypedDict
# Data validation
from pydantic import BaseModel, Field
# LangGraph
from langgraph.graph.message import add_messages

class State( TypedDict ):
    messages: Annotated[ list, add_messages ]
    user_question: str | None
    google_results: str | None
    bing_results: str | None
    # reddit_results: str | None
    # selected_reddit_urls: list[ str ] | None
    # reddit_post_data: list | None
    google_analysis: str | None
    bing_analysis: str | None
    # reddit_analysis: str | None
    final_answer: str | None

class RedditUrlAnalysis( BaseModel ):
    selected_urls: list[ str ] = Field( description = "The URLs of the Reddit posts that are most relevant to the user's question" )

# __all__ = [ "State", "RedditUrlAnalysis" ]