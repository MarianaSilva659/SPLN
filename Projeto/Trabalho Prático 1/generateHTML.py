import json
import os
from pathlib import Path

def load_dict_from_file(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        return json.load(file)

def create_directory(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)

def build_base_html(title, content, active_page="home"):
    """Build the base HTML template with sidebar and navigation"""
    html = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="styles.css">
        <style>
            .search-container {{
                margin-bottom: 20px;
                padding: 0 10px;
            }}
            
            #termSearch {{
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 5px;
            }}
            
            #termSearch:focus {{
                outline: none;
                border-color: var(--accent-color);
                box-shadow: 0 0 3px rgba(0,0,0,0.2);
            }}
        </style>
        <script>
            function toggleChildren(element) {{
                const childrenList = element.parentElement.querySelector('ul');
                if (childrenList) {{
                    childrenList.classList.toggle('hidden');
                    const toggleIcon = element;
                    if (toggleIcon) {{
                        toggleIcon.textContent = childrenList.classList.contains('hidden') ? '▶' : '▼';
                    }}
                }}
            }}
            
            function toggleMobileSidebar() {{
                if (window.innerWidth <= 768) {{
                    document.getElementById('sidebar').classList.toggle('mobile-open');
                }}
            }}
            
            function changeBackgroundColor() {{
                const colors = [
                    'var(--bg-color-1)',
                    'var(--bg-color-2)',
                    'var(--bg-color-3)'
                ];
                let currentIndex = 0;
                
                setInterval(() => {{
                    document.body.style.backgroundColor = colors[currentIndex];
                    currentIndex = (currentIndex + 1) % colors.length;
                }}, 10000); // Change every 10 seconds
            }}

            function searchByTerm() {{
                const searchTerm = document.getElementById('termSearch').value.toLowerCase();
                const allNodes = document.querySelectorAll('.node');
                
                if (searchTerm === '') {{
                    allNodes.forEach(node => {{
                        node.style.display = '';
                        const childList = node.querySelector('ul');
                        if (childList) {{
                            childList.classList.remove('hidden');
                        }}
                    }});
                    return;
                }}
                
                // First hide all nodes
                allNodes.forEach(node => {{
                    node.style.display = 'none';
                }});
                
                const matchingNodes = document.querySelectorAll(`[data-terms*="${{searchTerm}}"]`);
                matchingNodes.forEach(node => {{
                    node.style.display = '';
                    
                    // Show all parent nodes
                    let parent = node.parentElement;
                    while (parent && !parent.classList.contains('tree')) {{
                        if (parent.classList.contains('node')) {{
                            parent.style.display = '';
                        }}
                        if (parent.tagName === 'UL') {{
                            parent.classList.remove('hidden');
                        }}
                        parent = parent.parentElement;
                    }}
                }});
            }}
            
            window.onload = function() {{
                changeBackgroundColor();
            }};
        </script>
    </head>
    <body>
        <div class="page-container">
            <!-- Sidebar -->
            <div id="sidebar">
                <div class="sidebar-header">
                    <h2>Filtros</h2>
                    <button class="mobile-close-btn" onclick="toggleMobileSidebar()">×</button>
                </div>
                <div class="sidebar-content">
                    <div class="search-container">
                        <h3>Pesquisar por Termo</h3>
                        <input type="text" id="termSearch" placeholder="Digite um termo..." onkeyup="searchByTerm()">
                    </div>
                    
                    <h3>Navegação</h3>
                    <ul class="nav-links">
                        <li><a href="index.html" class="{active_page == 'home' and 'active' or ''}">Página Inicial</a></li>
                        <li><a href="bibliografias.html" class="{active_page == 'bibliografias' and 'active' or ''}">Bibliografias</a></li> <!-- Novo botão -->
                        <li><a href="sobre.html" class="{active_page == 'sobre' and 'active' or ''}">Sobre</a></li>
                    </ul>
                </div>
            </div>
            
            <!-- Main Content -->
            <div id="main-content">
                <header>
                    <button class="mobile-menu-btn" onclick="toggleMobileSidebar()">≡</button>
                    <h1>{title}</h1>
                </header>
                <main>
                    {content}
                </main>
                <footer>
                    <p>© 2025 Árvore de Fundos e Documentos</p>
                </footer>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def create_bibliographies_page(output_dir, bibliographies_dict):
    """Create the Bibliografias page with a table of entities and their biographies"""
    # Melhorando o conteúdo da tabela com estilos CSS
    table_content = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f4f4f4;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
    </style>
    <table>
        <tr><th>Entidade</th><th>Bibliografia</th></tr>
    """

    # Adiciona as linhas da tabela com as entidades e biografias
    for entity, biography in bibliographies_dict.items():
        table_content += f"<tr><td>{entity}</td><td>{biography}</td></tr>\n"
    
    table_content += "</table>"

    # Gera o HTML completo com a tabela
    html = build_base_html("Bibliografias", table_content, "bibliografias")
    
    # Salva a página em bibliografias.html
    with open(os.path.join(output_dir, "bibliografias.html"), "w", encoding="utf-8") as file:
        file.write(html)

def build_tree_html(tree_dict, node_info_dict, filter_type=None):
    """Build the tree HTML content with optional filtering"""
    html = '<div class="tree">\n<ul class="root-list">\n'
    
    for root_id, root_data in tree_dict.items():
        root_info = node_info_dict.get(root_id, {})
        root_title = root_info.get("title", f"Raiz {root_id}")
        root_type = root_info.get("type", "")
        
        if filter_type and root_type != filter_type:
            continue
        
        html += f'<li class="node" data-terms="{",".join(root_info.get("term", [])).lower() if isinstance(root_info.get("term", []), list) else str(root_info.get("term", "")).lower()}">\n'
        
        # Changed to link to local HTML file instead of external link
        html += f'<span class="toggle" onclick="toggleChildren(this)">▼</span><span class="node-id">{root_id}:</span><a href="{root_id}.html">{root_title}</a>'
        
        if root_type:
            html += f'<span class="node-info">({root_type})</span>'
        
        if "sons" in root_data and root_data["sons"]:
            html += "\n<ul>\n"
            for child in root_data["sons"]:
                child_html = build_node_html(child, node_info_dict, filter_type)
                if child_html:  # Only add if the node wasn't filtered out
                    html += child_html
            html += "</ul>\n"
        
        html += "</li>\n"
    
    html += "</ul>\n</div>\n"
    return html

def build_node_html(node_data, node_info_dict, filter_type=None, level=2):
    """Build HTML for a single node and its children"""
    node_id = node_data.get("node", "")
    children = node_data.get("sons", [])
    
    node_info = node_info_dict.get(node_id, {})
    node_title = node_info.get("title", f"Nodo {node_id}")
    node_type = node_info.get("type", "")
    
    # Skip if filtering is enabled and this node doesn't match
    if filter_type and node_type != filter_type:
        # Check if any children match the filter
        has_matching_children = False
        for child in children:
            if build_node_html(child, node_info_dict, filter_type, level + 1):
                has_matching_children = True
                break
        
        if not has_matching_children:
            return ""
    
    node_html = f'<li class="node" data-terms="{",".join(node_info.get("term", [])).lower() if isinstance(node_info.get("term", []), list) else str(node_info.get("term", "")).lower()}">\n'
    
    # Changed to link to local HTML file instead of external link
    node_html += f'<span class="toggle" onclick="toggleChildren(this)">▼</span><span class="node-id">{node_id}:</span><a href="{node_id}.html">{node_title}</a>'
    
    if node_type:
        node_html += f'<span class="node-info">({node_type})</span>'
    
    if children:
        node_html += "\n<ul>\n"
        for child in children:
            child_html = build_node_html(child, node_info_dict, filter_type, level + 1)
            if child_html:  
                node_html += child_html
        node_html += "</ul>\n"
    
    node_html += "</li>\n"
    return node_html

def create_record_page(output_dir, record_id, record_info, entidade):
    """Create an individual HTML page for a record"""
    
    # Prepare people section if available
    people_section = ""
    if entidade and "pessoas" in entidade and entidade["pessoas"]:
        people_section = '''
        <div class="record-section record-people">
            <h3><i class="section-icon">👤</i> Pessoas</h3>
            <div class="section-content">
                <ul class="entity-list">'''
        for person in entidade["pessoas"]:
            person_info = f"{person['nome']}"
            if person.get('profissao'):
                people_section += f'<li><span class="entity-name">{person["nome"]}</span> <span class="entity-detail">- {person["profissao"]}</span></li>'
            else:
                people_section += f'<li><span class="entity-name">{person["nome"]}</span></li>'
        people_section += '''
                </ul>
            </div>
        </div>'''
    
    # Prepare places section if available
    places_section = ""
    if entidade and "lugares" in entidade and entidade["lugares"]:
        places_section = '''
        <div class="record-section record-places">
            <h3><i class="section-icon">📍</i> Lugares</h3>
            <div class="section-content">
                <ul class="entity-list">'''
        for place in entidade["lugares"]:
            places_section += f'<li><span class="entity-name">{place}</span></li>'
        places_section += '''
                </ul>
            </div>
        </div>'''
    
    # Prepare terms section if available
    terms_section = ""
    if record_info.get('term') and len(record_info.get('term')) > 0:
        terms_section = '''
        <div class="record-section record-terms">
            <h3><i class="section-icon">🏷️</i> Termos</h3>
            <div class="section-content">
                <ul class="entity-list">'''
        for term in record_info.get('term'):
            terms_section += f'<li><span class="entity-name">{term}</span></li>'
        terms_section += '''
                </ul>
            </div>
        </div>'''
    
    # Add custom CSS for the sections
    custom_css = '''
    <style>
        .record-section {
            margin: 20px 0;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .record-section h3 {
            margin: 0;
            padding: 12px 15px;
            background-color: #f5f5f5;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            align-items: center;
            font-size: 1.1em;
        }
        
        .section-icon {
            margin-right: 8px;
            font-style: normal;
        }
        
        .section-content {
            padding: 15px;
            background-color: #ffffff;
        }
        
        .entity-list {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        
        .entity-list li {
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .entity-list li:last-child {
            border-bottom: none;
        }
        
        .entity-name {
            font-weight: 500;
        }
        
        .entity-detail {
            color: #666;
        }
        
        .record-people h3 {
            background-color: #e8f4f9;
            color: #0277bd;
        }
        
        .record-places h3 {
            background-color: #e8f5e9;
            color: #2e7d32;
        }
        
        .record-terms h3 {
            background-color: #fff8e1;
            color: #ff8f00;
        }
    </style>
    '''
    
    content = f"""
    {custom_css}
    <div class="record-details">
        <h2>{record_info.get('title', f'Registro {record_id}')}</h2>
        
        <div class="record-metadata">
            <p><strong>ID:</strong> {record_id}</p>
            <p><strong>Tipo:</strong> {record_info.get('type', 'N/A')}</p>
            
            {f'<p><strong>ID Pai:</strong> {record_info.get("parent", "N/A")}</p>' if record_info.get('parent') else ''}
            {f'<p><strong>ID Raiz:</strong> {record_info.get("root_parent", "N/A")}</p>' if record_info.get('root_parent') else ''}
            
            {f'<div class="record-content"><h3>Conteúdo:</h3><p>{record_info.get("scopeContent")}</p></div>' if record_info.get('scopeContent') and record_info.get('scopeContent') != "Sem scopeContent" else ''}
            
            {f'<div class="record-restrictions"><h3>Restrições de Uso:</h3><p>{record_info.get("useRestrict")}</p></div>' if record_info.get('useRestrict') and record_info.get('useRestrict') != "Sem useRestrict" else ''}
                        
            {f'<div class="record-biography"><h3>Biografia/História:</h3><p>{record_info.get("bioHist")}</p></div>' if record_info.get('bioHist') and record_info.get('bioHist') != "Sem biografia" else ''}
                        
            {f'<div class="record-geography"><h3>Nome Geográfico:</h3><p>{record_info.get("geogName")}</p></div>' if record_info.get('geogName') and record_info.get('geogName') != "Sem geogName" else ''}

            {people_section}
            
            {places_section}
            
            {terms_section}

            {f'<p><strong>Link Original:</strong> <a href="{record_info.get("link")}" target="_blank">{record_info.get("link")}</a></p>' if record_info.get('link') else ''}
        </div>
        
        <div class="record-navigation">
            <a href="index.html" class="back-button">Voltar para a Árvore</a>
        </div>
    </div>
    """
    html = build_base_html(f"Registro {record_id} - {record_info.get('title', '')}", content)
    
    with open(os.path.join(output_dir, f"{record_id}.html"), "w", encoding="utf-8") as file:
        file.write(html)

def create_about_page(output_dir):
    """Create the About page"""
    about_content = """
    <div class="about-content">
        <h2>Sobre este Projeto</h2>
        <p>Este projeto foi desenvolvido para facilitar a navegação e visualização de fundos e documentos em uma estrutura hierárquica.</p>
        
        <h2>Como Usar</h2>
        <p>Utilize a barra lateral para filtrar o conteúdo ou navegue entre as diferentes páginas do site.</p>
        
        <h2>Funcionalidades</h2>
        <ul>
            <li>Visualização hierárquica de fundos e documentos</li>
            <li>Filtros por termo nos arquivo</li>
            <li>Bibliografias</li>
        </ul>
    </div>
    """
    
    html = build_base_html("Sobre o Projeto", about_content, "sobre")
    
    with open(os.path.join(output_dir, "sobre.html"), "w", encoding="utf-8") as file:
        file.write(html)

def main():
    site = ['siteAlbertoSampaio', 'sitePonteDeLima']
    names = ["AS", "PL"]
    
    i = 0
    for name in names:
        try:
            output_dir = site[i]
            create_directory(output_dir)
            
            node_info_path = f'./save_data/nodes_info_{name}.json'
            tree_path = f'./save_data/directory_tree_{name}.json'
            bibliographies_path = f'./save_data/people_biographies_{name}.json'
            
            node_info_dict = load_dict_from_file(node_info_path)
            tree_dict = load_dict_from_file(tree_path)
            bibliographies_dict = load_dict_from_file(bibliographies_path)
            entities_file_path = f'./save_data/extracted_entities_{name}.json'
            if os.path.exists(entities_file_path):
                    entities_data = load_dict_from_file(entities_file_path)
            # Generate individual record pages
            for record_id, record_info in node_info_dict.items():
                record_entities = entities_data.get(record_id, {})
                create_record_page(output_dir, record_id, record_info, record_entities)
                
            tree_content = build_tree_html(tree_dict, node_info_dict)
            main_html = build_base_html("Árvore de Fundos e Documentos", tree_content, "home")
            
            with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as file:
                file.write(main_html)
            
            create_about_page(output_dir)
            create_bibliographies_page(output_dir, bibliographies_dict)
            
            print(f"✅ Site gerado com sucesso no diretório: {output_dir}")
            print("Arquivos gerados:")
            print("  - index.html (Página principal)")
            print("  - [ID].html (Páginas individuais para cada registro)")
            print("  - sobre.html (Página sobre o projeto)")
            print("  - bibliografias.html (Página de bibliografias)")
            print("  - styles.css (Estilos do site)")
        
        except FileNotFoundError as e:
            print(f"❌ Erro: Arquivo não encontrado - {e}")
            print("Verifique se os arquivos JSON estão no diretório correto.")
        except json.JSONDecodeError as e:
            print(f"❌ Erro: Formato JSON inválido - {e}")
            print("Verifique se os arquivos JSON estão corretamente formatados.")
        except Exception as e:
            print(f"❌ Erro ao processar os dados para '{name}': {e}")
        i += 1
if __name__ == "__main__":
    main()
