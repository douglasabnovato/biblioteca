# 🎬📚 Cine&Livro

Uma experiência imersiva e moderna para descoberta e recomendação centralizada de filmes e livros, combinando alta performance, design elegante e interatividade em tempo real.

## 🚀 Em produção

- URL: https://cinelivro.streamlit.app (sugerida; confirme a escolhida no Streamlit)
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
pytest                            # 11 testes (dados, carga, HTML e interface)
```

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