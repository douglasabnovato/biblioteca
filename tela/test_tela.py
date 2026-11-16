"""Fluxo principal e acessibilidade com o app rodando, num navegador real (Playwright + axe-core).

Rodar: `streamlit run app.py` em um terminal e `pytest tela` em outro.
No CI, o job "tela" sobe o app e roda estes testes (issue #6).
Fica fora de `testpaths` de propósito: sem o app no ar, falha em vez de ser pulado.
"""
import json
import os
from pathlib import Path

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page, expect

URL = os.environ.get("APP_URL", "http://localhost:8501").rstrip("/")
# Segundo servidor, com CINELIVRO_ATRASO_TESTE: a consulta demora e o aviso de carregamento precisa aparecer (#18)
URL_LENTO = os.environ.get("APP_URL_LENTO", "http://localhost:8502").rstrip("/")
SAIDA = Path(os.environ.get("TELA_SAIDA", "tela-saida"))
SAIDA.mkdir(exist_ok=True)
PAGINAS = {"Home": "Início", "Filme": "Filmes", "Livro": "Livros"}


def abrir(page: Page, p: str = "Home", tema: str = "light"):
    # O tema do app é fixo (.streamlit/config.toml); o teste confere que a preferência do sistema não muda o resultado
    page.emulate_media(color_scheme=tema, reduced_motion="reduce")
    page.goto(f"{URL}/?p={p}")
    expect(page.get_by_text("encontrado").first).to_be_visible(timeout=90_000)
    # O Streamlit desenha em partes: espera o menu e a busca antes de testar o teclado
    expect(page.get_by_role("link", name="Livros")).to_be_visible(timeout=30_000)
    expect(page.locator('iframe[title="st_keyup.st_keyup"]')).to_be_visible(timeout=30_000)
    page.wait_for_load_state("networkidle")


def frame_busca(page: Page):
    return page.frame_locator('iframe[title="st_keyup.st_keyup"]')


