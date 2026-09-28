"""Acesso ao catálogo em SQLite: busca por tipo, categoria e título (sem diferenciar acentos e maiúsculas)."""
import sqlite3
import unicodedata
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "cine_livro.db"


def normalizar(texto):
    """Remove acentos e passa para minúsculas (ex.: "Ficção" -> "ficcao")."""
    sem_acento = unicodedata.normalize("NFD", str(texto or ""))
    return "".join(c for c in sem_acento if unicodedata.category(c) != "Mn").lower().strip()


def conectar(db_path=DB_PATH):
    """Abre o banco em modo leitura com a função normalizar disponível no SQL."""
    conn = sqlite3.connect(f"file:{Path(db_path).as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    conn.create_function("normalizar", 1, normalizar, deterministic=True)
    return conn


def buscar_dados(tipo=None, categoria=None, busca=None, db_path=DB_PATH):
    """Lista itens filtrando por tipo (Filme/Livro), categoria e trecho do título, em ordem alfabética."""
    query = "SELECT id, titulo, descricao, imagem, tipo, categoria FROM itens WHERE 1=1"
    params = []
    if tipo and tipo != "Home":
        query += " AND tipo = ?"
        params.append(tipo)
    if categoria and categoria != "Todas":
        query += " AND categoria = ?"
        params.append(categoria)
    termo = normalizar(busca)[:80]
    if termo:
        query += " AND normalizar(titulo) LIKE ? ESCAPE '\\'"
        params.append("%" + termo.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%")
    query += " ORDER BY categoria, titulo"
    with conectar(db_path) as conn:
        return [dict(row) for row in conn.execute(query, params).fetchall()]


def listar_categorias(tipo=None, db_path=DB_PATH):
    """Categorias existentes no catálogo (antes a lista ficava fixa no código)."""
    query = "SELECT DISTINCT categoria FROM itens"
    params = []
    if tipo and tipo != "Home":
        query += " WHERE tipo = ?"
        params.append(tipo)
    with conectar(db_path) as conn:
        return [r[0] for r in conn.execute(query + " ORDER BY categoria", params).fetchall()]
# Fim de backend.py
