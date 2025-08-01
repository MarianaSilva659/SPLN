import json
import spacy
import re
from pathlib import Path

nlp = spacy.load('pt_core_news_lg')

names = ["PL"]

def remover_pos_quebras(texto):
    partes = re.split(r'\n{1,5}', texto)
    return partes[0].strip()


def extrair_info_formatada(scope_content):
    doc_scope_content = nlp(scope_content)
    pessoas = []
    lugares = []

    for ent in doc_scope_content.ents:
        if ent.label_ == "PER":
            pessoas.append(remover_pos_quebras(ent.text.strip()))
        elif ent.label_ == "LOC":
            lugares.append(remover_pos_quebras(ent.text.strip()))

    profissionais = []
    profissoes_detectadas = set()

    for pessoa in pessoas:
        match = re.search(rf'([^\n:]+):\s*{re.escape(pessoa)}', scope_content)
        if match:
            profissao = match.group(1).strip()
            profissoes_detectadas.add(profissao)
            profissionais.append({"nome": pessoa, "profissao": profissao})
        else:
            profissionais.append({"nome": pessoa, "profissao": None})

    # Filtrar pessoas cujo nome é uma profissão
    profissionais_filtrados = [
        p for p in profissionais
        if p["nome"] not in profissoes_detectadas
    ]

    return {
        "pessoas": profissionais_filtrados,
        "lugares": lugares
    }


for name in names:
    ficheiro = Path(f"./save_data/nodes_info_{name}.json")
    
    with ficheiro.open(encoding="utf-8") as f:
        dados = json.load(f)

    resultado = {}

    for id_, reg in dados.items():
     
        scope_content = reg.get("scopeContent", "")

        entidades = extrair_info_formatada(scope_content)
        resultado[id_] = entidades

    profissoes_detectadas = set()
    for entidade in resultado.values():
        for pessoa in entidade["pessoas"]:
            if pessoa["profissao"]:
                profissoes_detectadas.add(pessoa["profissao"])

    for entidade in resultado.values():
        entidade["pessoas"] = [
            p for p in entidade["pessoas"]
            if p["nome"] not in profissoes_detectadas
        ]

    output_path = f"./save_data/extracted_entities_SS{name}.json"
    with open(output_path, "w", encoding="utf-8") as f_out:
        json.dump(resultado, f_out, ensure_ascii=False, indent=2)

    print(f"Entidades extraídas com sucesso para '{name}'! Guardadas em '{output_path}'")
