import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Erro: Nenhum arquivo foi fornecido como argumento.")
        sys.exit(1)
    
    f = sys.argv[1]
    file_result = sys.argv[2]

    if not os.path.isfile(f):
        print(f"Erro: O arquivo '{f}' não foi encontrado.")
        sys.exit(1)

    with open(f, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    visto = set()
    with open(file_result, "w", encoding="utf-8") as output_file:
        for linha in linhas:
            linha_limpa = linha.rstrip()  # Remove espaços à direita, mas mantém linhas em branco
            
            if linha_limpa not in visto or linha_limpa == "":  
                output_file.write(linha)  # Mantém a formatação original
                visto.add(linha_limpa)  

    print("\nLinhas únicas foram salvas em", file_result)

if __name__ == "__main__":
    main()
