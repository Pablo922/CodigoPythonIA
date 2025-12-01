import streamlit as st
from agente_ia import AgenteProductividad

# --- 1. CONFIGURACIÓN DEL PROYECTO ---
st.set_page_config(
    page_title="Agente de Productividad",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS CSS PROFESIONALES (Minimalismo Dark) ---
st.markdown("""
<style>
    /* Fuente oficial y colores base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    .stApp {
        background-color: #0E0E0E; /* Negro puro, más elegante */
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }

    /* Ocultar elementos de marca de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* --- SIDEBAR --- */
    section[data-testid="stSidebar"] {
        background-color: #161616; /* Ligeramente más claro que el fondo */
        border-right: 1px solid #2A2A2A;
    }

    /* --- BOTONES DE SUGERENCIA (PANTALLA INICIO) --- */
    /* Convertimos botones estándar en tarjetas clicables */
    div.stButton > button {
        background-color: #1E1E1E;
        color: #C0C0C0;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        height: auto;
        min-height: 100px;
        width: 100%;
        text-align: left;
        transition: all 0.2s ease-in-out;
    }
    
    div.stButton > button:hover {
        background-color: #2D2D2D;
        border-color: #4CAF50; /* Un toque verde sutil al pasar el mouse */
        color: #FFFFFF;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    /* --- INPUT DE CHAT --- */
    .stChatInput textarea {
        background-color: #1E1E1E !important;
        border: 1px solid #333 !important;
        color: white !important;
        border-radius: 12px !important;
    }
    
    /* --- MENSAJES --- */
    /* Ajuste para que los iconos no se vean pegados */
    .stChatMessage {
        padding: 1rem;
    }
    
    /* Título de Bienvenida */
    .welcome-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #FFFFFF 0%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .welcome-subtitle {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 3rem;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE ESTADO (Cerebro de la App) ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

def procesar_entrada(texto):
    """Función central para manejar cualquier input (chat o botones)"""
    # 1. Guardar mensaje del usuario
    st.session_state.mensajes.append({"role": "user", "content": texto})
    
    # 2. Generar respuesta (con manejo de errores visual)
    try:
        # Instanciamos el agente aquí para asegurar frescura
        agente = AgenteProductividad()
        respuesta = agente.consultar(texto)
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
    except Exception as e:
        st.session_state.mensajes.append({"role": "assistant", "content": f"⚠️ **Error del Sistema:** {str(e)}"})

def nuevo_chat():
    st.session_state.mensajes = []

# --- 4. BARRA LATERAL (Navegación) ---
with st.sidebar:
    st.markdown("### ⚡ Panel de Control")
    
    # Botón Principal
    if st.button("＋ Nuevo Chat", use_container_width=True, type="primary"):
        nuevo_chat()
        st.rerun()
    
    st.divider()
    
    # Información del Agente
    st.caption("ESTADO DEL SISTEMA")
    st.success("● API Conectada")
    st.caption("MODELO")
    st.info("Gemini Pro / Flash")
    
    st.divider()
    st.markdown("Made with Python & Streamlit")

# --- 5. ÁREA PRINCIPAL (La Interfaz) ---

# CASO A: CHAT VACÍO -> Mostrar Bienvenida "Clean"
if not st.session_state.mensajes:
    # Centramos el contenido
    col_spacer, col_content, col_spacer2 = st.columns([1, 4, 1])
    
    with col_content:
        st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True) # Espacio vertical
        st.markdown('<h1 class="welcome-title">Hola, Usuario</h1>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-subtitle">¿Qué quieres lograr hoy? Selecciona una opción rápida o escribe abajo.</p>', unsafe_allow_html=True)
        
        # Grid de opciones rápidas (Botones funcionales)
        c1, c2, c3 = st.columns(3)
        
        with c1:
            if st.button("🚀 Priorizar mis tareas\n\nOrganiza mi lista pendiente"):
                procesar_entrada("Tengo muchas cosas que hacer y no sé por dónde empezar. Ayúdame a priorizar.")
                st.rerun()
                
        with c2:
            if st.button("📧 Redactar correo\n\nPara un cliente o profesor"):
                procesar_entrada("Ayúdame a redactar un correo formal y profesional.")
                st.rerun()
                
        with c3:
            if st.button("🧠 Resumir texto\n\nExtraer puntos clave"):
                procesar_entrada("Voy a pegarte un texto largo y necesito que extraigas los puntos clave.")
                st.rerun()

# CASO B: CHAT ACTIVO -> Mostrar Historial
else:
    for msj in st.session_state.mensajes:
        if msj["role"] == "assistant":
            with st.chat_message("assistant", avatar="⚡"):
                st.markdown(msj["content"])
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(msj["content"])

# --- 6. INPUT DE CHAT (Siempre visible) ---
if prompt := st.chat_input("Escribe tu objetivo, tarea o duda aquí..."):
    procesar_entrada(prompt)
    st.rerun()