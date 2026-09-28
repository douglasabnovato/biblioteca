"""Testes da camada de dados, do script de carga e do HTML dos cards."""
import json

import pytest

from scripts.popular_banco import carregar, popular
from src.backend import buscar_dados, listar_categorias, normalizar
from src.render import card_html


@pytest.fixture(scope="module")
def db(tmp_path_factory):
    """Banco temporário gerado a partir do itens.json do projeto."""
    caminho = tmp_path_factory.mktemp("db") / "teste.db"
    popular(carregar(), caminho)
    return caminho


def test_normalizar_remove_acentos():
    assert normalizar("  Ficção Científica ") == "ficcao cientifica"


def test_busca_sem_acento_e_sem_maiusculas(db):
    assert [i["titulo"] for i in buscar_dados(busca="DRACULA", db_path=db)] == [i["titulo"] for i in buscar_dados(busca="drácula", db_path=db)]
    assert buscar_dados(busca="dracula", db_path=db)


def test_filtros_por_tipo_e_categoria(db):
    livros = buscar_dados(tipo="Livro", db_path=db)
    assert livros and all(i["tipo"] == "Livro" for i in livros)
    terror = buscar_dados(tipo="Filme", categoria="Terror", db_path=db)
    assert all(i["categoria"] == "Terror" and i["tipo"] == "Filme" for i in terror)
    assert len(buscar_dados(db_path=db)) == 30


def test_curingas_do_like_nao_viram_filtro(db):
    assert buscar_dados(busca="%", db_path=db) == []
    assert buscar_dados(busca="_", db_path=db) == []


def test_categorias_vem_do_banco(db):
    assert "Romance" in listar_categorias(db_path=db)
    assert set(listar_categorias("Livro", db_path=db)) <= set(listar_categorias(db_path=db))


def test_card_escapa_html():
    html = card_html({"titulo": "<script>x</script>", "descricao": "a & b", "tipo": "Livro", "imagem": ""})
    assert "<script>" not in html and "&lt;script&gt;" in html and "a &amp; b" in html
    assert 'class="badge livro"' in html


def test_card_com_capa_tem_alt():
    item = buscar_dados(busca="duna")[0]
    assert f'alt="Capa de {item["titulo"]}"' in card_html(item)


def test_carga_recusa_item_invalido(tmp_path):
    arquivo = tmp_path / "itens.json"
    arquivo.write_text(json.dumps([{"titulo": "X", "descricao": "", "imagem": "./assets/x.jpg", "tipo": "Série", "categoria": "Ação"}]), encoding="utf-8")
    with pytest.raises(ValueError, match="faltando descricao"):
        carregar(arquivo)
# Fim de test_backend.py