def rodar_axe(page: Page, nome: str):
    """Roda o axe-core, guarda o resumo e a captura em tela-saida/ e devolve as violações."""
    resultado = Axe().run(page)
    violacoes = resultado.response["violations"]
    resumo = [
        {
            "regra": v["id"],
            "impacto": v["impact"],
            "alvos": [n["target"] for n in v["nodes"]][:5],
            "html": [n["html"][:160] for n in v["nodes"]][:3],
            "motivo": [n.get("failureSummary", "")[:300] for n in v["nodes"]][:2],
        }
        for v in violacoes
    ]
    (SAIDA / f"axe-{nome}.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
    page.screenshot(path=str(SAIDA / f"tela-{nome}.png"), full_page=True)
    print(f"axe {nome}: {len(violacoes)} violações", json.dumps(resumo, ensure_ascii=False))
    return resumo


@pytest.mark.parametrize("tema", ["light", "dark"])
@pytest.mark.parametrize("p", list(PAGINAS))
def test_axe_sem_violacao(page: Page, p: str, tema: str):
    # Desde o ciclo de 15/11/2026, qualquer violação reprova, inclusive as moderadas (#11)
    page.set_viewport_size({"width": 1366, "height": 900})
    abrir(page, p, tema)
    # Desde o Streamlit 1.67 o conteúdo fica num <main>; antes, a regra "region" acusava conteúdo fora de landmark
    expect(page.get_by_role("main")).to_have_count(1)
    resumo = rodar_axe(page, f"{p}-{tema}")
    assert resumo == [], resumo


@pytest.mark.parametrize("tema", ["light", "dark"])
def test_detalhe_abre_pelo_card_sem_violacao(page: Page, tema: str):
    page.set_viewport_size({"width": 1366, "height": 900})
    abrir(page, "Home", tema)
    page.locator(".card h3 a", has_text="Percy Jackson e O Ladrão de Raios").click()
    expect(page.get_by_role("heading", level=1, name="Percy Jackson e O Ladrão de Raios")).to_be_visible(timeout=60_000)
    expect(page.get_by_text("Também em livro")).to_be_visible()
    resumo = rodar_axe(page, f"detalhe-{tema}")
    assert resumo == [], resumo
    # O link da adaptação leva ao livro, e "Voltar" leva à lista do tipo
    page.locator(".detalhe a", has_text="Percy Jackson - O Ladrão de Raios").click()
    expect(page.get_by_role("heading", level=1, name="Percy Jackson - O Ladrão de Raios")).to_be_visible(timeout=60_000)
    page.get_by_role("link", name="Voltar para Livros").click()
    expect(page.get_by_role("link", name="Livros")).to_have_attribute("aria-current", "page", timeout=60_000)


def test_detalhe_com_id_invalido_volta_para_o_inicio(page: Page):
    page.goto(f"{URL}/?p=item&id=abc")
    expect(page.get_by_text("Título não encontrado")).to_be_visible(timeout=90_000)
    expect(page.get_by_text("30 títulos encontrados")).to_be_visible()


def test_esc_fecha_o_filtro_e_mantem_o_foco(page: Page):
    abrir(page, "Livro")
    filtro = page.get_by_label("Filtrar por categoria")
    filtro.focus()
    page.keyboard.press("ArrowDown")  # abre a lista do filtro pelo teclado
    expect(page.get_by_role("listbox")).to_be_visible(timeout=10_000)
    page.keyboard.press("Escape")
    expect(page.get_by_role("listbox")).to_have_count(0, timeout=10_000)
    foco = page.evaluate("() => document.activeElement.getAttribute('aria-label') || ''")
    assert "categoria" in foco.lower(), foco


def test_fluxo_principal_busca_e_filtro(page: Page):
    abrir(page)
    # 1. Busca em tempo real pelo título
    campo = frame_busca(page).locator("input")
    # O st_keyup reage a teclas (keyup), como uma pessoa digitando; fill() não dispara keyup
    campo.click()
    campo.press_sequentially("Duna", delay=80)
    # A Home começa com 30 títulos: a busca precisa reduzir a lista e tirar o que não é Duna
    expect(page.get_by_text("30 títulos encontrados")).to_have_count(0, timeout=30_000)
    expect(page.locator(".card h3", has_text="Interestelar")).to_have_count(0)
    expect(page.locator(".card h3", has_text="Duna").first).to_be_visible()
    page.screenshot(path=str(SAIDA / "fluxo-1-busca.png"), full_page=True)
    # 2. Menu leva para Livros, com o item atual marcado
    page.get_by_role("link", name="Livros").click()
    expect(page.get_by_role("link", name="Livros")).to_have_attribute("aria-current", "page", timeout=60_000)
    # 3. Filtro de categoria
    page.get_by_label("Filtrar por categoria").click()
    page.get_by_role("option", name="Terror").click()
    # Sem filtro há várias categorias (h2); com "Terror", sobra uma só, e é ela
    expect(page.get_by_role("heading", level=2)).to_have_count(1, timeout=30_000)
    expect(page.get_by_role("heading", level=2, name="Terror", exact=True)).to_be_visible()
    page.screenshot(path=str(SAIDA / "fluxo-2-filtro.png"), full_page=True)


def test_teclado_alcanca_menu_busca_e_filtro_com_foco_visivel(page: Page):
    abrir(page, "Filme")
    diagnostico = page.evaluate(
        """() => [...document.querySelectorAll('nav a, iframe, input, [role=combobox]')].map(e => ({
            tag: e.tagName, texto: (e.textContent || e.title || e.getAttribute('aria-label') || '').trim().slice(0, 30),
            tabIndex: e.tabIndex, inert: !!e.closest('[inert]'), oculto: !!e.closest('[aria-hidden=true]'),
            visibilidade: getComputedStyle(e).visibility, display: getComputedStyle(e).display,
            caixa: (r => [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)])(e.getBoundingClientRect()),
        }))"""
    )
    print("Focáveis:", json.dumps(diagnostico, ensure_ascii=False))
    vistos = []
    for _ in range(40):
        page.keyboard.press("Tab")
        alvo = page.evaluate(
            """() => {
                const a = document.activeElement;
                const estilo = getComputedStyle(a);
                return {
                    tag: a.tagName,
                    texto: (a.getAttribute('aria-label') || a.textContent || a.title || '').trim().slice(0, 40),
                    titulo: a.title || '',
                    // contorno do projeto (3px), e não o anel padrão de 1px do navegador
                    contorno: estilo.outlineStyle !== 'none' && parseFloat(estilo.outlineWidth) >= 3,
                };
            }"""
        )
        vistos.append(alvo)
    (SAIDA / "teclado.json").write_text(json.dumps(vistos, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Tab:", json.dumps(vistos, ensure_ascii=False))
    links = [v for v in vistos if v["tag"] == "A" and v["texto"] in PAGINAS.values()]
    assert {v["texto"] for v in links} == set(PAGINAS.values()), vistos
    assert all(v["contorno"] for v in links), links
    assert any(v["tag"] == "IFRAME" and "st_keyup" in v["titulo"] for v in vistos), vistos
    assert any(v["tag"] == "INPUT" and "categoria" in v["texto"].lower() for v in vistos), vistos


def test_aviso_de_carregamento_aparece_e_some(page: Page):
    page.goto(f"{URL_LENTO}/?p=Filme")
    aviso = page.get_by_text("Carregando o catálogo…")
    expect(aviso).to_be_visible(timeout=60_000)
    page.screenshot(path=str(SAIDA / "carregamento.png"), full_page=True)
    expect(page.get_by_text("15 títulos encontrados")).to_be_visible(timeout=60_000)
    expect(aviso).to_have_count(0)
