import xml.etree.ElementTree as ET
import yaml

def parse_record(record):
    ns = {
        'oai': 'http://www.openarchives.org/OAI/2.0/',
        'd': 'http://schemas.datacontract.org/2004/07/Data'
    }

    header = record.find('oai:header', ns)
    metadata = record.find('oai:metadata', ns)
    desc = metadata.find('d:DescriptionItem', ns)

    return {
        'id': desc.findtext('d:ID', default='', namespaces=ns),
        'titulo': desc.findtext('d:UnitTitle', default='', namespaces=ns),
        'tipo_titulo': desc.findtext('d:UnitTitleType', default='', namespaces=ns),
        'repo': desc.findtext('d:Repository', default='', namespaces=ns),
        'data': {
            'inicio': desc.findtext('d:UnitDateInitial', default='', namespaces=ns),
            'fim': desc.findtext('d:UnitDateFinal', default='', namespaces=ns),
            'certeza': desc.findtext('d:UnitDateFinalCertainty', default='false', namespaces=ns) == 'true'
        },
        'descricao': desc.findtext('d:ScopeContent', default='', namespaces=ns),
        'restricoes': desc.findtext('d:AccessRestrict', default='', namespaces=ns),
        'dimensoes': desc.findtext('d:Dimensions', default='', namespaces=ns),
        'idioma': desc.findtext('d:LangMaterial', default='', namespaces=ns),
        'url': desc.findtext('d:IdentifierUrl', default='', namespaces=ns),
    }

def prettyprint_yaml(records, name):
    output_file= f'./prettyprintXML/prettyprintXML_{name}.yaml'
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(records, f, allow_unicode=True, sort_keys=False)

def main():
    arquivo = ['./arquivoOAI/alberto_sampaio_archeevo.xml', './arquivoOAI/ponteDeLima.xml']
    names = ['AS', 'PL']
    i = 0
    for a in arquivo:
        tree = ET.parse(a)  
        root = tree.getroot()

        records = []
        for record in root.findall('oai:record', {
            'oai': 'http://www.openarchives.org/OAI/2.0/'
        }):
            try:
                parsed = parse_record(record)
                records.append(parsed)
            except Exception as e:
                print("Erro ao processar um registo:", e)

        prettyprint_yaml(records, names[i])
        i += 1

if __name__ == "__main__":
    main()
