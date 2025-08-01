import json
import re
import spacy
from pathlib import Path

nlp = spacy.load("pt_core_news_lg")

names = ["AS", "PL"]

def is_valid_name(name):
    return len(name.split()) >= 2

def normalize_first_letter(name):
    return re.sub(r'[^a-zA-Z]', '', name[0].lower())

def is_person_name(name):
    doc = nlp(name)
    for ent in doc.ents:
        if ent.label_ == "PER":
            return True
    return False

def extract_name_and_bio(node):
    bio = node.get("bioHist", "").strip()
    title = node.get("title", "").strip()
    name = ""

    if title and title != "Sem título" and re.match(r"^[A-ZÁÉÍÓÚÃÕÂÊÔa-záéíóúãõâêôç\s]+$", title) and bio != "Sem biografia":
        if is_valid_name(title):
            name = title

    if bio and bio != "Sem biografia":
        match = re.match(r"([A-ZÁÉÍÓÚÃÕÂÊÔa-záéíóúãõâêôç\s\[\]\.]+?) (nasceu|foi|é|,|tinha|morreu|faleceu|nascido|nascida)", bio)
        if match:
            extracted_name = match.group(1).strip("[] ")
            if is_valid_name(extracted_name):
                name = extracted_name

        if not name and title and is_valid_name(title):
            name = title

    if name and bio:
        return name, bio
    return None, None

for name in names:
    input_path = Path(f"./save_data/nodes_info_{name}.json")
    output_path = Path(f"./save_data/people_biographies_{name}.json")

    print(f"\n🔍 A processar: {input_path.name} -> {output_path.name}")
    
    if not input_path.exists():
        print(f"Ficheiro não encontrado: {input_path}")
        continue

    with input_path.open("r", encoding="utf-8") as f:
        nodes = json.load(f)

    people_biographies = {}

    for node_id, node_data in nodes.items():
        person_name, bio = extract_name_and_bio(node_data)
        if person_name and bio and is_person_name(person_name):
            if person_name in people_biographies:
                if len(bio) > len(people_biographies[person_name]):
                    people_biographies[person_name] = bio
            else:
                people_biographies[person_name] = bio

    sorted_bios = dict(sorted(
        people_biographies.items(),
        key=lambda x: normalize_first_letter(x[0])
    ))

    with output_path.open("w", encoding="utf-8") as out_file:
        json.dump(sorted_bios, out_file, ensure_ascii=False, indent=2)

    print(f"Biografias extraídas com sucesso para '{name}'! Guardadas em '{output_path.name}'")
