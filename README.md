# LangGraph Advanced Example

A sophisticated chatbot application built with LangGraph that demonstrates advanced graph-based AI workflows for multi-source research and analysis.

## Overview

This project showcases a complex LangGraph implementation that performs parallel searches across multiple sources (Google, Bing, and Reddit), analyzes the results, and synthesizes comprehensive answers. The graph-based architecture allows for efficient parallel processing and sophisticated data flow management.

## Features

- **Multi-Source Research**: Simultaneous searches across Google, Bing, and Reddit
- **Parallel Processing**: Efficient concurrent execution of search and analysis operations
- **Intelligent Analysis**: AI-powered analysis of search results from each source
- **Synthesis Engine**: Combines insights from multiple sources into coherent answers
- **Interactive Chatbot**: Command-line interface for real-time interaction
- **Modular Architecture**: Clean separation of concerns with dedicated modules for different operations

## Architecture

The application uses a sophisticated graph topology that orchestrates the following workflow:

1. **Parallel Search Phase**
   - Google Search
   - Bing Search  
   - Reddit Search

2. **Analysis Phase**
   - Analyze Google results
   - Analyze Bing results
   - Analyze Reddit posts and retrieve relevant content
   - Analyze retrieved Reddit results

3. **Synthesis Phase**
   - Combine all analyses into a final comprehensive answer

## Project Structure

```
├── main.py                        # Application entry point
├── chatbot.py                     # Interactive chatbot interface
├── pyproject.toml                 # Project dependencies and configuration
└── src/
    ├── graph/
    │   ├── graph_builder.py       # Graph construction logic
    │   ├── topology.py            # Graph topology and edge definitions
    │   ├── registry.py            # Node registration
    │   ├── schemas.py             # Data models and state definitions
    │   └── nodes/
    │       ├── search.py          # Search operation nodes
    │       ├── retrieve.py        # Data retrieval nodes
    │       ├── analysis.py        # Analysis operation nodes
    │       └── synthesize.py      # Synthesis operation nodes
    ├── llm/
    │   └── client.py              # LLM client configuration
    ├── operations/
    │   ├── web_operations.py      # Web scraping and API operations
    │   └── snapshot_operations.py # Data snapshot operations
    └── prompts/
        └── templates.py           # Prompt templates
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd langgraph-advance-example
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_custom_search_engine_id
BING_API_KEY=your_bing_api_key_here
```

## Usage

Run the chatbot:
```bash
python main.py
```

The chatbot will start and prompt you for questions. Type your question and the system will:

1. Perform parallel searches across Google, Bing, and Reddit
2. Analyze the results from each source
3. Synthesize a comprehensive answer based on all findings

Type `exit` to quit the chatbot.

## Dependencies

- **Python**: >=3.13
- **LangGraph**: >=0.6.6 - Graph-based workflow orchestration
- **LangChain**: >=0.3.27 - LLM integration and tooling
- **jsonpatch**: >=1.33 - JSON document modification
- **python-dotenv**: >=1.1.1 - Environment variable management

## Graph Flow

The application uses a sophisticated graph topology:

```
START
├── google_search ──────────► analyze_google_results ──┐
├── bing_search ────────────► analyze_bing_results ────┼──► synthesize_analysis ──► END
└── reddit_search ──► analyze_reddit_posts ──► retrieve_reddit_posts ──► analyze_reddit_results ──┘
```

## Key Components

### State Management
The application maintains a comprehensive state object that tracks:
- User messages and questions
- Search results from each source
- Analysis results from each source
- Final synthesized answers

### Node Types
- **Search Nodes**: Perform searches across different platforms
- **Analysis Nodes**: Process and analyze search results
- **Retrieval Nodes**: Fetch detailed content from selected sources
- **Synthesis Nodes**: Combine analyses into final answers

### Parallel Processing
The graph architecture enables efficient parallel execution of independent operations, significantly improving response times for complex queries.

## Development

The project is structured for easy extension and modification:

1. **Adding New Search Sources**: Implement new search nodes in `src/graph/nodes/search.py`
2. **Custom Analysis Logic**: Modify analysis nodes in `src/graph/nodes/analysis.py`
3. **Graph Topology Changes**: Update the topology in `src/graph/topology.py`
4. **State Schema Updates**: Modify schemas in `src/graph/schemas.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Built with LangGraph for advanced AI workflow orchestration and LangChain for LLM integration.
