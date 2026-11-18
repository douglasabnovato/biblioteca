# Plano de ação — Cine&Livro

Timebox: 30 min.

| MoSCoW | Item | Ganho | Esforço | Status |
|---|---|---|---|---|
| Must | Script de carga funcionando (D1) | Alto | Baixo | ✅ |
| Must | Escape do HTML (D2) | Alto | Baixo | ✅ |
| Should | Erro amigável sem banco (D3) | Médio | Baixo | ✅ |
| Should | Acessibilidade (D4) | Médio | Baixo | ✅ axe 0 |
| Should | Busca sem acento, categorias do banco (D5) | Médio | Baixo | ✅ |
| Could | Página de detalhe com sinopse longa e onde assistir/comprar | Alto | Médio | Próximo ciclo |
| Could | Rodapé e CTA (itens do README) | Baixo | Baixo | Próximo ciclo |

## Ciclo de 18/11/2026

> Branch `feature/2026-11-18` → `developer/sprint-2026-11-19` → `main`. Nível: N1. Triagem das issues pela regra de 18/11/2026 da engenharia.

- Título do card sem o link "Link to heading" no Tab (#19).
- Versões do teste de tela fixas em `requirements-tela.txt` (#21), as mesmas do CI de 16/11/2026: playwright 1.65.2, pytest-playwright 0.10.0 e axe-playwright-python 0.1.8. O passo `pip list` do job `tela` mostra as instaladas.

## Ciclo de 15/11/2026

> Executado em 15 e 16/11/2026. Branch `feature/2026-11-15` → `developer/sprint-2026-11-12` → `main`. O PR da sprint para a `main` (#15) segue aberto com o responsável. Nível: N1.

### Produto

**Problema e público.** Quem busca o que ver ou ler encontra filmes e livros num único catálogo.

**Hipótese e meta.** Acreditamos que a busca sem acento e o filtro por categoria deixam uma pessoa achar um título sem instrução. Saberemos quando o teste de tela no navegador fizer o percurso (busca, menu e filtro) sem ajuda e sem violação do axe, sem violação do axe, em todo PR. Num projeto N1 não há medição com público.

**Foco do ciclo.** Fechar as lacunas da régua: hipótese com "saberemos quando", axe com zero violações (inclusive a moderada `region`, #11), tema escuro fixo, para a tela não depender da preferência do sistema (o app não tem tema claro), auditoria de dependências no CI e hospedagem com passo a passo atualizado.

**O que a pesquisa trouxe.**

| Ideia | O que levamos para o projeto | Fonte |
|---|---|---|
| A regra `region` do axe pede todo o conteúdo dentro de um landmark; o preferido é o elemento nativo (`<main>`), e `role="main"` é aceito | O Streamlit 1.67 já desenha o conteúdo num `<main>`; o teste passa a reprovar qualquer violação e confere que existe um `main` | [Deque University: regra region](https://dequeuniversity.com/rules/axe/4.10/region) |
| O tema do Streamlit herda de `base = "light"` ou `"dark"` no `[theme]` do `.streamlit/config.toml` | Fixar `base = "dark"`, que é o visual do CSS do projeto, para a tela não mudar com a preferência do sistema | [Streamlit: config.toml](https://docs.streamlit.io/develop/api-reference/configuration/config.toml), [Streamlit: theming](https://docs.streamlit.io/develop/concepts/configuration/theming) |
| No Community Cloud, só quem administra o app o torna público: App settings → Sharing → "This app is public and searchable", ou Share → "Make this app public" | Passo a passo clique a clique no `docs/DEPLOY.md` e na issue #4 | [Streamlit: share your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app) |
| O `pip-audit` confere pacotes Python contra a base de vulnerabilidades do PyPA | Passo `pip-audit -r requirements.txt` no CI, já que os alertas do Dependabot estão desligados (API 403) | [PyPI: pip-audit](https://pypi.org/project/pip-audit/) |

**Backlog priorizado (impacto × esforço).**

| Prioridade | Item | Impacto | Esforço | Destino |
|---|---|---|---|---|
| 1 | Auditoria de dependências no CI e atualização minor do Streamlit | Alto | Baixo | Este ciclo |
| 2 | Hipótese com meta e "saberemos quando"; critério 3 conforme a régua N1 | Alto | Baixo | Este ciclo |
| 3 | Violação `region` e tema escuro fixo | Médio | Baixo | Este ciclo (#11) |
| 4 | Esc fecha o filtro de categoria e devolve o foco; teste do aviso de carregamento | Médio | Baixo | Este ciclo (#18) |
| 5 | Página de detalhe de cada título | Alto | Médio | Este ciclo, se couber (#7) |
| 6 | Mais pares de filme e livro | Médio | Médio | Issue #8 |
| 7 | App público e caminhos longos no Windows | Alto | Baixo | Responsável (#4, #12) |

**Fora do escopo.** Contas, avaliações, recomendação personalizada, API externa de filmes ou livros, domínio próprio.

### Engenharia

**Arquitetura.** `app.py` (Streamlit) lê o SQLite em modo leitura por `src/backend.py`; `src/render.py` monta o HTML escapado dos cards. O tema fica em `.streamlit/config.toml`. Os testes rodam em dois jobs: `app` (pytest com AppTest, sem navegador) e `tela` (Playwright e axe com `streamlit run`).

**Riscos.**
- O landmark `main` vem do HTML do Streamlit 1.67; se uma versão futura mudar isso, o teste de tela reprova.
- Subir o Streamlit de 1.64 para 1.67 pode mudar o DOM; o job `tela` pega a quebra.
- O `pip` com Streamlit falha no Windows local por caminho longo (#12); o que não rodar aqui roda no CI e fica registrado no PR.

**Qualidade.** Testes do fluxo no navegador com axe sem violação, teclado (Tab e Esc) e foco visível; `pip-audit` sem vulnerabilidade conhecida; nenhum segredo nem dado pessoal.

**Definição de pronto.** Jobs `app` e `tela` verdes no PR; `docs/MVP.md`, README e `docs/DEPLOY.md` atualizados com comando, data e resultado.

### Plano de ação

**Este ciclo executa.** Itens 1 a 5 do backlog, o passo a passo de publicação e a atualização dos documentos.

**Vira issue.** Mais pares (#8), app público (#4), caminhos longos (#12) e as tarefas novas que o ciclo identificar.

## Ciclo de 07/11/2026

> Executado em 09/11/2026. Branch `feature/2026-11-07` → `developer/sprint-2026-11-12` → `main` (o PR para a `main` fica com o responsável). Nível: N1.

### Produto

**Foco.** Critério 8: medir acessibilidade e teclado com o app rodando (#6) e percorrer o fluxo principal na tela.

**O que a pesquisa trouxe.**

| Ideia | O que levamos para o projeto | Fonte |
|---|---|---|
| O `axe-playwright-python` roda o axe-core numa página aberta pelo Playwright em Python e devolve as violações | Job `tela` no CI com `Axe().run(page)` nas 3 páginas; falha com violação grave ou crítica | [PyPI: axe-playwright-python](https://pypi.org/project/axe-playwright-python), [documentação de uso](https://pamelafox.github.io/axe-playwright-python/usage) |
| O Streamlit diz que pensa em acessibilidade nos componentes, mas nunca fez uma avaliação oficial | Testar o app montado, e não confiar no componente; o teste achou contraste baixo no `st.caption` | [Fórum do Streamlit: conformidade 508](https://discuss.streamlit.io/t/508-compliance-for-streamlit/13579/2) |
| Regiões da página (header, main, footer) ajudam quem usa teclado e leitor de tela a pular blocos | Virou issue: tirar a violação `region` (#11) | [IBM Accessibility: design visual](https://www.ibm.com/able/toolkit/design/visual/) |

**Backlog do ciclo.**

| Prioridade | Item | Destino |
|---|---|---|
| 1 | Teste de tela com axe e teclado no CI | Este ciclo (#6) |
| 2 | Contraste da contagem e ordem dos títulos | Este ciclo (#6) |
| 3 | Violação moderada `region` | Issue #11 |
| 4 | Rodar o app no Windows (caminhos longos) | Responsável (#12) |
| 5 | Página de detalhe e mais pares | Issues #7 e #8 |
| 6 | App público e proteção da `main` | Responsável (#4, #5) |

### Engenharia

**Arquitetura.** Streamlit (`app.py`) lê o SQLite por `src/backend.py`; `src/render.py` monta os cards com HTML escapado. Os testes de tela ficam em `tela/`, fora do `pytest` padrão, para falhar (e não serem pulados) quando o app não está no ar.

**Riscos.**
- O Streamlit desenha a tela em partes: o teste espera o menu e a busca aparecerem antes de usar o teclado, e espera sobrar um título só depois do filtro.
- Versões do Playwright e do axe no job `tela` não estão fixas (`>=`); o log do CI registra as instaladas (playwright 1.64.1, pytest-playwright 0.10.0). Fixadas em 18/11/2026 (#21).

**Definição de pronto.** Jobs `app` e `tela` verdes no PR; `docs/MVP.md` e README atualizados.

### Plano de ação

**Este ciclo executa.** Itens 1 e 2 do backlog, o fluxo na tela e a atualização do `docs/MVP.md` e do README.

**Vira issue.** #11 (agente); #12 (responsável).

## Ciclo de 03/11/2026

Executado em 06/11/2026, nas branches `feature/2026-11-06` → `developer/sprint-2026-11-12` → `main`.

### Produto

**Problema e público.** Quem busca o que ver ou ler encontra filmes e livros num único catálogo, por busca ou categoria.

**Hipótese e meta (proposta).** Uma pessoa acha um título pela busca ou pela categoria sem instrução.

**O que a pesquisa trouxe.**

| Ideia | Fonte | Uso aqui |
|---|---|---|
| Serviços de streaming juntam num só lugar as obras que vieram de livros, para quem leu o livro achar o filme | [Best of Netflix, hub de adaptações](https://best-of-netflix.com/netflix-launches-new-hub-for-fans-of-book-to-screen-adaptations/) | O card mostra "Também em livro/filme" quando a obra existe nos dois formatos |
| Um app do Streamlit Community Cloud que pede login está privado; só quem administra muda para público | [Streamlit, Share your app](https://docs.streamlit.io/streamlit-community-cloud/get-started/share-your-app) | Explica o 303 e o passo do responsável em #4 |

**Backlog priorizado (impacto × esforço).**

| Item | Impacto | Esforço | Destino |
|---|---|---|---|
| Ligar filme e livro da mesma obra | Médio | Baixo | Este ciclo |
| README honesto sobre o link | Alto | Baixo | Este ciclo |
| Tornar o app público | Alto | Baixo (responsável) | [#4](https://github.com/douglasabnovato/biblioteca/issues/4) |
| Proteger a `main` | Médio | Baixo (responsável) | [#5](https://github.com/douglasabnovato/biblioteca/issues/5) |
| Medir acessibilidade | Médio | Baixo | [#6](https://github.com/douglasabnovato/biblioteca/issues/6) |
| Página de detalhe | Alto | Médio | [#7](https://github.com/douglasabnovato/biblioteca/issues/7) |
| Mais pares no catálogo | Médio | Baixo | [#8](https://github.com/douglasabnovato/biblioteca/issues/8) |

**Fora do escopo.** Recomendação personalizada, contas e avaliações.

### Engenharia

**Arquitetura.** App Streamlit (`app.py`) que lê um SQLite em modo leitura (`src/backend.py`) e monta cards com escape de HTML (`src/render.py`). O banco é gerado de `scripts/itens.json` por `scripts/popular_banco.py`. A ligação entre formatos usa uma chave do título sem acento, pontuação e conectores.

**Riscos.** O app publicado é privado. A chave do título pode ligar obras diferentes com nomes parecidos; com 30 títulos, os testes conferem que só Percy Jackson forma par.

**Qualidade.** pytest com AppTest do Streamlit no CI (Python 3.12). Escape de HTML testado no texto novo.

**Definição de pronto.** CI verde, teste novo, `MVP.md` e README atualizados.

### Plano de ação

**Executado neste ciclo.** Ligação entre filme e livro; README com o link real e o motivo do 303; régua N1; seção de estado no README.

**Vira issue.** #4 a #8.
