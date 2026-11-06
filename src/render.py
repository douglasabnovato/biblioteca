"""Geração do HTML dos cards com escape de conteúdo (título e descrição não viram HTML)."""
import base64
import html
import mimetypes
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=256)
def imagem_data_uri(caminho):
    """Converte a capa local em data URI para usar com texto alternativo; devolve '' se o arquivo não existir."""
    arquivo = (RAIZ / str(caminho)).resolve()
    if RAIZ not in arquivo.parents or not arquivo.is_file():
        return ""
    tipo = mimetypes.guess_type(arquivo.name)[0] or "image/jpeg"
    return f"data:{tipo};base64,{base64.b64encode(arquivo.read_bytes()).decode()}"


def card_html(item, par=None):
    """HTML de um card: capa com alt, título, descrição, selo do tipo e, se houver, a obra no outro formato."""
    titulo = html.escape(str(item.get("titulo", "")))
    descricao = html.escape(str(item.get("descricao", "")))
    tipo = "Livro" if item.get("tipo") == "Livro" else "Filme"
    classe = "badge livro" if tipo == "Livro" else "badge"
    src = imagem_data_uri(item.get("imagem") or "")
    capa = f'<img class="capa" src="{src}" alt="Capa de {titulo}" loading="lazy">' if src else ""
    extra = ""
    if par:
        formato = "livro" if par.get("tipo") == "Livro" else "filme"
        extra = f'<p class="adaptacao">Também em {formato}: {html.escape(str(par.get("titulo", "")))}</p>'
    return (
        f'<article class="card">{capa}<div><h3>{titulo}</h3><p>{descricao}</p>{extra}</div>'
        f'<span class="{classe}">{tipo}</span></article>'
    )
# Fim de render.py
