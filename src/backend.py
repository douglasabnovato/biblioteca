import sqlite3

def buscar_dados(tipo=None, categoria=None, busca=None):
    conn = sqlite3.connect('database/cine_livro.db')
    # Permite acessar colunas pelo nome como um dicionário
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    query = "SELECT * FROM itens WHERE 1=1"
    params = []

    if tipo and tipo != "Home":
        query += " AND tipo = ?"
        params.append(tipo)
    
    if categoria and categoria != "Todas":
        query += " AND categoria = ?"
        params.append(categoria)
    
    if busca:
        query += " AND titulo LIKE ?"
        params.append(f"%{busca}%")

    cursor.execute(query, params)
    res = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return res