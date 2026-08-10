import streamlit as st
from PIL import Image
from st_keyup import st_keyup
from src.backend import buscar_dados

# Configuração da página em modo wide
st.set_page_config(layout="wide", page_title="Cine&Livro")

# Carregar CSS atualizado da nova estrutura (Fase 1 e Fase 2)
with open("src/styles/main.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Navegação e busca via parâmetros de URL
query_params = st.query_params
navegacao = query_params.get("p", "Home")

# Navbar HTML Fixa Superior (Glassmorphism)
st.markdown(f"""
    <div class="nav-custom">
        <div class="nav-item"><a href="/?p=Home" target="_self">Home</a></div>
        <div class="nav-item"><a href="/?p=Filme" target="_self">🎬 Filmes</a></div>
        <div class="nav-item"><a href="/?p=Livro" target="_self">📚 Livros</a></div>
    </div>
""", unsafe_allow_html=True)

# Container principal para compensar a navbar fixa
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

st.title("🎬📚 Cine&Livro")

# Campo de busca em tempo real com st_keyup
search = st_keyup(
    label="Pesquisar...", 
    placeholder="🔍 Pesquisar por título...", 
    key="search_input",
    label_visibility="collapsed" 
)

# Filtro de categoria condicional (UI)
categoria_sel = "Todas"
if navegacao != "Home":
    categorias = ["Todas", "Ação", "Comédia", "Ficção Científica", "Romance", "Terror"]
    categoria_sel = st.selectbox("Filtrar por categoria", categorias)

# Chamada ao Backend centralizado
itens = buscar_dados(tipo=navegacao, categoria=categoria_sel, busca=search)

st.divider()

# Renderização dos Cards (Frontend Responsivo)
if itens:
    # 1. Agrupar itens por categoria encontrada
    categorias_encontradas = {}
    for item in itens:
        cat = item['categoria']
        if cat not in categorias_encontradas:
            categorias_encontradas[cat] = []
        categorias_encontradas[cat].append(item)

    # 2. Iterar sobre cada categoria para criar as seções
    for categoria, lista_itens in categorias_encontradas.items():
        st.subheader(f"📌 {categoria}")
        
        # 3. Renderizar os cards em colunas (3 por linha) com responsividade
        for i in range(0, len(lista_itens), 3):
            cols = st.columns(3)
            for j, item in enumerate(lista_itens[i:i+3]):
                with cols[j]:
                    # Exibição segura da imagem com o padrão atualizado
                    if item.get('imagem'):
                        st.image(item['imagem'], width='stretch')
                    
                    # Definição de classe dinâmica para a badge baseada no tipo
                    tipo_item = item.get('tipo', 'Filme')
                    badge_class = "badge livro" if tipo_item == "Livro" else "badge"
                    
                    # Renderização estruturada do Card HTML
                    st.markdown(f"""
                    <div class="card">
                        <div>
                            <h3>{item['titulo']}</h3>
                            <p>{item['descricao']}</p>
                        </div>
                        <span class="{badge_class}">{tipo_item}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.write("---") 
else:
    st.info(f"Nenhum resultado encontrado para: '{search}'")

st.markdown('</div>', unsafe_allow_html=True)