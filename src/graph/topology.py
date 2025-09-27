# LangGraph
from langgraph.graph import START, END

def register_topology( graph_builder ):
    # On start, graph will run the google_search and bing_search nodes in parallel
    graph_builder.add_edge( START, "google_search" )
    graph_builder.add_edge( START, "bing_search" )
    graph_builder.add_edge( START, "reddit_search" )

    # On successful completion of the google_search and bing_search nodes, the graph will run the analyze_google_results and analyze_bing_results nodes in parallel
    graph_builder.add_edge( "google_search", "analyze_google_results" )
    graph_builder.add_edge( "bing_search", "analyze_bing_results" )
    graph_builder.add_edge( "reddit_search", "analyze_reddit_posts" )

    # On successful completion of the analyze_reddit_posts node, the graph will run the retrieve_reddit_posts node
    graph_builder.add_edge( "analyze_reddit_posts", "retrieve_reddit_posts" )

    # On successful completion of the retrieve_reddit_posts node, the graph will run the analyze_google_results, analyze_bing_results, and analyze_reddit_results nodes in parallel
    graph_builder.add_edge( "retrieve_reddit_posts", "analyze_reddit_results" )
    # On successful completion of the analyze_google_results, analyze_bing_results, and analyze_reddit_results nodes, the graph will run the synthesize_analysis node
    graph_builder.add_edge( "analyze_google_results", "synthesize_analysis" )
    graph_builder.add_edge( "analyze_bing_results", "synthesize_analysis" )
    graph_builder.add_edge( "analyze_reddit_results", "synthesize_analysis" )
    
    # On successful completion of the synthesize_analysis node, the graph will end
    graph_builder.add_edge( "synthesize_analysis", END )