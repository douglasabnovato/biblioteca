> **Projeto de estudo (N1).** Estado conferido em 09/11/2026. Critérios em [docs/MVP.md](docs/MVP.md).

## Estado e próximos passos (ciclo de 07/11/2026)

Sem link publicado que responda: em 09/11/2026, https://biblioteca-cine-livros.streamlit.app/ responde HTTP 303 e redireciona para o login do Streamlit, porque o app está privado. Tornar público é do responsável ([#4](https://github.com/douglasabnovato/biblioteca/issues/4)). Para ver o catálogo, rode localmente (seção "Como executar").

**Finalizado: sim**, com 9 de 10 critérios aplicáveis atendidos; o que resta (#4) depende do responsável. A `main` está protegida desde 10/11/2026 (exige PR e bloqueia force push).

**O que foi feito em 09/11/2026**

- Job `tela` no CI: sobe o app, roda o axe-core em Início, Filmes e Livros e percorre busca, menu e filtro num Chromium real, também pelo teclado ([#6](https://github.com/douglasabnovato/biblioteca/issues/6)).
- O teste achou e o ciclo corrigiu o contraste da contagem de resultados (3,68:1) e a ordem dos títulos.

**O que queremos fazer**

- [#4](https://github.com/douglasabnovato/biblioteca/issues/4) Tornar o app do Streamlit público ou corrigir o link (responsável).
- [#5](https://github.com/douglasabnovato/biblioteca/issues/5) Proteger a `main`: feito em 10/11/2026 (ruleset `principal-protegida`); a issue fecha no merge da `main`.
- [#12](https://github.com/douglasabnovato/biblioteca/issues/12) Habilitar caminhos longos no Windows para rodar o app localmente (responsável).
- [#7](https://github.com/douglasabnovato/biblioteca/issues/7) Abrir a página de detalhe de cada título.
- [#8](https://github.com/douglasabnovato/biblioteca/issues/8) Ampliar o catálogo com mais pares de filme e livro.
- [#11](https://github.com/douglasabnovato/biblioteca/issues/11) Conteúdo dentro de landmarks (regra `region` do axe).

**Onde está a documentação**

- [docs/MVP.md](docs/MVP.md): estado de cada critério, com evidência e data.
- [docs/PLANO-DE-ACAO.md](docs/PLANO-DE-ACAO.md): plano do ciclo, pesquisa e backlog.

# 🎬📚 Cine&Livro

Uma experiência imersiva e moderna para descoberta e recomendação centralizada de filmes e livros, combinando alta performance, design elegante e interatividade em tempo real.

## 🚀 Em produção

- URL: https://biblioteca-cine-livros.streamlit.app/ (pede login em 06/11/2026: app privado, ver #4)
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
pytest                            # 15 testes (dados, carga, HTML e interface)
```

Teste de tela, com o app no ar (`streamlit run app.py` em outro terminal):

```bash
pip install -r requirements-tela.txt
python -m playwright install chromium
pytest tela                       # axe-core, fluxo principal e teclado num navegador real
```

No Windows, o `pip` com Streamlit pode falhar por caminho longo (#12); o CI roda os dois conjuntos em todo push.

Para adicionar um título: inclua-o em `scripts/itens.json` (a capa vai em `assets/`) e rode o script de carga — ele avisa se faltar campo ou imagem.

**Publicação gratuita:** [Streamlit Community Cloud](https://streamlit.io/cloud) → Create app → este repositório, branch `main`, `app.py`, Python 3.12 em Advanced settings. Passo a passo em [docs/DEPLOY.md](docs/DEPLOY.md).

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
