# Schemas
from ..schemas import State
# Prompts
from ...prompts.templates import get_synthesis_messages
# LangChain
from ...llm.client import get_llm

llm = get_llm()

def synthesize_analysis( state: State ):
    print( "Synthesizing analysis" )
    user_question = state.get( "user_question", "" )
    google_analysis = state.get( "google_analysis", "" )
    bing_analysis = state.get( "bing_analysis", "" )
    # reddit_analysis = state.get( "reddit_analysis", "" )

    messages = get_synthesis_messages( user_question, google_analysis, bing_analysis, None )
    reply = llm.invoke( messages )

    return { "final_answer": reply.content, "messages": [ { "role": "assistant", "content": reply.content } ] }