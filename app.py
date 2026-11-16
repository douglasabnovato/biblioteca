"""Cine&Livro: catálogo de filmes e livros com busca em tempo real, navegação por tipo e filtro por categoria."""
import html
import os
import time

import streamlit as st
from st_keyup import st_keyup

from src.backend import buscar_dados, buscar_item, listar_categorias, pares_adaptacao
from src.render import card_html, detalhe_html

st.set_page_config(layout="wide", page_title="Cine&Livro", page_icon="🎬")

with open("src/styles/main.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

PAGINAS = {"Home": "Início", "Filme": "Filmes", "Livro": "Livros"}
navegacao = st.query_params.get("p", "Home")
# Só nos testes de tela (#18): atrasa a consulta para o aviso de carregamento aparecer; em produção fica 0
ATRASO_TESTE = min(float(os.environ.get("CINELIVRO_ATRASO_TESTE", "0") or 0), 10)


@st.cache_data(ttl=600, show_spinner=False)
def consultar(tipo, categoria, busca):
    """Consulta com cache para não reabrir o banco a cada tecla."""
    return buscar_dados(tipo=tipo, categoria=categoria, busca=busca)


@st.cache_data(ttl=600, show_spinner=False)
def adaptacoes():
    """Obras que existem como filme e como livro no catálogo, com cache."""
    return pares_adaptacao(buscar_dados())


@st.cache_data(ttl=600, show_spinner=False)
def categorias_de(tipo):
    """Categorias do tipo atual, com cache."""
    return listar_categorias(tipo)


@st.cache_data(ttl=600, show_spinner=False)
def consultar_item(item_id):
    """Um título pelo id, com cache."""
    return buscar_item(item_id)


# Página de detalhe (?p=item&id=N); id inválido ou inexistente volta para o Início com aviso (#7)
detalhe = None
aviso = None
if navegacao == "item":
    try:
        detalhe = consultar_item(st.query_params.get("id", ""))
        if detalhe is None:
            aviso = "Título não encontrado. Veja o catálogo completo abaixo."
    except Exception:
        detalhe = None  # banco indisponível: a lista abaixo mostra o erro
    if detalhe is None:
        navegacao = "Home"
elif navegacao not in PAGINAS:
    navegacao = "Home"

ATUAL = 'aria-current="page"'
links = "".join(
    f'<a href="?p={chave}" target="_self" {ATUAL if chave == navegacao else ""}>{rotulo}</a>'
    for chave, rotulo in PAGINAS.items()
)
st.markdown(f'<nav class="nav-custom" aria-label="Principal">{links}</nav><div class="content-wrapper"></div>', unsafe_allow_html=True)

if detalhe:
    st.title(detalhe["titulo"], anchor=False)
    pagina_tipo = detalhe["tipo"] if detalhe["tipo"] in PAGINAS else "Home"
    st.markdown(
        f'<p class="voltar"><a href="?p={pagina_tipo}" target="_self">Voltar para {PAGINAS[pagina_tipo]}</a></p>',
        unsafe_allow_html=True,
    )
    try:
        par = adaptacoes().get(detalhe["id"])
    except Exception:
        par = None
    st.markdown(detalhe_html(detalhe, par), unsafe_allow_html=True)
    st.stop()

st.title("Cine&Livro" if navegacao == "Home" else f"Cine&Livro — {PAGINAS[navegacao]}", anchor=False)
if aviso:
    st.warning(aviso)

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

# O st.spinner só aparece se a espera passar de meio segundo; a barra de "Running" do Streamlit fica escondida pelo CSS
try:
    with st.spinner("Carregando o catálogo…"):
        if ATRASO_TESTE > 0:
            time.sleep(ATRASO_TESTE)
        itens = consultar(navegacao, categoria_sel, search or "")
        pares = adaptacoes()
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
        # h2 por categoria (o título da obra no card é h3) e sem âncora, para não somar paradas no Tab
        st.header(categoria, anchor=False)
        for i in range(0, len(lista), 3):
            cols = st.columns(3)
            for j, item in enumerate(lista[i:i + 3]):
                with cols[j]:
                    st.markdown(card_html(item, pares.get(item["id"])), unsafe_allow_html=True)
        st.write("---")
elif itens is not None:
    termo = html.escape(search or "")
    st.info(f"Nenhum resultado encontrado{f' para “{termo}”' if termo else ''}.")
# Fim de app.py
