import json
import spacy
from pathlib import Path

nlp = spacy.load('pt_core_news_lg')

names = ["AS", "PL"]

def extrair_entidades(texto):
    doc = nlp(texto)
    pessoas = set()
    lugares = set()
    casas = set()

    for ent in doc.ents:
        if ent.label_ == "PER":
            pessoas.add(ent.text)
        elif ent.label_ == "LOC":
            lugares.add(ent.text)
        elif ent.label_ == "FAC":
            casas.add(ent.text)

    return {
        "pessoas": list(pessoas),
        "casas": list(casas),
        "lugares": list(lugares)
    }

for name in names:
    ficheiro = Path(f"./save_data/nodes_info_{name}.json")
    
    with ficheiro.open(encoding="utf-8") as f:
        dados = json.load(f)

    resultado = {}

    for id_, reg in dados.items():
        texto_total = " ".join([
            reg.get("title", ""),
            reg.get("scopeContent", ""),
            reg.get("bioHist", "")
        ])
        entidades = extrair_entidades(texto_total)
        resultado[id_] = entidades

    output_path = f"./save_data/extracted_entities_{name}.json"
    with open(output_path, "w", encoding="utf-8") as f_out:
        json.dump(resultado, f_out, ensure_ascii=False, indent=2)

    print(f"Entidades extraídas com sucesso para '{name}'! Guardadas em '{output_path}'")
