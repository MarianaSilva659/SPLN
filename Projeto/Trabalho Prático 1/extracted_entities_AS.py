import json
import spacy
import re
from pathlib import Path

nlp = spacy.load('pt_core_news_lg')

names = ["AS"]

def remover_pos_quebras(texto):
    partes = re.split(r'\n{1,5}|"', texto)
    return partes[0].strip()

def extrair_info_formatada(title, scope_content, biogHist):
    # Expressões regulares para extrair profissão, freguesia e morada
    regex_profissao = re.search(r'(?i)Profiss[aã]o\s*[:\-–]\s*(.+?)(?:\n|$)', scope_content)
    regex_freguesia = re.search(r'(?i)Freguesia\s*[:\-–]\s*(.+?)(?:\n|$)', scope_content)
    regex_morada = re.search(r'(?i)Morada\s*[:\-–]\s*(.+?)(?:\n|$)', scope_content)

    profissao = regex_profissao.group(1).strip() if regex_profissao else None
    lugares = set()

    for match in [regex_freguesia, regex_morada]:
        if match:
            lugares.add(match.group(1).strip())

    pessoas_info = set()
    lugares_spacy = set()

    usar_titulo_apenas = any([profissao, regex_freguesia, regex_morada])

    # Se for pra usar só o título
    if usar_titulo_apenas:
        doc = nlp(title)
        for ent in doc.ents:
            if ent.label_ == "PER":
                pessoas_info.add((remover_pos_quebras(ent.text.strip()), profissao if profissao else None))
            elif ent.label_ == "LOC":
                lugares_spacy.add(remover_pos_quebras(ent.text.strip()))
    else:
        # Processar os três campos separadamente
        for texto in [title, scope_content, biogHist]:
            doc = nlp(texto)
            for ent in doc.ents:
                if ent.label_ == "PER":
                    pessoas_info.add((remover_pos_quebras(ent.text.strip()), profissao if profissao else None))
                elif ent.label_ == "LOC":
                    lugares_spacy.add(remover_pos_quebras(ent.text.strip()))

    lugares.update(lugares_spacy)

    pessoas_formatadas = [{"nome": nome, "profissao": prof} for nome, prof in pessoas_info]

    return {
        "pessoas": pessoas_formatadas,
        "lugares": list(lugares)
    }


for name in names:
    ficheiro = Path(f"./save_data/nodes_info_{name}.json")
    
    if not ficheiro.exists():
        print(f"Arquivo {ficheiro} não encontrado.")
        continue
    
    with ficheiro.open(encoding="utf-8") as f:
        dados = json.load(f)

    resultado = {}

    for id_, reg in dados.items():
        title = reg.get("title", "")
        scope_content = reg.get("scopeContent", "")
        biogHist = reg.get("biogHist", "")

        entidades = extrair_info_formatada(title, scope_content,biogHist)
        resultado[id_] = entidades

    output_path = f"./save_data/extracted_entities_SS{name}.json"
    with open(output_path, "w", encoding="utf-8") as f_out:
        json.dump(resultado, f_out, ensure_ascii=False, indent=2)

    print(f"Entidades extraídas com sucesso para '{name}'! Guardadas em '{output_path}'")
