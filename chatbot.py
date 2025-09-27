def run_chatbot(graph):
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
            # "reddit_results": None,
            # "selected_reddit_urls": None,
            # "reddit_post_data": None,
            "google_analysis": None,
            "bing_analysis": None,
            # "reddit_analysis": None,
            "final_answer": None,
        }

        print( "\nStarting parallel research process..." )
        print( "Launching Google and Bing searches...\n" )

        final_state = graph.invoke( state )

        if final_state.get( "final_answer" ):
            print( f"\nFinal Answer:\n{ final_state.get( 'final_answer' ) }\n" )

        print( "-" * 80 )