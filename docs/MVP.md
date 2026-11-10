# MVP — Cine&Livro

> Fonte única do estado. Tabela atual de 09/11/2026 (ciclo de 07/11/2026), com o critério 10 revisto em 10/11/2026. As tabelas anteriores estão em "Histórico", no fim.

**Problema e público:** Quem busca o que ver ou ler encontra filmes e livros num único catálogo.

**Nível:** N1 (estudo). Critérios 5 (medição) e 7 (LCP no ar) não se aplicam e saem da conta.

**Resumo:** 9 de 10 aplicáveis atendidos

**Finalizado:** sim

O critério que falta (3) depende do responsável, com issue `depende-do-responsavel`: tornar o app público (#4). A `main` está protegida desde 10/11/2026 (#5).

| # | Critério | Como verificar | Situação em 09/11/2026 |
|---|---|---|---|
| 1 | Problema e público claros | Dá para explicar em uma frase | Atende: frase acima |
| 2 | Hipótese a validar | Existe uma aposta escrita, com meta | Atende: uma pessoa acha um título pela busca ou pela categoria sem instrução (objetivo de estudo, ver Histórico) |
| 3 | Fluxo principal completo | Uma pessoa conclui sem ajuda | Parcial: o fluxo foi percorrido num Chromium real no CI em 09/11/2026 (ver abaixo), mas o endereço publicado responde 303 e pede login (#4) |
| 4 | Escopo enxuto | O que não entra está registrado | Atende: catálogo fixo em SQLite; recomendação, contas e avaliações ficam fora |
| 5 | Medição de uso | A métrica principal é coletada | Não se aplica (N1) |
| 6 | Falhas tratadas | Erro, vazio e carregamento têm resposta clara | Atende: `pytest -q` no CI em 09/11/2026, 15 passed, inclusive banco ausente e busca vazia |
| 7 | Desempenho aceitável | LCP de até 2,5 s no celular | Não se aplica (N1) |
| 8 | Acessibilidade básica | axe e teclado | Atende: `pytest tela -v` no job `tela` do CI em 09/11/2026 ([run](https://github.com/douglasabnovato/biblioteca/actions/runs/42631834475)), 5 passed. O axe-core não achou violação grave em Início, Filmes e Livros; antes, a contagem de resultados tinha contraste de 3,68:1. O Tab alcança o menu, a busca e o filtro, com foco visível. Sobra 1 violação moderada, `region` (#11) |
| 9 | Segurança e conformidade | Riscos decididos; termos de terceiros cumpridos | Atende: sem dados pessoais; consulta parametrizada; título e descrição escapados no HTML (`tests/test_backend.py`) |
| 10 | Entrega confiável | Publicação só depois de CI verde | Atende: `gh api repos/douglasabnovato/biblioteca/rulesets` em 10/11/2026: ruleset `principal-protegida` ativo (exige PR, bloqueia force push e exclusão); o workflow `CI` roda em todo push e PR, com os jobs `app` e `tela` (#5) |
| 11 | Testes dos fluxos críticos | Testes automatizados no CI | Atende: `pytest -q` (15 testes, com AppTest) e `pytest tela` (5 testes num navegador real), verdes no CI em 09/11/2026 |
| 12 | Documentação honesta | Qualquer pessoa roda o projeto, e os números estão certos | Atende: README com o link real e o motivo de não abrir; `curl` em 09/11/2026 deu 303 para o login, e o README diz isso |

### Fluxo principal percorrido na tela (09/11/2026)

Como foi feito: o `pip` com Streamlit falha no Windows local por caminho longo (#12). Por isso o job `tela` do CI sobe o app com `streamlit run app.py` e roda `tela/test_tela.py` num Chromium real (Playwright). As capturas e o resultado do axe ficam no artefato `tela-saida` do [run](https://github.com/douglasabnovato/biblioteca/actions/runs/42631834475).

1. Início abre com "30 títulos encontrados".
2. A busca em tempo real, digitando "Duna", reduz a lista de 30 títulos e tira os que não são Duna.
3. O menu leva a Livros e marca `aria-current="page"`.
4. O filtro "Terror" deixa só a categoria Terror.
5. Pelo teclado, o Tab passa por Início, Filmes, Livros, a busca e o filtro de categoria, e os links mostram contorno de foco.
6. O axe-core roda em Início, Filmes e Livros, sem violação grave.

O que o teste achou e o ciclo corrigiu: o contraste da contagem e a ordem dos títulos (h3 logo abaixo do h1). Também saíram as âncoras dos títulos, que somavam paradas inúteis no Tab.

## Histórico

### Tabela de 06/11/2026 (ciclo de 03/11/2026)

> Criado em 31/10/2026, com os critérios usados no `movies`. Situação baseada em `AVALIACAO.md` e na conferência deste ciclo.

### Problema e hipótese

**Problema e público:** Quem busca o que ver ou ler encontra filmes e livros em um único catálogo.

**Hipótese:** Projeto de estudo: uma pessoa acha um título pela busca ou pela categoria sem instrução. Proposta inicial, para o responsável confirmar ou trocar. Sem medição, a meta ainda não pode ser conferida.

**Nível:** N1 (estudo). **Resumo em 06/11/2026:** 7 de 10 critérios aplicáveis atendem (1, 2, 4, 6, 9, 11, 12); 2 parciais (3, 10); 1 não medido (8); 5 e 7 não se aplicam (N1). **Finalizado: não.** Falta o critério 8 (#6), que o código resolve; 3 e 10 dependem do responsável (#4, #5).

### 1. Critérios

| # | Critério | Como verificar | Situação em 31/10/2026 |
|---|---|---|---|
| 1 | Problema e público claros | Dá para explicar em uma frase | Atende |
| 2 | Hipótese a validar | Existe uma aposta escrita, com meta | Atende: objetivo de estudo |
| 3 | Fluxo principal completo | Uma pessoa conclui sem ajuda | Parcial: testes de tela existem; o endereço publicado responde 303 e pede login (06/11/2026, #4) |
| 4 | Escopo enxuto | O que não entra está registrado | Atende: catálogo fixo em SQLite |
| 5 | Medição de uso | A métrica principal é coletada | Não se aplica (N1): projeto de estudo |
| 6 | Falhas tratadas | Erro, vazio e carregamento têm resposta clara | Atende: banco ausente e busca vazia têm mensagem |
| 7 | Desempenho aceitável | LCP de até 2,5 s no celular | Não se aplica (N1): o app publicado é privado (#4) |
| 8 | Acessibilidade básica | Lighthouse e teclado | Não medido neste ciclo (#6) |
| 9 | Segurança e conformidade | Riscos decididos; termos de terceiros cumpridos | Atende: sem dados pessoais; consulta parametrizada |
| 10 | Entrega confiável | Publicação só depois de CI verde | Parcial: CI em todo push e PR; `main` sem proteção (#5) |
| 11 | Testes dos fluxos críticos | Testes automatizados no CI | Atende: `tests/test_app.py` e `tests/test_backend.py` |
| 12 | Documentação honesta | Qualquer pessoa roda o projeto, e os números estão certos | Atende: README com o link real, o motivo de não abrir (303) e a issue #4; comandos conferidos em 06/11/2026 |

**Resultado:** 7 de 10 critérios aplicáveis atendidos (06/11/2026). Antes: 6 de 12.

### 2. Tarefas

| # | Tarefa | Situação |
|---|---|---|
| 1 | Ativar o CI que estava em `ci/` e tirar arquivos compilados do Git | PR aberto |
| 2 | Confirmar a URL ou tornar o app público no Streamlit | Com o responsável |

### 3. Fora do MVP

Recomendação personalizada, contas e avaliações. A lista é uma proposta e pode mudar com a decisão do responsável.

### 4. Revisão de 06/11/2026 (ciclo de 03/11/2026)

- Régua N1: critérios 5 e 7 passam a "Não se aplica".
- Link publicado conferido com `curl`: https://biblioteca-cine-livros.streamlit.app/ e https://cinelivro.streamlit.app respondem 303 para o login do Streamlit (#4).
- Critério 12 vai para "Atende": o README diz o link real e por que não abre.
- Cards mostram a obra no outro formato. Testes: 15 (antes 11).
