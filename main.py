import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# 1. Налаштування теми та шрифтів через CSS
st.set_page_config(page_title="Network Analysis Pro", layout="wide")

st.markdown("""
    <style>
    /* Підключення шрифту та змінення розміру основного тексту */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 18px; /* Збільшений розмір слів */
    }

    /* Стилізація заголовків */
    h1 {
        color: #1E3A8A !important;
        font-size: 3rem !important;
        text-align: center;
        padding-bottom: 20px;
    }

    /* Картки для метрик */
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid #1E3A8A;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Заголовок
st.title("Аналітична Система Центральності")

# Ініціалізація даних (згідно з вашою дисципліною)
if 'G' not in st.session_state:
    G = nx.Graph()
    G.add_edges_from([
        ("Core_Router", "Switch_Dept1"), ("Core_Router", "Switch_Dept2"),
        ("Switch_Dept1", "PC_User1"), ("Switch_Dept1", "PC_User2"),
        ("Switch_Dept2", "Database_Srv"), ("Database_Srv", "Core_Router")
    ])
    st.session_state.G = G

# Розподіл інтерфейсу на вкладки
tab1, tab2 = st.tabs(["📊 Аналіз та Метрики", "🌐 Інтерактивна Топологія"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Додати новий вузол")
        node_a = st.text_input("Назва вузла A (напр. Firewall)")
        node_b = st.text_input("Назва вузла B (напр. DMZ)")
        if st.button("З'єднати вузли"):
            if node_a and node_b:
                st.session_state.G.add_edge(node_a, node_b)
                st.rerun()

    with col2:
        st.header("Результати обчислень")
        centrality = nx.degree_centrality(st.session_state.G)
        for node, val in sorted(centrality.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"""
                <div class="metric-card">
                    <strong>Вузол:</strong> {node}<br>
                    <strong>Центральність:</strong> {val:.4f}
                </div>
            """, unsafe_allow_html=True)

with tab2:
    st.header("Візуалізація мережевої інфраструктури")
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#1E3A8A")
    
    # Налаштування дизайну графа
    for node in st.session_state.G.nodes():
        score = centrality[node]
        net.add_node(node, label=node, size=score*150, color="#3B82F6", border_width=2)
        
    net.from_nx(st.session_state.G)
    
    # Додавання можливості фізичної взаємодії
    net.toggle_physics(True)
    net.save_graph("network.html")
    
    with open("network.html", 'r', encoding='utf-8') as f:
        components.html(f.read(), height=650)