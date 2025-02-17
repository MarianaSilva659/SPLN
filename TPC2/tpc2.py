#!/usr/bin/env python3
from jjcli import *

def remove_linhas_repetidas(cl):
    linhas_vistas = list()
    print("clp \n", cl.opt)
    for linha in cl.input():
        # Manter os espaços extras da linha (-s)
        if "-s" in cl.opt:
            print("-s")
            ln = linha
        # Remove espaços extras e quebras de linha
        else:
            ln = linha.strip()            
        
        if "-p" in cl.opt and ln in linhas_vistas:
            linha_comentada = "# " + ln
            linhas_vistas.append(linha_comentada)
            
        if not ln or ln not in linhas_vistas:
            # (-e)
            if "-e" in cl.opt and linha != "":
                linhas_vistas.append(ln)
            elif "-e" not in cl.opt:
               # print(linha)
                linhas_vistas.append(ln)
                

    for l in linhas_vistas:
        print(l)

def main():
    cl = clfilter(opt="sep", man=__doc__)
    remove_linhas_repetidas(cl)

if __name__ == "__main__":
    main()