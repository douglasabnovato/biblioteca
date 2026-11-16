# Deploy · Cine&Livro

Como o catálogo fica no ar, de graça, no Streamlit Community Cloud. Revisto em 16/11/2026 (ciclo de 15/11/2026).

## 1. Estado em 16/11/2026

| Item | Situação | Evidência |
|---|---|---|
| App criado no Community Cloud | Sim, mas **privado** | `curl -s -o /dev/null -w "%{http_code}" https://biblioteca-cine-livros.streamlit.app/` devolve `303` para `share.streamlit.io/-/auth/app` (pede login) |
| Link no "About" do repositório | `https://biblioteca-cine-livros.streamlit.app/` | `gh repo view --json homepageUrl` |
| Código pronto para publicar | Sim | CI verde no PR; nenhum segredo; `requirements.txt` com versões fixas |
| Tornar o app público | **Responsável** | Issue [#4](https://github.com/douglasabnovato/biblioteca/issues/4) |

## 2. Por que o Community Cloud

| Opção | Resultado |
|---|---|
| **Streamlit Community Cloud (escolhida)** | Gratuito, feito para Streamlit, instala o `requirements.txt` e republica a cada push na branch escolhida |
| GitHub Pages | Não roda Python: só arquivos estáticos |
| Render (plano gratuito) | Funciona, mas pede comando de início e porta, e dorme após 15 min; sem ganho aqui |
| Hugging Face Spaces | Gratuito, mas é mais uma conta e mais um repositório |

Não há `render.yaml` nem workflow do Pages: o Community Cloud lê o repositório direto e não precisa de arquivo de deploy.

## 3. O que o Community Cloud usa do repositório

| Arquivo | Para quê |
|---|---|
| `app.py` | Ponto de entrada (Main file path) |
| `requirements.txt` | `streamlit==1.67.0`, `streamlit-keyup==0.3.0` e `pillow>=13.0.0,<14` (a 12.x tem vulnerabilidades) |
| `.streamlit/config.toml` | Tema fixo `base = "dark"`, o mesmo do CSS do projeto |
| `database/cine_livro.db` | Catálogo versionado (30 títulos), aberto em modo leitura |
| `assets/` | Capas, embutidas nos cards |

Sem segredos: o app não tem login, formulário nem chave de serviço externo. O campo **Secrets** fica vazio.

**Banco em produção.** O disco do Community Cloud é temporário, mas o app não grava nada. A cada reinício o banco vem do repositório. Para mudar o catálogo: editar `scripts/itens.json` (capa em `assets/`), rodar `python scripts/popular_banco.py` e fazer commit do `.db`. O CI recria o banco a partir do JSON antes dos testes; um JSON inválido quebra o CI antes de chegar ao ar.

## 4. Passo a passo do responsável

### 4.1 Tornar o app público (issue #4)

1. Entrar em **https://share.streamlit.io** com a conta do GitHub dona do repositório.
2. Na lista **My apps**, achar `biblioteca-cine-livros`.
3. Clicar nos **três pontos (⋮)** ao lado do app → **Settings**.
4. Aba **Sharing** → em **Who can view this app**, escolher **This app is public and searchable** → **Save**.
   - Outro caminho: abrir o app e clicar em **Share** (canto superior direito) → **Make this app public**.
5. Conferir num terminal: `curl -s -o /dev/null -w "%{http_code}" https://biblioteca-cine-livros.streamlit.app/` deve devolver `200`.

### 4.2 Conferir a versão do Python e a branch

1. Ainda em **Settings**, aba **General**: a branch deve ser `main` e o arquivo `app.py`.
2. A versão do Python deve ser **3.12**, a mesma do CI. O painel só troca a versão apagando e recriando o app (**Delete app** e depois **Create app**, com os mesmos dados de 4.3). Se já for 3.12, não mexer.

### 4.3 Se precisar recriar o app

1. **Create app** → **Deploy a public app from GitHub**.
2. **Repository**: `douglasabnovato/biblioteca`. **Branch**: `main`. **Main file path**: `app.py`.
3. **App URL**: `biblioteca-cine-livros` (o mesmo de hoje, para o link do README seguir valendo).
4. **Advanced settings** → **Python version**: `3.12`. **Secrets**: vazio. **Save**.
5. **Deploy** e acompanhar o log (2 a 5 min na primeira vez).

### 4.4 Depois do merge na `main`

1. O Community Cloud republica sozinho. Para forçar: **⋮ → Reboot app**.
2. Conferir no ar:
   - A página inicial mostra "30 títulos encontrados", agrupados por categoria.
   - Digitar "dracula" na busca acha "Drácula".
   - **Livros** mostra o filtro de categoria; "Terror" deixa só essa categoria.
   - Clicar no título "Percy Jackson e O Ladrão de Raios" abre o detalhe, com link para o livro.
   - `?p=item&id=abc` volta para o Início com o aviso "Título não encontrado".
3. Avisar no PR ou na #4 a data e o código HTTP, para o `docs/MVP.md` registrar.

## 5. Rodar localmente

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (Linux/macOS: source .venv/bin/activate)
pip install -r requirements-dev.txt
python scripts/popular_banco.py
streamlit run app.py            # http://localhost:8501
pytest                          # 22 testes
```

No Windows sem caminhos longos (#12), criar a venv numa pasta de caminho curto (ex.: `C:\v`). Em 16/11/2026, `pip install -r requirements.txt` funcionou assim, com `LongPathsEnabled = 0`.

## 6. Limites do plano gratuito

- O app dorme depois de um tempo sem visita; quem chega vê "This app has gone to sleep" e clica para acordar (cerca de 1 minuto).
- Cerca de 1 GB de memória: sobra para este catálogo.
- A capa `assets/freeguy.jpg` tem 4,7 MB e vai embutida em base64; a primeira carga fica mais lenta. Medir o desempenho não se aplica em N1.

## 7. Fontes

- [Streamlit: share your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app): público × privado e onde trocar.
- [Streamlit: config.toml](https://docs.streamlit.io/develop/api-reference/configuration/config.toml): opção `base` do tema.
