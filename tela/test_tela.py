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
SAIDA = Path(os.environ.get("TELA_SAIDA", "tela-saida"))
SAIDA.mkdir(exist_ok=True)
PAGINAS = {"Home": "Início", "Filme": "Filmes", "Livro": "Livros"}


def abrir(page: Page, p: str = "Home"):
    page.goto(f"{URL}/?p={p}")
    expect(page.get_by_text("encontrado").first).to_be_visible(timeout=90_000)


def frame_busca(page: Page):
    return page.frame_locator('iframe[title="st_keyup.st_keyup"]')


@pytest.mark.parametrize("p", list(PAGINAS))
def test_axe_sem_violacao_grave(page: Page, p: str):
    abrir(page, p)
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
    (SAIDA / f"axe-{p}.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
    page.screenshot(path=str(SAIDA / f"tela-{p}.png"), full_page=True)
    print(f"axe {p}: {len(violacoes)} violações", json.dumps(resumo, ensure_ascii=False))
    graves = [r for r in resumo if r["impacto"] in ("serious", "critical")]
    assert graves == [], graves


def test_fluxo_principal_busca_e_filtro(page: Page):
    abrir(page)
    # 1. Busca em tempo real pelo título
    campo = frame_busca(page).locator("input")
    campo.fill("Duna")
    expect(page.get_by_text("Duna").first).to_be_visible(timeout=30_000)
    expect(page.get_by_text("título encontrado").or_(page.get_by_text("títulos encontrados")).first).to_be_visible()
    page.screenshot(path=str(SAIDA / "fluxo-1-busca.png"), full_page=True)
    # 2. Menu leva para Livros, com o item atual marcado
    page.get_by_role("link", name="Livros").click()
    expect(page.get_by_role("link", name="Livros")).to_have_attribute("aria-current", "page", timeout=60_000)
    # 3. Filtro de categoria
    page.get_by_label("Filtrar por categoria").click()
    page.get_by_role("option", name="Terror").click()
    expect(page.get_by_role("heading", name="Terror", exact=True)).to_be_visible(timeout=30_000)
    expect(page.get_by_role("heading", name="Romance", exact=True)).to_have_count(0)
    page.screenshot(path=str(SAIDA / "fluxo-2-filtro.png"), full_page=True)


def test_teclado_alcanca_menu_busca_e_filtro_com_foco_visivel(page: Page):
    abrir(page, "Filme")
    page.wait_for_timeout(3000)
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
                    contorno: estilo.outlineStyle !== 'none' && parseFloat(estilo.outlineWidth) > 0,
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
