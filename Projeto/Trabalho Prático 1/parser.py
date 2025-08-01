import json
import re
import xml.etree.ElementTree as ET
from collections import defaultdict

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    ns = {'oai': 'http://www.openarchives.org/OAI/2.0/',
          'data': 'http://schemas.datacontract.org/2004/07/Data'}
    
    nodes = dict()
    hierarchy = defaultdict(list)  
    root_parents = set()

    for record in root.findall(".//oai:record", ns):
        metadata = record.find(".//oai:metadata", ns)
        if metadata is None:
            continue
        
        description = metadata.find(".//data:DescriptionItem", ns)
        if description is None:
            continue
        
        record_id = description.find("data:ID", ns)
        parent_id = description.find("data:Parent", ns)
        root_parent_id = description.find("data:RootParent", ns)
        type_ = description.find("data:DescriptionLevel", ns)
        title = description.find("data:UnitTitle", ns)
        link = description.find("data:IdentifierUrl", ns)
        scopeContent = description.find("data:ScopeContent", ns)
        useRestrict = description.find("data:UseRestrict", ns)
        term = description.find("data:Terms", ns)
        bioHist = description.find("data:BiogHist", ns)
        custodHist = description.find("data:CustodHist", ns)
        
        geogName = description.find("data:GeogName", ns)
        record_id = record_id.text if record_id is not None else "Sem record_id"
        parent_id = parent_id.text if parent_id is not None else "Sem parent_id"
        root_parent_id = root_parent_id.text if root_parent_id is not None else "Sem root_parent_id"
        root_parents.add(root_parent_id)
        type_ = type_.text if type_ is not None else "Sem type"
        title = title.text if title is not None else "Sem title"
        link = link.text if link is not None else "Sem link"
        scopeContent = scopeContent.text if scopeContent is not None else "Sem scopeContent"
        useRestrict = useRestrict.text if useRestrict is not None else "Sem useRestrict"
        term = term.text if term is not None else "Sem Terms"
        term_list = []
        if term != "Sem Terms":
            split_terms = re.split(r",|\s+e\s+", term)
            term_list = [t.strip().capitalize() for t in split_terms if t.strip()]
        bioHist = bioHist.text if bioHist is not None else "Sem biografia"
        custodHist = custodHist.text if custodHist is not None else "Sem custodHist"
        geogName = geogName.text if geogName is not None else "Sem geogName"

        nodes[record_id] = {"id": record_id, "parent": parent_id, "root_parent": root_parent_id, "title":title, "type": type_, "link": link, "scopeContent": scopeContent, "useRestrict": useRestrict, "term": term_list, "bioHist": bioHist, "custodHist": custodHist, "geogName": geogName}
        hierarchy[parent_id].append(record_id)
    return nodes, hierarchy, root_parents

def add_son_to_node(directory_tree, parent_value, new_son):
        for root_key, root_data in directory_tree.items():
            for son in root_data['sons']:
                if son['node'] == parent_value:
                    son['sons'].append({
                        'node': new_son,
                        'sons': []
                    })
                    return True  
                if len(son['sons']) > 0:
                    if add_son_to_node({'root': {'sons': son['sons']}}, parent_value, new_son):
                        return True
        
        return False  

def getDirectoryTree(nodes, hierarchy, root_parents, num_nodes):
    directory_tree = dict()
    current_parents = set()
    num_root = 1
    num_nodes = 0
    #Cria um objeto para cada RootParent
    for root_parent in root_parents:
        directory_tree[root_parent] = {
            'sons': []
        }
        num_root += 1
        #print(f'root_parent {root_parent} -> {hierarchy[root_parent]}')
        if len(hierarchy[root_parent]) > 0:
            num_parent = 1
            for son in hierarchy[root_parent]:
                node = {
                    'node' : son,
                    'sons': []
                }
                directory_tree[root_parent]['sons'].append(node)
                current_parents.add(son)
            while len(current_parents) > 0: 
                new_parents = set()
                for parent in current_parents:
                    if len(hierarchy[parent]) > 0:
                        for son in hierarchy[parent]:
                            add_son_to_node(directory_tree, parent,son)
                            new_parents.add(son)
                            
                current_parents = new_parents
    return directory_tree   
    #for r in directory_tree:
    #print("\n r", directory_tree['78502'])



def save_dict_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file)


xml_files = ["./arquivoOAI/ponteDeLima.xml","./arquivoOAI/alberto_sampaio_archeevo.xml" ]
names = ["PL", "AS"]

if __name__ == "__main__":
    i = 0
    for file in xml_files:
        xml_file = file
        nodes, hierarchy, root_parents = parse_xml(xml_file)
        orphan_parents = {parent for parent in hierarchy if parent not in nodes}

        deriva = dict()
        for orphan in orphan_parents:
            deriva[orphan] = hierarchy[orphan]

        deriva_output_file = f'./save_data/files_non-existent_parent_{names[i]}.json'
        save_dict_to_file(deriva, deriva_output_file)

        nodesoutputfile = f'./save_data/nodes_info_{names[i]}.json'
        save_dict_to_file(nodes, nodesoutputfile)
        #print("Árvore Arquivística:")
        #print("\nNúmeros de nodos ", len(nodes))
        #print("\nNúmero do Root Parents ", len(root_parents))
        ##hierarchy -> pai : [filhos]
        ##nodes -> {nodo : {id, pai, root_parent(representa Secções),titulo, type}}
        directory_tree = getDirectoryTree(nodes, hierarchy, root_parents, len(nodes))
        directorysoutputfile = f'./save_data/directory_tree_{names[i]}.json'
        save_dict_to_file(directory_tree, directorysoutputfile)
        i += 1
