# Análise — Cine&Livro (biblioteca)

## 1. Especificação

Catálogo de 30 filmes e livros (5 categorias × 2 tipos) em Streamlit + SQLite, com busca em tempo real e filtro por categoria. Stack Python mantida por decisão do usuário.

| ID | Requisito | Antes | Depois |
|---|---|---|---|
| RF01 | Navegar Início / Filmes / Livros | ✅ | ✅ (página inválida tratada) |
| RF02 | Buscar por título enquanto digita | ✅ exige acento exato | ✅ sem acento, com debounce |
| RF03 | Filtrar por categoria | ✅ lista fixa no código | ✅ lida do banco |
| RF04 | Popular o banco a partir do JSON | ❌ scripts falhavam | ✅ com validação |

## 2. Defeitos encontrados

| # | Severidade | Defeito | Referência |
|---|---|---|---|
| D1 | Alta | `popular_banco.py` e `init_sqlite.py` abrem `itens.json` na raiz, mas o arquivo está em `scripts/` → carga impossível | — |
| D2 | Média | Título e descrição interpolados em HTML com `unsafe_allow_html` sem escape | OWASP A05:2025 |
| D3 | Média | Banco ausente → traceback na tela | OWASP A10:2025 |
| D4 | Média | Capas sem texto alternativo; rótulos dos campos com baixo contraste | WCAG 2.2 1.1.1, 1.4.3 |
| D5 | Baixa | Busca exige acento exato; categorias fixas no código; `__pycache__` versionado; requirements com 40 pacotes congelados | — |

## 3. Baseline automatizado

| Verificação | Antes | Depois |
|---|---|---|
| App executa | ✅ | ✅ |
| Carga do banco | ❌ | ✅ |
| Testes | 0 | 11 (pytest + AppTest) |
| axe-core | não medido | 0 violações |

## Rubrica v2 (grupo fullstack)

Aprovação: média ponderada ≥ 7,0 **e** C1 e C4 (eliminatórios) ≥ 5. Regras: nota sem evidência vale no máximo 6; C1 limitado a 7 para parte não executada de ponta a ponta; C9 ≥ 8 só com URL publicada e CI verde.

| # | Critério | Referência | Peso | Antes | Depois | Evidência | Justificativa |
|---|---|---|---|---|---|---|---|
| C1 | Núcleo de valor | MVP (Ries); SWEBOK Requirements | 16% | 7 | 8 | streamlit run + Chromium: Início, Filmes e Livros com filtro | Já funcionava; ganhou busca sem acento e página inválida tratada |
| C2 | Estados e condições excepcionais | Nielsen; OWASP A10:2025 | 8% | 3 | 7 | mensagem se o banco faltar; busca sem resultado; fallback da busca | Banco ausente derrubava a página com traceback |
| C3 | Acessibilidade | WCAG 2.2 AA (axe-core) | 7% | 4 | 8 | axe-core 0 (Início e Livros); capas com alt | Capas via st.image sem texto alternativo; navegação com emojis lidos pelo leitor de tela |
| C4 | Segurança e privacidade | OWASP Top 10:2025 / ASVS 5.0 N1 | 14% | 5 | 8 | HTML dos cards com escape (teste com <script>); banco aberto só leitura | Título/descrição entravam em HTML sem escape (unsafe_allow_html) |
| C5 | Dados | 3FN / ACID / fonte única | 10% | 4 | 8 | script de carga valida JSON e imagens; CHECK de tipo e índice | Os dois scripts de carga procuravam itens.json na raiz e falhavam (o arquivo está em scripts/) |
| C6 | Testes | Pirâmide de testes; SWEBOK Testing | 9% | 0 | 8 | pytest 11 (dados, carga, HTML e AppTest da interface) | Não havia testes |
| C7 | Qualidade de código | SOLID / camadas; SWEBOK Construction | 7% | 5 | 8 | backend/render/app separados; categorias vindas do banco | Lista de categorias fixa no código |
| C8 | Desempenho | Complexidade; Core Web Vitals | 5% | 5 | 7 | cache de 10 min nas consultas; busca com debounce | Uma consulta nova a cada tecla |
| C9 | Operação | 12-Factor; DORA | 7% | 3 | 7 | requirements enxuto; CI em ci/; Streamlit Community Cloud gratuito | __pycache__ versionado; requirements com 40 pacotes congelados |
| C10 | Documentação | README como contrato | 5% | 5 | 8 | readme com como rodar, testar e publicar | README sem instruções de execução |
| C11 | Produto e evidência | Cagan (4 riscos); Torres | 7% | 6 | 7 | busca sem acento ("dracula" acha "Drácula") | Sem métrica de uso |
| C12 | Sustentabilidade técnica | OWASP A03:2025; SWEBOK Maintenance | 5% | 4 | 8 | streamlit 1.64 e só 2 dependências diretas | Dependências transitivas fixadas manualmente |

**Média ponderada:** antes **4,42** (REPROVADO) → depois **7,73** (APROVADO).

