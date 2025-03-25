import re 
import requests
import shelve 
import jjcli
from bs4 import BeautifulSoup as bs

d = shelve.open("pagecache.db")


# ir buscar a página
def myget(url):
    if url not in d:
        print(f".............. getting {url}")
        txt = requests.get(url).text
        d[url] = txt
    return d[url] 

def buscar_info_artigo(url):
    response = myget(url)
    soup = bs(response, "html.parser")


    titulo = soup.find("meta", property="og:title")
    if titulo and "content" in titulo.attrs:
        conteudo_titulo = titulo["content"].strip()
    else:
        conteudo_titulo = "sem_titulo"
    
    descricao = soup.find("meta", property="og:description")
    if descricao and "content" in descricao.attrs:
        conteudo_desc = descricao["content"].strip()
    else:
        conteudo_desc = "Sem descrição"

    artigo = soup.find("article")
    conteudo_artigo = artigo.get_text("\n").strip() if artigo else "No Article Found"

    nome_ficheiro = url.replace("http://", "").replace("https://", "").replace("/", "_") + ".txt"
    print(conteudo_titulo)
    
    with open(nome_ficheiro, "w", encoding="utf-8") as f:
        f.write(f"Título: {conteudo_titulo}\n")
        f.write(f"Descrição: {conteudo_desc}\n\n")
        f.write("Conteúdo do artigo:\n")
        f.write(conteudo_artigo)

def obter_urls_ficheiros(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = bs(response.text, "html.parser")

    links = soup.find_all("a")

    urls_ficheiros = [url + link.get("href") for link in links if link.get("href") and not link.get("href").startswith("?") and not link.get("href").startswith("/")]

    return urls_ficheiros

url_base = "https://natura.di.uminho.pt/~jj/bs4/folha8-2023/"
urls = obter_urls_ficheiros(url_base)


for url in urls:
    buscar_info_artigo(url)
    

d.close()