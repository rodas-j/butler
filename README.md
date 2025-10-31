# PyButler

PyButler is an open-source NLP application that helps create Notion-style database structures through natural language prompts. The project leverages Langchain for LLM orchestration and OpenAI's GPT models to intelligently generate database schemas with properties, types, and sample data.

## Features

- Natural language to database schema conversion
- Notion-style property type support (Text, Number, Select, Multi-select, Date, etc.)
- Automatic sample data generation
- Firebase integration for prompt/response storage
- RESTful API built with Flask
- MCP (Model Context Protocol) integration with Todoist

## MCP Setup (Todoist Integration)

This project includes configuration for the official Todoist MCP server, allowing AI assistants to interact with Todoist tasks.

### Prerequisites

- Node.js and npm/npx installed
- Todoist API token ([Get one here](https://todoist.com/app/settings/integrations/developer))

### Configuration

1. The MCP configuration is located in `.claude/mcp.json`
2. Set your Todoist API token in your environment:
   ```bash
   export TODOIST_API_TOKEN=your_token_here
   ```

3. For Claude Code or compatible AI assistants, the MCP server will automatically connect when configured

### Getting Your Todoist API Token

1. Go to [Todoist Integrations](https://todoist.com/app/settings/integrations/developer)
2. Scroll to "API token" section
3. Copy your token and add it to your `.env` file

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/rodas-j/butler.git
cd butler

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/rodas-j/butler.git
cd butler

# Install dependencies
pip install -r requirements.txt
```

## Environment Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   TODOIST_API_TOKEN=your_todoist_api_token_here
   PORT=8080
   ```

## Usage

### Running the Flask Application

```bash
# Development mode
python main.py

# Production mode with Gunicorn
gunicorn -w 1 -t 8 -b 0.0.0.0:8080 main:app
```

### API Endpoints

#### Health Check
```bash
GET /
```

#### Generate Database (Simple)
```bash
POST /database
Content-Type: application/json

{
  "prompt": "Create a task tracker database"
}
```

#### Generate Database (Advanced with Firebase)
```bash
POST /beta/database
Content-Type: application/json

{
  "prompt": "Create a 2023 goal tracker with status columns"
}
```

### Running with Docker

```bash
# Build the image
docker build -t pybutler .

# Run the container
docker run -p 8080:8080 --env-file .env pybutler
```

## Development

### Code Quality Tools

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **Mypy**: Type checking
- **Pytest**: Testing
- **Pre-commit hooks**: Automatic formatting on commit

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=butler

# Run specific test file
pytest tests/test_database.py
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Project Structure

```
butler/
├── .claude/              # MCP configuration
│   └── mcp.json          # Todoist MCP setup
├── butler/               # Main application package
│   ├── app.py            # OpenAI query functions
│   ├── config.py         # LLM and property configurations
│   ├── firebase.py       # Firebase integration
│   ├── strings.py        # Database property definitions
│   ├── utils.py          # Utility functions
│   └── database/         # Database chain implementation
│       ├── database.py   # Main DatabaseChain class
│       ├── api.py        # Response generation
│       └── config.py     # Database configuration
├── tests/                # Test files
├── main.py               # Flask application entry point
├── logger.py             # Logging configuration
├── pyproject.toml        # Poetry configuration
├── requirements.txt      # Pip requirements
└── Dockerfile            # Docker configuration
```

## Architecture

### DatabaseChain

The core of PyButler is the `DatabaseChain` class, which uses a builder pattern to process natural language through multiple LLM steps:

1. **Add Columns**: Identifies properties from the prompt
2. **Add Property Types**: Assigns appropriate Notion-style types
3. **Add Options**: Generates select/multi-select options
4. **Add Content**: Creates sample data entries
5. **Add Details**: Generates title, description, and emoji

### Supported Property Types

- Title
- Text
- Number
- Select
- Multi-select
- Date
- Person
- Files & Media
- Checkbox
- URL
- Email
- Phone
- Formula
- Relation
- Rollup
- Created Time
- Created By
- Last Edited Time
- Last Edited By

## Contributing

We welcome contributions to PyButler! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Credits

PyButler was created by [Rodas Jateno](https://twitter.com/WorkichoRodas).

## License

This project is licensed under the GPL license. Please refer to the `LICENSE` file for more information.

## Acknowledgments

- Built with [Langchain](https://langchain.readthedocs.io/en/latest/)
- Powered by OpenAI GPT models
- MCP integration via [Model Context Protocol](https://modelcontextprotocol.io/)

## Contact

For questions or feedback, reach out to [@WorkichoRodas](https://twitter.com/WorkichoRodas) on Twitter.

## Changelog

### 0.2.0 (Current)
- Added MCP (Model Context Protocol) integration with Todoist
- Cleaned up repository structure
- Enhanced documentation
- Added environment variable examples

### 0.1.0
- Initial release
- Basic database generation from natural language
- Flask API implementation
- Firebase integration
