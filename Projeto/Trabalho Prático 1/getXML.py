import requests
import xml.etree.ElementTree as ET

OAI_BASE_URL = "https://pesquisa-arquivo.cm-pontedelima.pt/OAI-PMH/"
METADATA_PREFIX = "aif" 

def fetch_records(resumption_token=None):
    params = {"verb": "ListRecords", "metadataPrefix": METADATA_PREFIX}

    if resumption_token:
        params = {"verb": "ListRecords", "resumptionToken": resumption_token}
    
    response = requests.get(OAI_BASE_URL, params=params)
    response.encoding = 'utf-8'
    response.raise_for_status()
    
    
    return response.text

def parse_response(xml_data):
    root = ET.fromstring(xml_data)
    ns = {"oai": "http://www.openarchives.org/OAI/2.0/"}

    records = root.findall(".//oai:record", ns)
    records_data = [ET.tostring(record, encoding="unicode") for record in records]

    resumption_token_elem = root.find(".//oai:resumptionToken", ns)
    resumption_token = resumption_token_elem.text if resumption_token_elem is not None else None

    return records_data, resumption_token

def download_oai_records():
    resumption_token = None
    all_records = []

    while True:
        xml_response = fetch_records(resumption_token)
        records, resumption_token = parse_response(xml_response)
        all_records.extend(records)

        print(f"Baixados {len(records)} registros. Token: {resumption_token}")

        if not resumption_token:
            break 

    with open("alberto_sampaio_archeevo.xml", "w", encoding="utf-8") as f:
        f.write("<OAIRecords>\n" + "\n".join(all_records) + "\n</OAIRecords>")

    print(f"Download completo! Total de registros: {len(all_records)}")

if __name__ == "__main__":
    download_oai_records()
