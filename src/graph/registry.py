# Nodes
from .nodes.search import google_search, bing_search, reddit_search
from .nodes.retrieve import retrieve_reddit_posts
from .nodes.analysis import analyze_google_results, analyze_bing_results, analyze_reddit_posts, analyze_reddit_results
from .nodes.synthesize import synthesize_analysis

def register_nodes( graph_builder ):
    graph_builder.add_node( "google_search", google_search )
    graph_builder.add_node( "bing_search", bing_search )
    graph_builder.add_node( "reddit_search", reddit_search )
    graph_builder.add_node( "analyze_reddit_posts", analyze_reddit_posts )
    graph_builder.add_node( "retrieve_reddit_posts", retrieve_reddit_posts )
    graph_builder.add_node( "analyze_google_results", analyze_google_results )
    graph_builder.add_node( "analyze_bing_results", analyze_bing_results )
    graph_builder.add_node( "analyze_reddit_results", analyze_reddit_results )
    graph_builder.add_node( "synthesize_analysis", synthesize_analysis )