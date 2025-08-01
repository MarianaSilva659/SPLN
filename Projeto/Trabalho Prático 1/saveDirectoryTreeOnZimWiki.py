import json
import os

def get_information(identifier, nodes_info):
    return f"**Tipo**: {nodes_info[identifier]['type']}\n**Título**: {nodes_info[identifier]['title']}"

def write_zim_from_nodes(nodes_info, zim_directory):
    """Cria uma página Zim para cada node, direto no diretório raiz."""
    os.makedirs(zim_directory, exist_ok=True)

    for identifier, info in nodes_info.items():
        page_path = os.path.join(zim_directory, f"{identifier}.txt")
        with open(page_path, 'w', encoding='utf-8') as zim_file:
            zim_file.write(f"= {identifier} =\n")
            zim_file.write(f"{get_information(identifier, nodes_info)}\n")

def load_dict_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

if __name__ == "__main__":
    names = ["AS", "PL"]

    for name in names:
        try:
            nodes_info = load_dict_from_file(f'./save_data/nodes_info_{name}.json')
            zim_directory = f'./zim_wiki_{name}'

            write_zim_from_nodes(nodes_info, zim_directory)

            print(f"Zim wiki gerada com sucesso para '{name}' em: {zim_directory}")
        except FileNotFoundError as e:
            print(f"Erro: Arquivo não encontrado - {e}")
        except Exception as e:
            print(f"Erro ao gerar wiki Zim para '{name}': {e}")
