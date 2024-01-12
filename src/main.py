from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from prompts import terminal_role, code_assistant_role
from dotenv import load_dotenv
from colorama import Fore, Style
import os
import subprocess
import argparse

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default=None)
    parser.add_argument("-c", "--code", action="store_true")
    # parser.add_argument("-c", "--code", action="store_const", const=code_assistant_role, default=terminal_role)
    return parser.parse_args()


def init_model(template):
    # messages = prompt.format(input="What is the current directory?")
    # .format(input="What is the current directory?")
    # .format_messages(input="What is the current directory?")
    # .format_prompt(input="What is the current directory?")
    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{input}")
    ])

    llm = ChatOpenAI(openai_api_key=openai_api_key)
    chain = prompt | llm 
    return chain


args = parse_args()

prompt = None
if args.file:
    with open(args.file, 'r') as file:
        prompt = file.read()

term_chain = init_model(terminal_role)
code_chain = init_model(code_assistant_role)
chain = term_chain if not args.code else code_chain

exit_commands = {"exit", "quit", "q", "bye", "goodbye", "stop", "end", "finish", "done"}
while (query := (input(Fore.GREEN + Style.BRIGHT + "> " + Style.RESET_ALL) if not prompt else prompt )) not in exit_commands:
    response = chain.invoke({"input": query})
    print(Fore.CYAN + Style.BRIGHT + response.content + Style.RESET_ALL)

    # response = llm.invoke(messages)
    # response = llm.invoke({"input": "What is the current directory?"})
    # print(response.content)
    
    # `shell=True` argument allows you to run the command in a shell
    # `capture_output=True` captures the command's output
    # `text=True` argument is used to return the output as a string    
    # command = response.content
    if not args.code:
        command = response.content
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(result.stdout)
        else:
            print(Fore.RED + Style.BRIGHT + result.stderr + Style.RESET_ALL)

        # verbose:
        #   Print the output of the command
        #   print("Output:", result.stdout)
        #   Print the error (if any)
        #   print("Error:", result.stderr)
        #   Print the return code
        #   print("Return Code:", result.returncode)
    
    else:
        python_code = response.content

        template = """
        Generate a python file name that best illustrates the following code:
        {code}
        """
        prompt = PromptTemplate.from_template(template).format(code=python_code)
        
        llm = ChatOpenAI(openai_api_key=openai_api_key)
        response = llm.invoke(prompt)
        
        file_name = response.content
        with open(file_name, "w") as file:
            file.write(python_code)
    
    prompt = None