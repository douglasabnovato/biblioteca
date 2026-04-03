import streamlit as st
from PIL import Image
from st_keyup import st_keyup
from src.backend import buscar_dados

st.set_page_config(layout="wide", page_title="Cine&Livro")

# Carregar CSS (Frontend)
with open("src/styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Navegação e busca
query_params = st.query_params
navegacao = query_params.get("p", "Home")

# Navbar HTML
st.markdown(f"""
    <div class="nav-custom">
        <div class="nav-item"><a href="/?p=Home" target="_self">Home</a></div>
        <div class="nav-item"><a href="/?p=Filme" target="_self">🎬 Filmes</a></div>
        <div class="nav-item"><a href="/?p=Livro" target="_self">📚 Livros</a></div>
    </div>
""", unsafe_allow_html=True)

st.title("🎬📚 Cine&Livro")

# Adicione este container para garantir o espaçamento correto
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# A mágica acontece aqui:
search = st_keyup(
    label="Pesquisar...", 
    placeholder="🔍 Pesquisar...", 
    key="search_input",
    label_visibility="collapsed" 
)

st.markdown('</div>', unsafe_allow_html=True)

# Filtro de categoria (Frontend UI)
categoria_sel = "Todas"
if navegacao != "Home":
    categorias = ["Todas", "Ação", "Comédia", "Ficção Científica", "Romance", "Terror"]
    categoria_sel = st.selectbox("Filtrar por categoria", categorias)

# CHAMADA AO BACKEND
itens = buscar_dados(tipo=navegacao, categoria=categoria_sel, busca=search)

# Renderização dos Cards (Frontend)
st.divider()

if itens:
    # 1. Agrupar itens por categoria
    categorias_encontradas = {}
    for item in itens:
        cat = item['categoria']
        if cat not in categorias_encontradas:
            categorias_encontradas[cat] = []
        categorias_encontradas[cat].append(item)

    # 2. Iterar sobre cada categoria e criar o cabeçalho
    for categoria, lista_itens in categorias_encontradas.items():
        st.subheader(f"{categoria}")
        
        # 3. Renderizar os cards em colunas (3 por linha)
        for i in range(0, len(lista_itens), 3):
            cols = st.columns(3)
            for j, item in enumerate(lista_itens[i:i+3]):
                with cols[j]:
                    # Verificação de segurança para imagem
                    if item.get('imagem'):
                        st.image(item['imagem'], use_container_width=True)
                    
                    st.markdown(f"""
                    <div class="card">
                        <h3>{item['titulo']}</h3>
                        <p>{item['descricao']}</p>
                        <span class="badge">{item['tipo']}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.write("---") 
else:
    st.info(f"Nenhum resultado encontrado para: '{search}'")