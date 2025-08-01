# Relatório TP1 - SPLN

Neste relatório, apresentamos e explicamos todos os scripts desenvolvidos como parte do trabalho prático para o projeto de SPLN (Scripting no Processamento de Linguagem Natural). O objetivo dos scripts é extrair, processar, organizar e realizar buscas eficientes sobre dados arquivísticos em formato XML e JSON, originários de repositórios OAI-PMH e outros arquivos relacionados.

## Objetivos Gerais

O objetivo principal é demonstrar o uso de técnicas de processamento de dados estruturados e semi-estruturados (como XML e JSON), com foco na extração de informação útil, como biografias, entidades (pessoas e lugares) e hierarquias arquivísticas. Através de diversos scripts em Python, conseguimos criar bases de dados estruturadas, processar metadados e gerar relatórios e páginas Wiki para consultas futuras.

A seguir, será apresentada uma descrição detalhada dos scripts desenvolvidos, as suas funcionalidades e a forma como eles contribuem para o processo geral.

---

# Script getXML.py - Download de Registos OAI-PMH

Este script em Python permite descarregar registos no formato XML de um repositório OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting), utilizando o endpoint dos diferentes arquivos.

## O que o script faz

1. **Conecta-se ao endpoint OAI-PMH**: Usa o verbo `ListRecords` para obter registos no formato de metadados `aif`.
2. **Lida com paginação automática**: Utiliza o `resumptionToken` fornecido pela API para continuar a recolher dados até que todos os registos sejam obtidos.
3. **Extrai e guarda os registos**: Todos os registos são guardados num ficheiro XML chamado `alberto_sampaio_archeevo.xml`.

# Análise dos Campos encontrados no XML

## 1. `record_id`

- Representa o identificador único de um registo dentro do sistema.
- No XML, é encontrado dentro de `<ID>`.
- Exemplo:
  ```xml
  <ID>100146</ID>
  ```

## 2. `parent`

- Indica o ID do elemento pai imediato.
- No XML, está dentro de `<Parent>`.
- Representa a relação hierárquica direta com outro registo.
- Exemplo:
  ```xml
  <Parent>99411</Parent>
  ```

## 3. `root_parent`

- No XML, está dentro de `<RootParent>`.
- Representa a secção ou unidade arquivística maior que engloba o registo.
- Exemplo:
  ```xml
  <RootParent>60695</RootParent>
  ```

## 4. `type`

- Representa o nível de descrição do registo.
- No XML, está dentro de `<DescriptionLevel>`.
- Tipos:
  - F (fundo)
  - SC (secção)
  - SSC (subsecção)
  - SR (Série)
  - UI (unidade de instalação)
  - D DC (documento, documento composto)
- Exemplo:
  ```xml
  <DescriptionLevel>UI</DescriptionLevel>
  ```

## Resumo das Relações

```
RootParent (60695)
│
├── Parent (99411)
│   ├── Record_ID (100146) - Type: UI
│
├── Parent (99257)
│   ├── Record_ID (100191) - Type: SSR
```

- `RootParent` define a grande categoria.
- `Parent` estabelece agrupamentos intermediários.
- `Record_ID` representa os elementos individuais.
- `Type` indica a natureza do registo.

# Script `prettyprint_xml.py`

Tem como objetivo **extrair e formatar informação arquivística** contida em ficheiros XML (provenientes de um sistema OAI-PMH), e guardá-la em ficheiros YAML legíveis.

## O que faz o script?

1. **Lê ficheiros XML com registos arquivísticos.**
   - São analisados dois ficheiros:
     - `alberto_sampaio_archeevo.xml`
     - `ponteDeLima.xml`

2. **Extrai campos relevantes de cada registo XML.**
   - Cada registo (`record`) contém metadados descritivos.
   - São extraídos os seguintes campos:
     - `id`: Identificador do registo
     - `titulo`: Título da unidade
     - `tipo_titulo`: Tipo de título
     - `repo`: Repositório de arquivo
     - `data`: Datas de início e fim (e certeza da data)
     - `descricao`: Conteúdo da unidade
     - `restricoes`: Restrições de acesso
     - `dimensoes`: Dimensões físicas
     - `idioma`: Idioma do conteúdo
     - `url`: Ligação para o registo online

