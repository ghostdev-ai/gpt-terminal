# GPT - Terminal

GPT-Terminal, a large language model with prompt engineering to perform tasks over the terminal from simple bash commands to code generation.

## Install
```bash
pip3 install -r requirements.txt
```

## Usage
GPT - Terminal can execute terminal commands as well as python code based on a prompt. For example, let's ask it to list all the files in the current directory:

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

Now, let's ask it to generate python code. Pass in the `code` or `--code` argument and a prompt: 

```bash
$ python3 src/main.py --code
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