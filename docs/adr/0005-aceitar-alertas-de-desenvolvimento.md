# ADR-05: Aceitar os alertas de desenvolvimento do Dependabot

- **Status:** Aceita; a substituir quando a `main` receber o pytest 9.2.0 (#20, na `feature/2026-11-18` desde 18/11/2026)
- **Data:** 16/11/2026
- **Origem:** ordem do responsável repassada pelo DG líder em 16/11/2026:

> "Regra geral por ADR. alertas que nao atrapalham a producao, pode passar. os que atrapalham, entender, escolher a melhor estrategia para manter a funcionalidade"

## Contexto

Em 16/11/2026, 14h38, `gh api "repos/douglasabnovato/biblioteca/dependabot/alerts?state=open&per_page=100"` deu 2 alertas abertos. Os dois são o mesmo aviso (GHSA-6w46-j5rx-g56g, "pytest has vulnerable tmpdir handling") no `pytest` 8.4.2, corrigido só na 9.0.3, versão maior.

O app no ar roda no Streamlit Community Cloud, que instala só o `requirements.txt` da raiz (ver `docs/DEPLOY.md`). Esse arquivo tem `streamlit`, `streamlit-keyup` e `pillow`; o `pytest` não está nele (`grep -c pytest requirements.txt` devolve 0). Os arquivos `requirements-dev.txt` e `requirements-tela.txt` só são instalados pelo CI (jobs `app` e `tela`) e por quem desenvolve.

## Decisão

Aceitar os alertas abaixo, porque não chegam à produção.

| Alerta | Pacote | Severidade | Quem o puxa | Por que não chega à produção |
|---|---|---|---|---|
| #1 | pytest 8.4.2 | média | `requirements-dev.txt` (dependência direta de teste) | Só o CI e quem desenvolve instalam esse arquivo; o Streamlit Cloud instala o `requirements.txt`, sem `pytest` |
| #2 | pytest 8.4.2 | média | `requirements-tela.txt` (inclui `-r requirements-dev.txt`) | Só o job `tela` do CI instala esse arquivo, para o teste no navegador |

Os alertas não são dispensados nem fechados pela API. Esta ADR só registra a decisão.

## Consequências

- O risco fica no ambiente de quem desenvolve e no CI (o aviso trata de pastas temporárias do `pytest`), não no app publicado.
- O `pip-audit -r requirements.txt` do job `app` segue cobrindo o que vai para a produção.
- A migração para o pytest 9 continua como próximo passo em #20, sem bloquear o critério 9.

## Quando revisar

- Se o `pytest`, ou outro pacote de desenvolvimento, passar a constar no `requirements.txt`.
- Se surgir correção do aviso na linha 8.x, sem versão maior.
- Na migração para o pytest 9 (#20), ou se a hospedagem passar a instalar outro arquivo de dependências.