3. **Converte os dados extraídos para formato YAML.**
   - O resultado é guardado num ficheiro `.yaml` dentro da pasta `./prettyprintXML/`
   - Os ficheiros têm o nome:  
     - `prettyprintXML_AS.yaml`  
     - `prettyprintXML_PL.yaml`


## Estrutura dos Ficheiros de Saída

Cada ficheiro YAML contém uma lista de registos com a seguinte estrutura:

```yaml
- id: "12345"
  titulo: "Exemplo de Título"
  tipo_titulo: "Oficial"
  repo: "Arquivo X"
  data:
    inicio: "1890"
    fim: "1900"
    certeza: true
  descricao: "Descrição do conteúdo."
  restricoes: "Sem restrições"
  dimensoes: "30x20cm"
  idioma: "Português"
  url: "http://exemplo.pt/registo/12345"
```

# Script `generate_zim_wiki.py`

Este script em Python tem como objetivo **gerar páginas em formato Wiki Zim** a partir de informações armazenadas em ficheiros JSON. As páginas Zim são organizadas numa estrutura hierárquica, com base nos dados contidos nos ficheiros JSON.

## Estrutura das Páginas Zim

Cada página Zim gerada tem a seguinte estrutura:

```plaintext
= 12345 =
**Tipo**: Secção
**Título**: Arquivo Histórico
```

# Parser de Registos OAI-PMH para Estrutura Arquivística (parser.py)

Este script em Python lê e processa ficheiros XML provenientes de um repositório OAI-PMH, extraindo os metadados e construindo uma representação em árvore da estrutura arquivística.

---

## O que o script faz

1. **Lê ficheiros XML OAI-PMH**: São processados ficheiros com registos arquivísticos em formato XML, extraídos previamente.
2. **Extrai e organiza os dados**: A informação é organizada num dicionário de nós (nodos), hierarquias pai-filho e conjuntos de “RootParent”.
3. **Constrói uma árvore arquivística**: A função `getDirectoryTree` transforma a estrutura hierárquica em árvore, representando a relação entre secções, séries e unidades documentais.
4. **Guardar os ficheiros que não têm pai válido**: Guardamos os ficheiros que têm um pai que não existe no arquivo analisado.
5. **Guarda os resultados**: Exporta os dados em formato `.json` para posterior análise.

---

## Estrutura dos dados extraídos

- `nodes`: Dicionário com informação de cada registo (ID, título, link, termos, etc.).
- `hierarchy`: Dicionário com relações pai → [filhos].
- `root_parents`: Conjunto com os identificadores dos elementos de topo na hierarquia.
---

## Função `getDirectoryTree`

Esta função é a chave para construir a **estrutura arquivística em árvore**, a mesma simula como um arquivo físico estaria organizado hierarquicamente.

### Como funciona:

1. **Itera pelos `root_parents`**:
   - Cada `root_parent` representa uma secção principal (por exemplo: um fundo documental).
   - Cria um nó base no `directory_tree`.

2. **Adiciona filhos diretos**:
   - Os filhos diretos do `root_parent` são adicionados como primeiros descendentes (nível 1 da árvore).

3. **Navegação recursiva**:
   - Com o apoio da função auxiliar `add_son_to_node`, percorre-se recursivamente os filhos de cada nó.
   - Estes filhos vão sendo inseridos no campo `'sons'` do respetivo pai.

4. **Evita loops ou repetições**:
   - A estrutura em conjuntos (`current_parents`, `new_parents`) assegura que não se percorre duas vezes o mesmo nível.

### Exemplo simplificado de estrutura final:

```json
{
  "78502": {
    "sons": [
      {
        "node": "78510",
        "sons": [
          {
            "node": "78511",
            "sons": []
          }
        ]
      }
    ]
  }
}
```


## Script `search_tree.py`

