from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from prompts import terminal_assistant_role, python_assistant_role
from dotenv import load_dotenv
from colorama import Fore, Style
import os
import subprocess
import argparse
 

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--chat", action="store_true")
    parser.add_argument("-f", "--file", nargs="+", action="append", help="Specify one or more text files for prompt chaining.")
    parser.add_argument("-s", "--shell", type=str, default=None)
    parser.add_argument("-py", "--python", action="store_true")
    parser.add_argument("-swe", "--software_engineer", action="store_true")
    # parser.add_argument("-c", "--code", action="store_const", const=code_assistant_role, default=terminal_role)
    return parser.parse_args()


def init_role(template):
    # messages = prompt.format(input="What is the current directory?")
    # .format(input="What is the current directory?")
    # .format_messages(input="What is the current directory?")
    # .format_prompt(input="What is the current directory?")

    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{input}")
    ])

    llm = ChatOpenAI(openai_api_key=openai_api_key, 
                     temperature=0.0)  # lower temperature results in a deterministic model 
    chain = prompt | llm
    return chain


def init_chat():
    chat_chain = ConversationChain(
        llm=ChatOpenAI(openai_api_key=openai_api_key, 
                       model="gpt-3.5-turbo",
                       temperature=0.0),
        memory=ConversationBufferMemory()
    )
    return chat_chain


def chain_prompts(prompts: list[str]):
    pass


def run_subprocess(terminal_command):
    # `shell=True` argument allows you to run the command in a shell
    # `capture_output=True` captures the command's output
    # `text=True` argument is used to return the output as a string    
    result = subprocess.run(terminal_command, 
                            shell=True, 
                            capture_output=True, 
                            text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(Fore.RED + Style.BRIGHT + result.stderr + Style.RESET_ALL)


def main():
    args = parse_args()
    
    term_chain = init_role(terminal_assistant_role)
    code_chain = init_role(python_assistant_role)
    chat_chain = init_chat()


    if args.file:
        chain_prompts(args.file[0])


    chain = term_chain
    if args.chat:
        chain = chat_chain
    elif args.python:
        chain = code_chain

    exit_commands = {"exit", "quit", "q", "bye", "goodbye", "stop", "end", "finish", "done"}
    while (query := input(Fore.GREEN + Style.BRIGHT + "> " + Style.RESET_ALL)) not in exit_commands:
        # response = llm.invoke(messages)
        # response = llm.invoke({"input": "What is the current directory?"})
        # print(response.content)
        if args.chat:
            conversation = chain.invoke({ "input": query })
            print(Fore.CYAN + Style.BRIGHT + conversation["response"] + Style.RESET_ALL)
        else:
            response = chain.invoke({"input": query})
            print(Fore.CYAN + Style.BRIGHT + response.content + Style.RESET_ALL)
        
        if not args.python and not args.chat:
            run_subprocess(response.content)
        else:
            pass

main()