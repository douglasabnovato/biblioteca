"""Testes da interface com o AppTest do Streamlit (execução sem navegador)."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.backend import buscar_dados

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def rodar(p=None, **params):
    """Executa o app, opcionalmente em uma página (?p=) e com outros parâmetros da URL (ex.: id)."""
    at = AppTest.from_file(APP, default_timeout=30)
    if p:
        at.query_params["p"] = p
    for chave, valor in params.items():
        at.query_params[chave] = valor
    return at.run()


def id_de(titulo):
    """Id de um título no banco que o app usa."""
    return next(i["id"] for i in buscar_dados() if i["titulo"] == titulo)


def test_home_agrupa_por_categoria():
    at = rodar()
    assert not at.exception
    assert [s.value for s in at.header] == ["Ação", "Comédia", "Ficção Científica", "Romance", "Terror"]
    assert at.caption[0].value == "30 títulos encontrados"


def test_pagina_de_livros_tem_filtro_com_categorias_do_banco():
    at = rodar("Livro")
    assert not at.exception, at.exception
    assert at.selectbox, [m.value for m in at.error]
    opcoes = at.selectbox[0].options
    assert opcoes[0] == "Todas" and "Romance" in opcoes
    at.selectbox[0].select("Terror").run()
    assert [s.value for s in at.header] == ["Terror"]


def test_home_mostra_adaptacao_entre_filme_e_livro():
    at = rodar()
    textos = " ".join(m.value for m in at.markdown)
    assert "Também em livro: Percy Jackson - O Ladrão de Raios" in textos
    assert "Também em filme: Percy Jackson e O Ladrão de Raios" in textos


def test_pagina_invalida_volta_para_home():
    at = rodar("<script>")
    assert at.title[0].value == "Cine&Livro"
def test_detalhe_mostra_titulo_tipo_categoria_e_descricao():
    at = rodar("item", id=str(id_de("Duna")))
    assert not at.exception, at.exception
    assert at.title[0].value == "Duna"
    textos = " ".join(m.value for m in at.markdown)
    assert "<dt>Tipo</dt><dd>Livro</dd>" in textos and "<dt>Categoria</dt><dd>Ficção Científica</dd>" in textos
    assert 'href="?p=Livro"' in textos
    assert not at.warning


def test_detalhe_liga_para_a_obra_no_outro_formato():
    filme = id_de("Percy Jackson e O Ladrão de Raios")
    livro = id_de("Percy Jackson - O Ladrão de Raios")
    at = rodar("item", id=str(filme))
    textos = " ".join(m.value for m in at.markdown)
    assert f'Também em livro: <a href="?p=item&amp;id={livro}" target="_self">' in textos


def test_detalhe_com_id_inexistente_ou_invalido_volta_para_o_inicio_com_aviso():
    for valor in ("99999", "abc", "0", "1 OR 1=1", ""):
        at = rodar("item", id=valor)
        assert not at.exception, (valor, at.exception)
        assert at.title[0].value == "Cine&Livro", valor
        assert at.warning and "não encontrado" in at.warning[0].value, valor
        assert at.caption[0].value == "30 títulos encontrados", valor


def test_card_da_home_leva_ao_detalhe():
    at = rodar()
    textos = " ".join(m.value for m in at.markdown)
    assert f'<h3><a href="?p=item&amp;id={id_de("Duna")}" target="_self">Duna</a></h3>' in textos
# Fim de test_app.py
