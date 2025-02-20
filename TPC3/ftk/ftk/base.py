import re
import jjcli
from collections import Counter

def lexer(txt):
    return re.findall(r'\w+(?:-\w+)*[^\W\s]+',txt)
   
def counter(tokens):
    return Counter(*tokens) 
    
def main():
    cl = jjcli.clfilter()
    tokens = list()
    for txt in cl.text():
        t = lexer(txt)
        print(t)
        tokens.append(t)
    c = counter(tokens)
    print(c)