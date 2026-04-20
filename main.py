import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# 1. Налаштування темного дизайну та шрифтів
st.set_page_config(page_title="Network Analysis System", layout="wide")

st.markdown("""
    <style>
    /* Підключення шрифту Inter для технологічного вигляду */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Глобальні налаштування кольорів та шрифтів */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117; /* Глибокий темний фон */
        color: #E0E0E0;
    }

    /* Стилізація головного заголовка */
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #00C6FF, #0072FF); /* Градієнтний синій */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 30px;
        letter-spacing: -1px;
    }

    /* Стилізація карток для метрик */
    .metric-card {
        background-color: #1A1C23;
        border: 1px solid #2D2E3A;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #0072FF;
    }
    .metric-label {
        color: #888;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        color: #00C6FF;
        font-size: 1.4rem;
        font-weight: 600;
    }

    /* Кастомізація кнопок */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #0072FF !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Використання кастомного класу для заголовка
st.markdown('<h1 class="main-title">Network Analysis Pro</h1>', unsafe_allow_html=True)

# Ініціалізація графа
if 'G' not in st.session_state:
    G = nx.Graph()
    G.add_edges_from([
        ("Gateway", "Main_Switch"), ("Main_Switch", "Server_Farm"),
        ("Main_Switch", "User_VLAN"), ("Server_Farm", "DB_Cluster"),
        ("User_VLAN", "Workstation_1"), ("DB_Cluster", "Gateway")
    ])
    st.session_state.G = G

# Навігація через вкладки
tab1, tab2 = st.tabs(["📊 Analytics Engine", "🌐 Visual Infrastructure"])

with tab1:
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("### 🛠 Configuration")
        node_a = st.text_input("Source Node")
        node_b = st.text_input("Target Node")
        if st.button("Deploy Connection"):
            if node_a and node_b:
                st.session_state.G.add_edge(node_a, node_b)
                st.rerun()

    with col2:
        st.markdown("### 📉 Centrality Metrics")
        centrality = nx.degree_centrality(st.session_state.G)
        
        # Вивід результатів через кастомні HTML-картки
        for node, val in sorted(centrality.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Node Identifier: {node}</div>
                    <div class="metric-value">Centrality Index: {val:.4f}</div>
                </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🕸 Infrastructure Visualization")
    # Налаштування візуалізації (темна тема для графа)
    net = Network(height="600px", width="100%", bgcolor="#0E1117", font_color="#E0E0E0")
    
    for node in st.session_state.G.nodes():
        score = centrality[node]
        # Колір вузла залежить від його важливості (від синього до яскраво-блакитного)
        net.add_node(node, label=node, size=score*200, color="#00C6FF", border_width=2, font={'size': 18})
        
    net.from_nx(st.session_state.G)
    net.toggle_physics(True)
    
    # Використання тимчасового файлу для відображення
    net.save_graph("network_pro.html")
    with open("network_pro.html", 'r', encoding='utf-8') as f:
        components.html(f.read(), height=650)
