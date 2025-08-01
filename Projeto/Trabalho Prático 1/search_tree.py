import json
import os
import sqlite3
import argparse
import sys

def load_json_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File {filename} contains invalid JSON.")
        return None

def create_sqlite_db(json_file, db_file="tree_search.db"):
    try:
        node_info = load_json_data(json_file)
        if not node_info:
            return False
            
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute('DROP TABLE IF EXISTS nodes')
        cursor.execute('''
        CREATE TABLE nodes (
            node_id TEXT PRIMARY KEY,
            title TEXT,
            type TEXT,
            link TEXT,
            scopeContent TEXT,
            useRestrict TEXT,
            term TEXT,
            bioHist TEXT,
            custodHist TEXT,
            geogName TEXT,
            content TEXT
        )
        ''')

        cursor.execute('DROP TABLE IF EXISTS nodes_fts')
        cursor.execute('''
        CREATE VIRTUAL TABLE nodes_fts USING fts5(
            node_id, 
            title, 
            type, 
            link,
            scopeContent,
            useRestrict,
            term,
            bioHist,
            custodHist,
            geogName,
            content,
            content='nodes',
            tokenize='porter unicode61'
        )
        ''')

        def normalize(field):
            if isinstance(field, list):
                return " ".join(field)
            return str(field)

        for node_id, info in node_info.items():
            title = info.get('title', '')
            node_type = info.get('type', '')
            link = info.get('link', '')
            scopeContent = normalize(info.get('scopeContent', ''))
            useRestrict = normalize(info.get('useRestrict', ''))
            term = normalize(info.get('term', ''))
            bioHist = normalize(info.get('bioHist', ''))
            custodHist = normalize(info.get('custodHist', ''))
            geogName = normalize(info.get('geogName', ''))

            content = " ".join([
                node_id, title, node_type, scopeContent, useRestrict,
                term, bioHist, custodHist, geogName
            ])

            cursor.execute(
                "INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (node_id, title, node_type, link, scopeContent, useRestrict,
                 term, bioHist, custodHist, geogName, content)
            )

        cursor.execute('''
        INSERT INTO nodes_fts(
            node_id, title, type, link, scopeContent, useRestrict,
            term, bioHist, custodHist, geogName, content
        )
        SELECT node_id, title, type, link, scopeContent, useRestrict,
               term, bioHist, custodHist, geogName, content
        FROM nodes
        ''')

        conn.commit()
        conn.close()
        
        print(f"SQLite database created successfully at {db_file}")
        return True
    except Exception as e:
        print(f"Error creating SQLite database: {e}")
        return False


def search_with_sqlite(search_term, db_file="tree_search.db"):
    try:
        if not os.path.exists(db_file):
            print(f"Error: SQLite database {db_file} not found.")
            return []
            
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = f'''
        SELECT node_id, title, type, link
        FROM nodes_fts
        WHERE nodes_fts MATCH ?
        ORDER BY rank
        '''
        
        cursor.execute(query, (search_term,))
        results = cursor.fetchall()
        
        formatted_results = []
        for row in results:
            node_id = row['node_id']
            title = row['title']
            node_type = row['type']
            link = row['link']
            
            result = f"Node {node_id}: {title}"
            if node_type:
                result += f" ({node_type})"
            if link:
                result += f" - Link: {link}"
            formatted_results.append(result)
        
        conn.close()
        return formatted_results
    except Exception as e:
        print(f"Error searching with SQLite: {e}")
        return []

def display_results(results, search_term):
    if not results:
        print(f"No results found for '{search_term}'.")
        return
        
    print(f"\nSearch results for '{search_term}':")
    print("-" * 60)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")
    
    print("-" * 60)
    print(f"Found {len(results)} results.\n")

def main():
    parser = argparse.ArgumentParser(description="Search tree data using SQLite FTS5.")
    parser.add_argument("search_term", help="Term to search for")
    parser.add_argument("--json-file", "-j", default="./save_data/nodes_info_AS.json",
                        help="Path to the JSON file containing node information")
    parser.add_argument("--db-file", "-d", default="tree_search.db",
                        help="Path to the SQLite database file")
    parser.add_argument("--create-db", "-c", action="store_true",
                        help="Create/update the SQLite database before searching")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.json_file):
        print(f"Error: JSON file {args.json_file} not found.")
        sys.exit(1)
    
    if args.create_db or not os.path.exists(args.db_file):
        print("Creating/updating SQLite database...")
        if not create_sqlite_db(args.json_file, args.db_file):
            sys.exit(1)
    
    results = search_with_sqlite(args.search_term, args.db_file)
    
    display_results(results, args.search_term)

if __name__ == "__main__":
    main()