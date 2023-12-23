from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from prompts import terminal_role

from dotenv import load_dotenv
from colorama import Fore, Style

import os
import subprocess
import openai

import warnings
warnings.filterwarnings("ignore")


# Load variables from .env into the environment
load_dotenv()

# Access the variable OPENAI_API_KEY using the `os` module
openai.api_key = os.getenv("OPENAI_API_KEY")

exit_commands = ["exit", "quit", "q", "bye", "goodbye", "stop", "end", "finish", "done"]

def run_bash_command(bash_command: str) -> None:
    try:
        subprocess.run(bash_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {str(e)}")
        # print(Fore.RED + str(e) + Style.RESET_ALL)

def main():
    history = [SystemMessage(content=terminal_role)]
    chat = ChatOpenAI(model="gpt-4")

    while (query := input(Fore.GREEN + Style.BRIGHT + "> " + Style.RESET_ALL)) not in exit_commands:
        history.append(HumanMessage(content=query))

        response = chat(history)

        print(Fore.GREEN + Style.BRIGHT + response.content + Style.RESET_ALL)
        
        history.append(response)

        run_bash_command(response.content)

main()