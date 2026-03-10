# AI Command Execution Agent

Multi-agent system powered by OpenAI GPT-4o that helps users plan, execute, and manage projects through an interactive conversation

## Features

- Interactive step-by-step project execution (plan → ask → action → observe cycle)
- Tool integration: run commands, write/read files
- AI-guided project creation with user feedback loops
- JSON-structured responses for clarity

### Prerequisites

- Python 3.8+
- OpenAI API key (from openai.com)
- pip

## Setup Instructions

- Clone/download the project
- Create `.env` file in the project root
- Add your API key: `OpenAI_API_KEY=your_api_key_here`
- Install dependencies: `pip install -r requirements.txt`

- Run: `python app.py`
- `.env` File Setup

```py
OpenAI_API_KEY=sk-xxxxxxxxxxxxx
```

Get your key from: https://platform.openai.com/api-keys

## How It Works

- The agent works through defined steps: plan, ask, action, observe
- Supports creating projects with proper folder structure
- Guides through decision-making with questions
- Executes system commands and manages files

### Available Tools

- `run_command`: Execute system commands
- `write_file`: Create/edit files
- `read_file`: Read existing files
