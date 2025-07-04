from __future__ import annotations
from dotenv import load_dotenv
from typing import List
import asyncio
import httpx
import os

from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart

from github_agent import github_agent, GitHubDeps
from configure_langfuse import configure_langfuse

# Load environment variables
load_dotenv()

# Configure Langfuse for agent observability
tracer = configure_langfuse()

class CLI:
    def __init__(self):
        self.messages: List[ModelMessage] = []
        self.deps = GitHubDeps(
            client=httpx.AsyncClient(),
            github_token=os.getenv('GITHUB_TOKEN'),
        )
    
    async def chat(self):
        print("GitHub Agent CLI (type 'quit' to exit)")
        print("Enter your message:")

        try:
            while True:
                user_input = input("> ").strip()
                if user_input.lower() == 'quit' or user_input.lower() == 'q':
                    break

                # Configure Langfuse tracing metadata
                with tracer.start_as_current_span("Pydantic-Ai-Trace") as span:
                    span.set_attribute("langfuse.user.id", "user-456")
                    span.set_attribute("langfuse.session.id", "987654322")
                    span.set_attribute("input.value", user_input)

                    # Run the agent with streaming
                    result = await github_agent.run(
                        user_input,
                        deps=self.deps,
                        message_history=self.messages
                    )
                    
                    # Store the user message
                    self.messages.append(
                        ModelRequest(parts=[UserPromptPart(content=user_input)])
                    )

                    # Store itermediatry messages like tool calls and responses
                    filtered_messages = [msg for msg in result.new_messages() 
                                    if not (hasattr(msg, 'parts') and 
                                            any(part.part_kind == 'user-prompt' or part.part_kind == 'text' for part in msg.parts))]
                    self.messages.extend(filtered_messages)

                    # Optional if you want to print out tool calls and responses
                    # print(filtered_messages + "\n\n")

                    print(result.output)

                    # Add the final response from the agent
                    self.messages.append(
                        ModelResponse(parts=[TextPart(content=result.output)])
                    )
                    
                    # Correct input and output
                    span.set_attribute("output.value", result.output)


        finally:
            await self.deps.client.aclose()

async def main():
    cli = CLI()
    await cli.chat()

if __name__ == "__main__":
    asyncio.run(main())