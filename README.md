# GPT-Terminal

GPT-Terminal, a large language model prompt engineered to perform tasks over the terminal from simple bash commands to code generation.

## Install
```bash
pip3 install -r requirements.txt
```

## Usage
GPT-Terminal can execute terminal commands as well as python code based on a prompt. For example, let's ask it to list all the files in the current directory:

```bash
$ python3 src/main.py
> list all the files in the current directory
ls
LICENSE
README.md
TODO.md
requirements.txt
src
```

Now, let's ask it to generate python code. Pass in the `-py` or `--python` argument and a prompt: 

```bash
$ python3 src/main.py --python
> write a function that prints the fibonacci sequence
def fibonacci_sequence(n):
    sequence = []
    a, b = 0, 1
    for i in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

n = int(input("Enter the number of terms: "))
result = fibonacci_sequence(n)
print(result)
```

Pass in the `-c` or `--chat` argument to initialize a conversation. 


```bash
$ python3 src/main.py --chat
> What is the capital of california?
The capital of California is Sacramento. It is located in the northern part of the state and is known for its rich history, diverse culture, and beautiful architecture. Sacramento became the capital of California in 1854, replacing the previous capital, San Jose. It is home to many government buildings, including the California State Capitol, which houses the state legislature and the office of the governor. The city is also known for its vibrant arts scene, with numerous museums, theaters, and galleries.
```