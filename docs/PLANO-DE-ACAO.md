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
