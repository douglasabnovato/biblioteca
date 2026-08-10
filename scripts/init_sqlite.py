import sqlite3
import json
import os

def create_database():
    # 1. Conectar ao banco (se não existir, o SQLite cria o arquivo .db)
    if not os.path.exists('database'):
        os.makedirs('database')
        
    conn = sqlite3.connect('database/cine_livro.db')
    cursor = conn.cursor()

    # 2. Criar a tabela baseada nos seus dados
    cursor.execute('DROP TABLE IF EXISTS itens') # Limpa se já existir
    cursor.execute('''
        CREATE TABLE itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            imagem TEXT,
            tipo TEXT,
            categoria TEXT
        )
    ''')

    # 3. Carregar dados do seu JSON para o SQLite
    try:
        with open("itens.json", "r", encoding="utf-8") as f:
            itens_brutos = json.load(f)
            
        for item in itens_brutos:
            cursor.execute('''
                INSERT INTO itens (titulo, descricao, imagem, tipo, categoria)
                VALUES (?, ?, ?, ?, ?)
            ''', (item['titulo'], item['descricao'], item['imagem'], item['tipo'], item['categoria']))
            
        conn.commit()
        print("✅ Banco de dados SQLite gerado com sucesso em 'database/cine_livro.db'!")
        print(f"✅ {len(itens_brutos)} itens importados.")
        
    except FileNotFoundError:
        print("❌ Erro: O arquivo 'itens.json' não foi encontrado.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()