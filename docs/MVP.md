# MVP — Cine&Livro

> Criado em 31/10/2026, com os critérios usados no `movies`. Situação baseada em `AVALIACAO.md` e na conferência deste ciclo.

## Problema e hipótese

**Problema e público:** Quem busca o que ver ou ler encontra filmes e livros em um único catálogo.

**Hipótese:** Projeto de estudo: uma pessoa acha um título pela busca ou pela categoria sem instrução. Proposta inicial, para o responsável confirmar ou trocar. Sem medição, a meta ainda não pode ser conferida.

**Nível:** N1 (estudo). **Resumo em 06/11/2026:** 7 de 10 critérios aplicáveis atendem (1, 2, 4, 6, 9, 11, 12); 2 parciais (3, 10); 1 não medido (8); 5 e 7 não se aplicam (N1). **Finalizado: não.** Falta o critério 8 (#6), que o código resolve; 3 e 10 dependem do responsável (#4, #5).

## 1. Critérios

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

## 2. Tarefas

| # | Tarefa | Situação |
|---|---|---|
| 1 | Ativar o CI que estava em `ci/` e tirar arquivos compilados do Git | PR aberto |
| 2 | Confirmar a URL ou tornar o app público no Streamlit | Com o responsável |

## 3. Fora do MVP

Recomendação personalizada, contas e avaliações. A lista é uma proposta e pode mudar com a decisão do responsável.

## 4. Revisão de 06/11/2026 (ciclo de 03/11/2026)

- Régua N1: critérios 5 e 7 passam a "Não se aplica".
- Link publicado conferido com `curl`: https://biblioteca-cine-livros.streamlit.app/ e https://cinelivro.streamlit.app respondem 303 para o login do Streamlit (#4).
- Critério 12 vai para "Atende": o README diz o link real e por que não abre.
- Cards mostram a obra no outro formato. Testes: 15 (antes 11).
