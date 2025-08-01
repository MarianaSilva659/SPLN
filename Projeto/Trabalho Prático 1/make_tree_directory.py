
import json

def get_information(identifier, nodes_info):
    node = nodes_info.get(identifier)
    if node and node.get('type'):
        return f"-{node['type']}-{node.get('title', 'Sem título')}"
    return "Sem informação"




def write_to_txt(directory_tree, nodes_info, file_name):
    """Escreve a árvore em um arquivo de texto, adicionando a informação extra."""
    def recursive_write(node, indent_level, file):
        identifier = node['node']
        additional_info = get_information(identifier, nodes_info)
        file.write(f"{'    ' * indent_level}{identifier}{additional_info}\n")
        
        for son in node['sons']:
            recursive_write(son, indent_level + 1, file)

    with open(file_name, 'w', encoding='utf-8') as file:
        for root_key, root_data in directory_tree.items():
            additional_info = get_information(root_key, nodes_info)
            file.write(f"{root_key}{additional_info}\n")
            for son in root_data['sons']:
                recursive_write(son, 1, file)  

def load_dict_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

    

if __name__ == "__main__":
    names = ["PL", "AS"]

    for name in names:
        try:
            nodes_info = load_dict_from_file(f'./save_data/nodes_info_{name}.json')
            directory_tree = load_dict_from_file(f'./save_data/directory_tree_{name}.json')

            output_filename = f'arvoreDiretorias_{name}.txt'
            write_to_txt(directory_tree, nodes_info, output_filename)

            print(f"Ficheiro de árvore de diretorias gerado: {output_filename}")

        except FileNotFoundError as e:
            print(f" Erro: Ficheiro não encontrado - {e}")
        except Exception as e:
            print(f" Erro ao gerar ficheiro para '{name}': {e}")

