import sqlite3
import json
import os

# Garante que a pasta database existe
os.makedirs('database', exist_ok=True)

# Lê os dados diretamente do arquivo itens.json da raiz
if os.path.exists('itens.json'):
    with open('itens.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
else:
    raise FileNotFoundError("O arquivo itens.json não foi encontrado na raiz do projeto.")

conn = sqlite3.connect('database/cine_livro.db')
cursor = conn.cursor()

# Recria a tabela para garantir que está limpa
cursor.execute('DROP TABLE IF EXISTS itens')
cursor.execute('''
    CREATE TABLE itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descricao TEXT,
        imagem TEXT,
        tipo TEXT,
        categoria TEXT
    )
''')

for item in dados:
    cursor.execute('''
        INSERT INTO itens (titulo, descricao, imagem, tipo, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (item['titulo'], item['descricao'], item['imagem'], item['tipo'], item['categoria']))

conn.commit()
conn.close()
print("Banco de dados populado com sucesso a partir do itens.json!")