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


def link_detalhe(item_id, texto):
    """Link para a página de detalhe do título (mesma aba, como o menu)."""
    try:
        numero = int(item_id)
    except (TypeError, ValueError):
        return texto
    return f'<a href="?p=item&amp;id={numero}" target="_self">{texto}</a>'


def card_html(item, par=None):
    """HTML de um card: capa com alt, título com link para o detalhe, descrição, selo do tipo e, se houver, a obra no outro formato."""
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
    nome = link_detalhe(item.get("id"), titulo) if item.get("id") is not None else titulo
    # Título com role="heading" em vez de <h3>: o st.markdown põe um link "Link to heading" em todo h1-h6,
    # e eram 30 paradas a mais no Tab (#19)
    return (
        f'<article class="card">{capa}<div><div class="titulo-card" role="heading" aria-level="3">{nome}</div>'
        f'<p>{descricao}</p>{extra}</div>'
        f'<span class="{classe}">{tipo}</span></article>'
    )


def detalhe_html(item, par=None):
    """HTML da página de detalhe: capa, tipo, categoria, descrição e link para a obra no outro formato."""
    titulo = html.escape(str(item.get("titulo", "")))
    descricao = html.escape(str(item.get("descricao", "")))
    tipo = "Livro" if item.get("tipo") == "Livro" else "Filme"
    categoria = html.escape(str(item.get("categoria", "")))
    src = imagem_data_uri(item.get("imagem") or "")
    capa = f'<img class="capa" src="{src}" alt="Capa de {titulo}">' if src else ""
    extra = ""
    if par:
        formato = "livro" if par.get("tipo") == "Livro" else "filme"
        nome_par = html.escape(str(par.get("titulo", "")))
        extra = f'<p class="adaptacao">Também em {formato}: {link_detalhe(par.get("id"), nome_par)}</p>'
    return (
        f'<article class="detalhe">{capa}<div><dl>'
        f'<dt>Tipo</dt><dd>{tipo}</dd><dt>Categoria</dt><dd>{categoria}</dd></dl>'
        f'<p>{descricao}</p>{extra}</div></article>'
    )


# Fim de render.py
