"""Testes da interface com o AppTest do Streamlit (execução sem navegador)."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def rodar(p=None):
    """Executa o app, opcionalmente em uma página (?p=)."""
    at = AppTest.from_file(APP, default_timeout=30)
    if p:
        at.query_params["p"] = p
    return at.run()


def test_home_agrupa_por_categoria():
    at = rodar()
    assert not at.exception
    assert [s.value for s in at.subheader] == ["Ação", "Comédia", "Ficção Científica", "Romance", "Terror"]
    assert at.caption[0].value == "30 títulos encontrados"


def test_pagina_de_livros_tem_filtro_com_categorias_do_banco():
    at = rodar("Livro")
    assert not at.exception, at.exception
    assert at.selectbox, [m.value for m in at.error]
    opcoes = at.selectbox[0].options
    assert opcoes[0] == "Todas" and "Romance" in opcoes
    at.selectbox[0].select("Terror").run()
    assert [s.value for s in at.subheader] == ["Terror"]


def test_pagina_invalida_volta_para_home():
    at = rodar("<script>")
    assert at.title[0].value == "Cine&Livro"
# Fim de test_app.py
