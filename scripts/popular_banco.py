"""Recria database/cine_livro.db a partir de scripts/itens.json (funciona de qualquer pasta; antes procurava itens.json na raiz)."""
import json
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
JSON = Path(__file__).resolve().parent / "itens.json"
DB = RAIZ / "database" / "cine_livro.db"
CAMPOS = ("titulo", "descricao", "imagem", "tipo", "categoria")


def carregar(caminho=JSON):
    """Lê e valida os itens: campos obrigatórios, tipo Filme/Livro e imagem existente."""
    itens = json.loads(Path(caminho).read_text(encoding="utf-8"))
    erros = []
    for n, item in enumerate(itens, 1):
        faltando = [c for c in CAMPOS if not str(item.get(c, "")).strip()]
        if faltando:
            erros.append(f"item {n}: faltando {', '.join(faltando)}")
        elif item["tipo"] not in ("Filme", "Livro"):
            erros.append(f"item {n}: tipo inválido '{item['tipo']}'")
        elif not (RAIZ / item["imagem"]).is_file():
            erros.append(f"item {n}: imagem não encontrada {item['imagem']}")
    if erros:
        raise ValueError("itens.json inválido:\n" + "\n".join(erros))
    return itens


def popular(itens, destino=DB):
    """Recria a tabela e insere os itens em uma transação."""
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(destino) as conn:
        conn.execute("DROP TABLE IF EXISTS itens")
        conn.execute(
            "CREATE TABLE itens (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, descricao TEXT NOT NULL,"
            " imagem TEXT NOT NULL, tipo TEXT NOT NULL CHECK (tipo IN ('Filme','Livro')), categoria TEXT NOT NULL)"
        )
        conn.execute("CREATE INDEX idx_itens_tipo_categoria ON itens (tipo, categoria)")
        conn.executemany(
            "INSERT INTO itens (titulo, descricao, imagem, tipo, categoria) VALUES (?, ?, ?, ?, ?)",
            [tuple(i[c] for c in CAMPOS) for i in itens],
        )
    return len(itens)


if __name__ == "__main__":
    total = popular(carregar())
    print(f"Banco gerado em {DB.relative_to(RAIZ)} com {total} itens.")
# Fim de popular_banco.py
