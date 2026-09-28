"""Cine&Livro: catálogo de filmes e livros com busca em tempo real, navegação por tipo e filtro por categoria."""
import html

import streamlit as st
from st_keyup import st_keyup

from src.backend import buscar_dados, listar_categorias
from src.render import card_html

st.set_page_config(layout="wide", page_title="Cine&Livro", page_icon="🎬")

with open("src/styles/main.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

PAGINAS = {"Home": "Início", "Filme": "Filmes", "Livro": "Livros"}
navegacao = st.query_params.get("p", "Home")
if navegacao not in PAGINAS:
    navegacao = "Home"


@st.cache_data(ttl=600, show_spinner=False)
def consultar(tipo, categoria, busca):
    """Consulta com cache para não reabrir o banco a cada tecla."""
    return buscar_dados(tipo=tipo, categoria=categoria, busca=busca)


@st.cache_data(ttl=600, show_spinner=False)
def categorias_de(tipo):
    """Categorias do tipo atual, com cache."""
    return listar_categorias(tipo)


ATUAL = 'aria-current="page"'
links = "".join(
    f'<a href="?p={chave}" target="_self" {ATUAL if chave == navegacao else ""}>{rotulo}</a>'
    for chave, rotulo in PAGINAS.items()
)
st.markdown(f'<nav class="nav-custom" aria-label="Principal">{links}</nav><div class="content-wrapper"></div>', unsafe_allow_html=True)

st.title("Cine&Livro" if navegacao == "Home" else f"Cine&Livro — {PAGINAS[navegacao]}")

def campo_busca():
    """Busca em tempo real (st_keyup); se o componente não carregar, usa o campo padrão do Streamlit."""
    try:
        return st_keyup(label="Pesquisar por título", placeholder="Pesquisar por título…", key="search_input", debounce=250)
    except Exception:
        return st.text_input("Pesquisar por título", placeholder="Pesquisar por título…", key="search_fallback")


search = campo_busca()

categoria_sel = "Todas"
if navegacao != "Home":
    categoria_sel = st.selectbox("Filtrar por categoria", ["Todas", *categorias_de(navegacao)])

try:
    itens = consultar(navegacao, categoria_sel, search or "")
except Exception:
    itens = None
    st.error("Não foi possível abrir o catálogo. Gere o banco com: python scripts/popular_banco.py")

st.divider()

if itens:
    st.caption(f"{len(itens)} {'título encontrado' if len(itens) == 1 else 'títulos encontrados'}")
    grupos = {}
    for item in itens:
        grupos.setdefault(item["categoria"], []).append(item)
    for categoria, lista in grupos.items():
        st.subheader(categoria)
        for i in range(0, len(lista), 3):
            cols = st.columns(3)
            for j, item in enumerate(lista[i:i + 3]):
                with cols[j]:
                    st.markdown(card_html(item), unsafe_allow_html=True)
        st.write("---")
elif itens is not None:
    termo = html.escape(search or "")
    st.info(f"Nenhum resultado encontrado{f' para “{termo}”' if termo else ''}.")
# Fim de app.py