Este script permite procurar e visualizar informações a partir de uma base de dados SQLite que contém dados extraídos de um ficheiro JSON. Ele usa a funcionalidade de Full-Text Search (FTS) do SQLite para realizar procuras eficientes.

### Funcionalidades:
1. **Carregar Dados JSON**: A função `load_json_data` lê e carrega dados de um ficheiro JSON.

2. **Criar Base de Dados SQLite**: A função `create_sqlite_db` cria uma base de dados SQLite, onde:
   - Uma tabela chamada `nodes` é criada para armazenar informações sobre os nós.
   - Uma tabela de texto virtual `nodes_fts` é criada para permitir procuras rápidas através do FTS5.
   - Os dados do ficheiro JSON são normalizados e inseridos nessas tabelas.

3. **Procurar na Base de Dados**: A função `search_with_sqlite` permite realizar uma procura no índice FTS da base de dados, retornando os nós que correspondem ao termo de pesquisa fornecido.

4. **Mostrar Resultados**: A função `display_results` exibe os resultados da procura de forma formatada, indicando o número de resultados encontrados.

5. **Execução Principal (Função `main`)**:
   - Usa o `argparse` para permitir a passagem de parâmetros através da linha de comandos.
   - Verifica se o ficheiro JSON existe e, se necessário, cria ou atualiza a base de dados SQLite.
   - Realiza a busca e exibe os resultados.


### Como Utilizar o Script de Procura (search_tree.py)

#### Configuração Inicial:

```shell
python3 search_tree.py "termo de procura" --create-db
```

Este comando cria a base de dados SQLite com o índice FTS5 a partir dos dados JSON (saved_data/nodes_info_AS.json, como ficheiro padrão).

#### Pesquisas Subsequentes:

```shell
python3 search_tree.py "termo de procura"
```

#### Opções Adicionais:

- `--json-file` ou `-j`: Especifica um caminho diferente para o ficheiro JSON.
- `--db-file` ou `-d`: Especifica um caminho diferente para o ficheiro da base de dados SQLite.

# Script `extract_biographies.py`

Este script em Python tem como objetivo **extrair biografias** de pessoas de um conjunto de dados e gerar um novo ficheiro JSON com essas informações. Ele faz uso da biblioteca **spaCy** para processar e identificar nomes de pessoas e também da biblioteca **unidecode** para garantir a ordenação correta dos nomes.

## O que o script faz?

1. **Carrega Dados de Ficheiro JSON**:
   - O script carrega um ficheiro JSON contendo dados sobre vários nós (pode ser um arquivo como `nodes_info_AS.json` ou `nodes_info_PL.json`).

2. **Extrai Nomes e Biografias**:
   - Para cada nó no ficheiro JSON, o script tenta extrair o nome da pessoa e a sua biografia.
   - A extração é feita considerando o título (campo `title`) e a biografia (campo `bioHist`) do nó.
   - O script verifica se o título é um nome válido e se a biografia contém informações que indicam uma pessoa (ex: "nasceu", "morreu", etc.).

3. **Verificação de Nome**:
   - O script usa a biblioteca **spaCy** com um modelo de língua portuguesa (`pt_core_news_lg`) para verificar se o nome extraído é uma pessoa. Ele valida o nome usando a etiquetagem de entidades do modelo (classe "PER" para pessoas).
   - Se o nome for válido e for uma pessoa, o nome e a biografia são armazenados.

4. **Armazenamento das Biografias**:
   - As biografias extraídas são armazenadas num dicionário, onde o nome da pessoa é a chave e a biografia é o valor.
   - Se houver várias entradas para a mesma pessoa, o script mantém a biografia mais longa, presumindo que seja a mais completa.

5. **Ordenação e Gravação**:
   - As biografias são ordenadas por nome (usando a função `unidecode` para garantir que a ordenação não seja afetada por caracteres especiais).
   - O resultado final é guardado num ficheiro JSON chamado `people_biographies_{name}.json`.

## Estrutura de Dados

O ficheiro de saída (`people_biographies_{name}.json`) terá a seguinte estrutura:

```json
{
  "Nome da Pessoa": "Biografia da pessoa.",
  "Outro Nome": "Outra biografia."
}
```

