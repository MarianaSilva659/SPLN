import re
import jjcli
from collections import Counter

def lexer(txt):
    return re.findall(r'\w+(?:-\w+)*[^\W\s]+', txt)

def counter(tokens):
    return Counter(tokens)

def frequencias_relativas(c):
    total_count = sum(c.values())
    frequencias_relativas = {}
    
    for token, count in c.items():
        frequencia_relativa = count / total_count
        frequencias_relativas[token] = frequencia_relativa
    
    return frequencias_relativas

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
        print("lexer ", t)
        tokens.extend(t)  

    c = counter(tokens)
    print("Frequências brutas:", c)

    frequencias_rel = frequencias_relativas(c)
    print("Frequências relativas:", frequencias_rel)

    modificacao = {'ola': 2, "aa":10}  
    c_modificado = modificar_frequencias(c, modificacao)
    print("Frequências modificadas:", c_modificado)

if __name__ == "__main__":
    main()
