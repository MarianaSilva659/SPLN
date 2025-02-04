import sys

def main():
    f = sys.argv[1]
    
    with open(f, "r", encoding="utf-8") as file:
        linhas = file.readlines()
        print("Linhas lidas:", linhas)
    
    texto = list(linhas) 
    print("Texto:", texto)

    visto = set()
    
    with open("resultado.txt", "w", encoding="utf-8") as output_file:
        for linha in texto:
            print(linha)
            if linha not in visto:
                print("entra ", linha , visto)
                output_file.write(linha)
                visto.add(linha)  # Marcar a linha como já 
                print(f"Escrevendo: {linha.strip()}")  # Para mostrar no terminal

    print("\nLinhas únicas foram salvas em 'resultado.txt'")

if __name__ == "__main__":
    main()
