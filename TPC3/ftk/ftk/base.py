import re
import jjcli
from collections import Counter

def lexer(txt):
    return re.findall(r'\w+(?:-\w+)*[^\W\s]+', txt)

def counter(tokens):
    return Counter(tokens)

def frequencias_relativas(c):
    total_count = sum(c.values())
    return {token: count / total_count for token, count in c.items()}

def modificar_frequencias(c, modificacao):
    # Adiciona ou subtrai frequências no counter
    for token, valor in modificacao.items():
        c[token] += valor
    return c

def main():
    cl = jjcli.clfilter()
    tokens = list()

    for txt in cl.text():
        t = lexer(txt)
        print(t)
        tokens.extend(t)  

    c = counter(tokens)
    print("Frequências brutas:", c)

    frequencias_rel = frequencias_relativas(c)
    print("Frequências relativas:", frequencias_rel)

    modificacao = {'exemplo-token': 2, 'outro-token': -1}  
    c_modificado = modificar_frequencias(c, modificacao)
    print("Frequências modificadas:", c_modificado)

if __name__ == "__main__":
    main()
