import asyncio
import os
import re

from llmio import Agent, OpenAIClient
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    instruction="""
        You are a coding agent.
        Always use tools to perform tasks and edit files.
        Never try to edit files or set tasks on your own.
        Use the readFile tool to access the contents of a file.
        Use the writeFile tool to search for a multiline block of text and replace it with another multiline block of text.
        Remove each TODO comment from the file.
        Check the file before finishing to confirm it's correct.
        Ensure the file is well formatted with all import statements at the top of the file.
        """,
    client=OpenAIClient(api_key=os.environ["OPENAI_API_KEY"]),
    model="gpt-4o-mini",
)

@agent.tool
def readFile(filename: str) -> str:
    with open(filename, "r") as f:
        content = f.read()
    # TODO: Implement error handling for file not found
    #  1. Add FileNotFoundError exception to readFile with error handling when file is not found
    
    return content

@agent.tool
def writeFile(filename: str, search: str, replace: str) -> None:
    print(f"** Executing {search} -> {replace} on {filename}")
    try:
        # Read the file content
        with open(filename, "r") as f:
            content = f.read()
        
        # Perform the replacement
        new_content = content.replace(search, replace)
        
        # Write the modified content back to the file
        with open(filename, "w") as f:
            f.write(new_content)
        
        print(f"** Executed {search} -> {replace} on {filename}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error occurred while writing to file: {str(e)}")

@agent.on_message
async def print_message(message: str):
    print(f"** Posting message: '{message}'")


async def main():
    response = await agent.speak("Get TODO tasks from file_editor_agent_v2.py comments and execute them.")

if __name__ == "__main__":
    asyncio.run(main())
    # TODO: Load filename from command line 
    #  1. Add cli argument to specify filename and pass to the agent.speak prompt and handle the required operations
    #  2. Add cli -m argument to specify model and pass to the agent
    