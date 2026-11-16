> **Projeto de estudo (N1).** Estado conferido em 16/11/2026. Critérios em [docs/MVP.md](docs/MVP.md).

## Estado e próximos passos (ciclo de 15/11/2026)

Sem link publicado que responda: em 16/11/2026, https://biblioteca-cine-livros.streamlit.app/ responde HTTP 303 e redireciona para o login do Streamlit, porque o app está privado. Tornar público é do responsável ([#4](https://github.com/douglasabnovato/biblioteca/issues/4)); o passo a passo está em [docs/DEPLOY.md](docs/DEPLOY.md). Para ver o catálogo, rode localmente (seção "Como executar").

**Finalizado: sim**, com 10 de 10 critérios aplicáveis atendidos (antes, 9 de 10). A `main` está protegida (exige PR e os jobs `app` e `tela` verdes).

**O que foi feito**

- Ciclo de 15/11/2026 ([PR #17](https://github.com/douglasabnovato/biblioteca/pull/17)):
  - Segurança: Streamlit 1.64.0 → 1.67.0 e Pillow 13, que corrige vulnerabilidades da 12.x; `pip-audit` no CI.
  - Página de detalhe de cada título, com link para a obra no outro formato ([#7](https://github.com/douglasabnovato/biblioteca/issues/7)).
  - axe-core com 0 violações no claro e no escuro, incluindo o detalhe; Esc no filtro ([#11](https://github.com/douglasabnovato/biblioteca/issues/11)). Tema fixo em `.streamlit/config.toml`.
  - Testes de banco indisponível e de lista vazia, que o MVP citava e não existiam.
  - Hipótese com meta e "saberemos quando"; passo a passo de publicação revisto.
- Ciclo de 07/11/2026 ([PR #13](https://github.com/douglasabnovato/biblioteca/pull/13)): job `tela` no CI com axe e teclado ([#6](https://github.com/douglasabnovato/biblioteca/issues/6)).
- Ciclo de 03/11/2026 ([PR #9](https://github.com/douglasabnovato/biblioteca/pull/9)): cards mostram a obra no outro formato.

**O que queremos fazer**

- [#4](https://github.com/douglasabnovato/biblioteca/issues/4) Tornar o app do Streamlit público (responsável).
- [#12](https://github.com/douglasabnovato/biblioteca/issues/12) Caminhos longos no Windows (responsável; há alternativa com venv em caminho curto).
- [#8](https://github.com/douglasabnovato/biblioteca/issues/8) Ampliar o catálogo com mais pares de filme e livro.
- [#18](https://github.com/douglasabnovato/biblioteca/issues/18) Testar o aviso de carregamento do catálogo.
- [#19](https://github.com/douglasabnovato/biblioteca/issues/19) Tirar o link "Link to heading" dos títulos dos cards.
- [#20](https://github.com/douglasabnovato/biblioteca/issues/20) Atualizar o pytest para a versão 9.
- [#21](https://github.com/douglasabnovato/biblioteca/issues/21) Fixar as versões do Playwright e do axe no teste de tela.
- [#22](https://github.com/douglasabnovato/biblioteca/issues/22) Reduzir o peso das capas na página inicial.
- [#23](https://github.com/douglasabnovato/biblioteca/issues/23) Avaliar o `streamlit-keyup` 1.0.

**Onde está a documentação**

- [docs/MVP.md](docs/MVP.md): estado de cada critério, com evidência e data.
- [docs/PLANO-DE-ACAO.md](docs/PLANO-DE-ACAO.md): plano de cada ciclo, pesquisa com fontes e backlog.
- [docs/DEPLOY.md](docs/DEPLOY.md): publicação no Streamlit Community Cloud, passo a passo.

# 🎬📚 Cine&Livro

Uma experiência imersiva e moderna para descoberta e recomendação centralizada de filmes e livros, combinando alta performance, design elegante e interatividade em tempo real.

## 🚀 Em produção

- URL: https://biblioteca-cine-livros.streamlit.app/ (pede login em 16/11/2026: app privado, ver #4)
- Hospedagem: Streamlit Community Cloud (gratuito), republica a cada push na `main`
- Passo a passo: [docs/DEPLOY.md](docs/DEPLOY.md)

---

## 🌟 Sobre o Projeto

O **Cine&Livro** é uma aplicação web desenvolvida para proporcionar aos usuários uma navegação fluida por um catálogo selecionado de obras cinematográficas e literárias. Com uma arquitetura limpa e moderna inspirada nas melhores plataformas de streaming, o sistema oferece filtros inteligentes, busca instantânea e um design refinado em tema escuro com efeitos visuais sofisticados.

---

## ✨ Principais Funcionalidades

* **Navegação Dinâmica por Categorias:** Alterne instantaneamente entre visões gerais, filmes e livros organizados por gêneros (Ação, Comédia, Ficção Científica, Romance e Terror).
* **Busca Instantânea em Tempo Real:** Localize títulos de forma dinâmica e imediata enquanto digita na barra de pesquisa integrada.
* **Armazenamento Robusto e Eficiente:** Gerenciamento de dados centralizado em banco de dados relacional SQLite, populado de forma automatizada por arquivos estruturados.
* **Interface Totalmente Responsiva:** Layout adaptado e fluido para diferentes tamanhos de tela (smartphones, tablets e desktops).

---

## 🛠️ Arquitetura e Tecnologias

O projeto foi construído seguindo rigorosos padrões de separação de responsabilidades e modularidade:

* **Frontend:** Streamlit com customizações avançadas em CSS moderno, fontes tipográficas refinadas e animações suaves de elevação (*hover*).
* **Backend:** Camada dedicada de acesso a dados em Python utilizando SQLite com consultas parametrizadas seguras.
* **Banco de Dados:** SQLite integrado na arquitetura local do sistema.

---

## ▶️ Como executar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (Linux/macOS: source .venv/bin/activate)
pip install -r requirements-dev.txt
python scripts/popular_banco.py   # (re)gera database/cine_livro.db a partir de scripts/itens.json
streamlit run app.py              # http://localhost:8501
pytest                            # 24 testes (dados, carga, HTML e interface)
```

Teste de tela, com o app no ar (`streamlit run app.py` em outro terminal):

```bash
pip install -r requirements-tela.txt
python -m playwright install chromium
pytest tela                       # 12 testes: axe-core (claro e escuro), fluxo, detalhe e teclado num navegador real
```

No Windows, o `pip` com Streamlit pode falhar por caminho longo (#12). Criar a venv numa pasta de caminho curto (ex.: `C:`) resolveu em 16/11/2026. O CI roda os dois conjuntos em todo push e PR. Com o app em outra porta, defina `APP_URL=http://localhost:<porta>` antes de `pytest tela`.

Para adicionar um título: inclua-o em `scripts/itens.json` (a capa vai em `assets/`) e rode o script de carga — ele avisa se faltar campo ou imagem.

**Publicação gratuita:** [Streamlit Community Cloud](https://streamlit.io/cloud). O app já existe e está privado; o passo a passo para torná-lo público ou recriá-lo está em [docs/DEPLOY.md](docs/DEPLOY.md).

## ✅ Versão 1.1 (revisão de qualidade)

- Busca sem diferenciar acentos e maiúsculas ("dracula" encontra "Drácula")
- Categorias lidas do banco; página inválida volta para o Início
- Conteúdo dos cards com escape de HTML; banco aberto em modo leitura
- Capas com texto alternativo, rótulos legíveis e foco visível (axe-core sem violações)
- Script de carga único e funcional (os dois anteriores procuravam o JSON no lugar errado)
- 11 testes automatizados; dependências reduzidas a `streamlit` e `streamlit-keyup`

Detalhes em [docs/ANALISE.md](docs/ANALISE.md), [docs/ARQUITETURA.md](docs/ARQUITETURA.md) e [docs/PLANO-DE-ACAO.md](docs/PLANO-DE-ACAO.md).

---

## 🚀 Contribuições e Próximos Passos

Este ecossistema está em constante evolução. Contribuições futuras são bem-vindas nas seguintes frentes:

* **Design do Footer:** Aprimoramento visual e estrutural do rodapé da aplicação.
* **Botão CTA em Destaque:** Implementação de chamada para ação na seção inicial para engajamento do usuário.
* **QA de Responsividade:** Validação e refinamento contínuo da experiência em dispositivos móveis.
