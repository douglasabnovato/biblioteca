# MVP — Cine&Livro

> Criado em 31/10/2026, com os critérios usados no `movies`. Situação baseada em `AVALIACAO.md` e na conferência deste ciclo.

## Problema e hipótese

**Problema e público:** Quem busca o que ver ou ler encontra filmes e livros em um único catálogo.

**Hipótese:** Projeto de estudo: uma pessoa acha um título pela busca ou pela categoria sem instrução. Proposta inicial, para o responsável confirmar ou trocar. Sem medição, a meta ainda não pode ser conferida.

## 1. Critérios

| # | Critério | Como verificar | Situação em 31/10/2026 |
|---|---|---|---|
| 1 | Problema e público claros | Dá para explicar em uma frase | Atende |
| 2 | Hipótese a validar | Existe uma aposta escrita, com meta | Atende: objetivo de estudo |
| 3 | Fluxo principal completo | Uma pessoa conclui sem ajuda | Parcial: testes de tela existem; o endereço publicado redireciona para login |
| 4 | Escopo enxuto | O que não entra está registrado | Atende: catálogo fixo em SQLite |
| 5 | Medição de uso | A métrica principal é coletada | Não atende: nada coleta uso |
| 6 | Falhas tratadas | Erro, vazio e carregamento têm resposta clara | Atende: banco ausente e busca vazia têm mensagem |
| 7 | Desempenho aceitável | LCP de até 2,5 s no celular | Não medido neste ciclo |
| 8 | Acessibilidade básica | Lighthouse e teclado | Não medido neste ciclo |
| 9 | Segurança e conformidade | Riscos decididos; termos de terceiros cumpridos | Atende: sem dados pessoais; consulta parametrizada |
| 10 | Entrega confiável | Publicação só depois de CI verde | Parcial: CI ativado em PR; `main` sem proteção |
| 11 | Testes dos fluxos críticos | Testes automatizados no CI | Atende: `tests/test_app.py` e `tests/test_backend.py` |
| 12 | Documentação honesta | Qualquer pessoa roda o projeto, e os números estão certos | Parcial: o README marca a URL como sugerida |

**Resultado:** 6 de 12 critérios atendidos por inteiro. É um julgamento técnico.

## 2. Tarefas

| # | Tarefa | Situação |
|---|---|---|
| 1 | Ativar o CI que estava em `ci/` e tirar arquivos compilados do Git | PR aberto |
| 2 | Confirmar a URL ou tornar o app público no Streamlit | Com o responsável |

## 3. Fora do MVP

Recomendação personalizada, contas e avaliações. A lista é uma proposta e pode mudar com a decisão do responsável.
