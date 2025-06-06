# Pydantic GitHub Agent

A simple AI agent that answers questions about GitHub Repos<br>

## Screenshots

![CLI and model reasoning](https://i.imgur.com/9cEiJ6M.png)
![output](https://i.imgur.com/a3qlkDp.png)

## Functionality

- Single-agent architecture built with Pydantic AI that utilizes tools to pull:
  - Information about the repo (name, description, size, owner, etc)
  - Repo structure
  - File content
- Observability and tracing using Langfuse
- CLI interface to interact with the agent
- Qwen3 8B for reasoning and tool use
- LLM locally served via LM studio (with ollama)

## Frameworks

1. Pydantic AI (for agents)
2. Langfuse (for observability and tracing)
3. Httpx (for making http requests to GitHub)

## Installation

1. Clone this repo
2. Create and activate a virtual environment
3. Run `pip install -r requirements.txt`
4. Spin up langfuse locally or create a project on the cloud
5. Rename `.env.example` to `.env` and add the necessary variables
6. Run `python cli.py` to start talking with the agent

## My Local Testing Setup

- Qwen3 8B served via LM studio (with Ollama runtime)
- A docker deployed instance of langfuse

## Usage

1. Once you run `cli.py` talk to the agent and ask it to give you information about a github repo by providing its url within the prompt
2. After the model responds, you can check traces on langfuse dashboard

## Example Run

![langfuse traces](https://i.imgur.com/PBaxwH5.png)
![trace example](https://i.imgur.com/abYO6sQ.png)