# Scripts `extracted_entities_AS.py` e `extracted_entities_PL.py`

## Objetivo
Ambos os scripts têm como objetivo **extrair informações sobre pessoas (nomes e duas profissões caso existam) e lugares** de ficheiros JSON contendo dados de diferentes arquivos. As informações extraídas são guardadas em novos ficheiros JSON.

## Principais Funções

##### Função **extrair_info_formatada(title, scope_content, biogHist)**

- Esta função é responsável por extrair informações como nomes de pessoas (usando o modelo **spaCy** para detecção de entidades) e lugares a partir dos textos fornecidos (título, conteúdo do escopo e biografia).

- As profissões, freguesias e moradas são extraídas com expressões regulares.

- A função usa um conjunto de regras para detectar profissões, lugares e pessoas (por exemplo, "Profissão:", "Freguesia:", "Morada:").

- Também usamos o **spacy** para identificar os lugares do tipo "LOC", que existem para além das já identificadas. 
- Para cada pessoa identificada, a função tenta associá-la a uma profissão.

### Script **`extracted_entities_PL.py`**

##### Função extrair_info_formatada(scope_content):

- Esta função é semelhante à função *extrair_info_formatada* do primeiro script, mas neste caso, ela trabalha apenas com o campo scopeContent para extrair nomes de pessoas e lugares.

- Ela usa o modelo **spaCy** para identificar entidades do tipo "PER" (pessoas) e "LOC" (lugares).

- Além disso, tenta identificar profissões associadas a pessoas a partir do texto scopeContent.

## Por que dois scripts separados?

1. **Fontes de Dados Diferentes**: Cada script processa um ficheiro diferente (`AS` e `PL`), tem as informações relativas às profissões com formatos e estruturas de dados que leva a necessidade de ter abordagens diferentes para cada um.
2. **Requisitos Específicos**: Os campos e as informações que cada ficheiro tem para extrair as profissões exigem diferentes abordagens de extração.

# Script `generateHTML.py` 

Para gerar um site de visualização hierárquica de dados, como documentos e fundos, utilizando arquivos JSON como fonte de dados. O site permite filtrar informações, visualizar a árvore hierárquica e aceder páginas específicas sobre entidades e registros.

## Funções

### 1. **`create_directory(directory)`**
Cria uma diretoria se ela não existir.

### 2. **`build_base_html(title, content, active_page="home")`**
Cria a estrutura básica do HTML com um título, conteúdo e uma navegação lateral. A navegação inclui links para as páginas "Página Inicial", "Bibliografias" e "Sobre".

### 3. **`create_bibliographies_page(output_dir, bibliographies_dict)`**
Gera a página de bibliografias, com uma tabela que contém entidades e as suas respectivas biografias, e a guarda como `bibliografias.html`.

### 4. **`build_tree_html(tree_dict, node_info_dict, filter_type=None)`**
Cria a estrutura HTML para a árvore hierárquica de registros. Utiliza um filtro opcional para exibir apenas registros de um tipo específico.

### 5. **`build_node_html(node_data, node_info_dict, filter_type=None, level=2)`**
Cria o HTML para um único nó da árvore e os seus filhos, recursivamente.

### 6. **`create_record_page(output_dir, record_id, record_info, entidade)`**
Cria uma página HTML para um registro específico, incluindo detalhes como pessoas associadas, lugares, termos e outras informações relacionadas.

### 7. **`create_about_page(output_dir)`**
Cria a página "Sobre o Projeto", que explica o propósito do site e como usá-lo.

## Processamento

- O código começa por carregar dados de ficheiros JSON (`nodes_info`, `directory_tree`, `people_biographies`, e `extracted_entities`).
- De seguida, ele cria páginas HTML individuais para cada registro, exibindo informações relacionadas (como pessoas, lugares, termos).
- O site inclui uma árvore hierárquica que é exibida como uma lista expansível.

# Constituição do Grupo

- **Mariana Silva - PG55980**
- **João Coelho - PG55954**
- **José Rodrigues - PG55969**




