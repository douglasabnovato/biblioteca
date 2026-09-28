# Deploy · Cine&Livro

Plano de ação para publicar o catálogo de filmes e livros em hospedagem gratuita.

## 1. Desafio

Colocar no ar, sem custo e com deploy automático, uma aplicação Python/Streamlit que lê um banco SQLite local (`database/cine_livro.db`) e mostra capas guardadas em `assets/`.

## 2. Conteúdo

### Decisão de hospedagem

| Opção | Resultado |
|---|---|
| **Streamlit Community Cloud (escolhida)** | Gratuito, feito para apps Streamlit, lê `requirements.txt` e publica a cada push na branch escolhida |
| GitHub Pages | Não executa Python: serve só arquivos estáticos |
| Render (web service gratuito) | Funciona, mas exige comando de início, porta e dorme após 15 min; sem ganho sobre o Community Cloud |
| Hugging Face Spaces | Alternativa gratuita válida, mas é mais uma conta e mais um repositório |

### Banco de dados em produção

- `database/cine_livro.db` **está versionado** no Git (30 títulos) e o app o abre em **modo somente leitura**. O disco do Community Cloud é temporário, mas isso não afeta o app: nada é gravado, e a cada reinício o banco vem de novo do repositório.
- Para mudar o catálogo: editar `scripts/itens.json` (capa em `assets/`), rodar `python scripts/popular_banco.py` localmente e fazer commit do `.db` gerado. O CI recria o banco a partir do JSON antes dos testes, então um JSON inválido quebra o CI antes de chegar ao ar.
- O `.db` atual ainda tem o esquema antigo (sem o `CHECK` de tipo e sem o índice). Os testes passam com ele e com o banco regenerado (verificado). Recomendo regenerar na Etapa 1.

### O que foi ajustado

| Mudança | Arquivo | Por quê |
|---|---|---|
| Passo a passo de publicação | `docs/DEPLOY.md` | Este documento |
| Seção "Em produção" e linha de publicação | `readme.md` | Endereço e hospedagem visíveis |

Nenhuma mudança de código foi necessária: o app já usa caminhos relativos à raiz do repositório, `requirements.txt` fixa as versões (`streamlit==1.64.0`, `streamlit-keyup==0.3.0`) e não há segredos. O CI existente (`ci/github-actions-ci.yml`) só roda carga do banco e testes; o deploy é feito pelo próprio Community Cloud.

Verificação feita antes da entrega: `pip install -r requirements-dev.txt`, `pytest` com 11 testes passando (com o banco atual e com o banco regenerado), e `streamlit run app.py` em modo headless respondendo 200 em `/` e `ok` em `/_stcore/health`. No Chromium, a página inicial mostra "30 títulos encontrados", `?p=Livro` mostra 15 livros com filtro de categoria, sem exceções.

### Limitações do plano gratuito

- O app dorme depois de um período sem acesso; o primeiro visitante vê a tela "This app has gone to sleep" e clica para acordar (cerca de 1 minuto).
- Recursos limitados (cerca de 1 GB de memória): suficiente para este catálogo.
- O repositório precisa ser público (ou você autoriza o acesso da conta Streamlit a repositórios privados).
- A capa `assets/freeguy.jpg` tem 4,7 MB e vai embutida em base64 no card (cerca de 6 MB na página inicial). Não impede o deploy, mas deixa a primeira carga lenta: ver decisões pendentes.

### Pontos de atenção (segurança e conteúdo)

- Não há segredos nem dados pessoais: o app não tem login nem formulário, e o banco é somente leitura.
- Capas e sinopses são de obras de terceiros, usadas em projeto de estudo.

## 3. Solução (passo a passo)

### Etapa 1 · Validar localmente (Git Bash)

1. `cd /c/ambiente-projeto/ser-mvp/biblioteca`
2. `python -m venv .venv && source .venv/Scripts/activate`
3. `pip install -r requirements-dev.txt`
4. Opcional, recomendado: `python scripts/popular_banco.py` (recria o banco com `CHECK` de tipo e índice; esperado: "Banco gerado em database/cine_livro.db com 30 itens.")
5. `pytest` (esperado: 11 testes passando)
6. `streamlit run app.py` e conferir `http://localhost:8501`: busca, páginas Filmes e Livros e filtro de categoria.

### Etapa 2 · Subir para o GitHub (branch `main`)

1. Apagar o que foi substituído:
   `git rm scripts/init_sqlite.py`
   `git rm -r src/__pycache__` (arquivos .pyc; o `.gitignore` novo já ignora)
2. Ativar o CI (a pasta `.github` é protegida para a ferramenta que preparou o projeto, então o arquivo veio em `ci/`):
   `mkdir -p .github/workflows && mv ci/github-actions-ci.yml .github/workflows/ci.yml && rmdir ci`
3. `git status` (não podem aparecer `.venv/` nem `__pycache__/`; se regenerou o banco, `database/cine_livro.db` aparece como modificado e deve ir no commit)
4. `git add -A`
5. `git commit -m "docs(deploy): publicação no Streamlit Community Cloud"`
6. `git push origin main`
7. Aba **Actions**: o CI precisa ficar verde.

### Etapa 3 · Criar o app no Streamlit Community Cloud

1. Entrar em **share.streamlit.io** com a conta do GitHub e autorizar o acesso aos repositórios.
2. **Create app → Deploy a public app from GitHub** (em versões antigas do painel: **New app**).
3. Preencher:
   - **Repository**: `douglasabnovato/biblioteca`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (opcional): por exemplo `cinelivro` → `https://cinelivro.streamlit.app` (se estiver ocupado, escolha outro)
4. **Advanced settings → Python version**: `3.12` (a mesma do CI). **Secrets**: deixar vazio, o app não usa segredos.
5. **Deploy** e acompanhar o log até aparecer o app (2 a 5 min na primeira vez, por causa da instalação do Streamlit).

### Etapa 4 · Conferir no ar

1. A página inicial mostra "30 títulos encontrados", agrupados em Ação, Comédia, Ficção Científica, Romance e Terror, com capas.
2. Digitar "dracula" na busca encontra "Drácula" (sem acento e sem maiúsculas).
3. **Livros** mostra só livros e o filtro de categoria; escolher "Terror" deixa só essa categoria.
4. `?p=<script>` na URL volta para o Início.
5. Um push na `main` republica sozinho (conferir em **Manage app → logs**).

### Etapa 5 · Fechar

1. No GitHub, **About → Website**: colar a URL do app (por exemplo `https://cinelivro.streamlit.app`) e, se for diferente, corrigir a URL na seção "Em produção" do `readme.md`.
