"""
Chatbot con Groq API - Interfaz Streamlit
Instalación: pip install streamlit groq python-dotenv
Ejecución: streamlit run chatbot_streamlit.py
"""

import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

# Cargar variables de entorno
env_path = r"C:\Users\Gustavo\Desktop\mi_chatbot\.env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")

class ChatAgent:
    
    def __init__(self, model, temperature, system_prompt):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.history = []
        if system_prompt:
            self.history.append({
                "role": "system",
                "content": system_prompt
            })
    
    def chat(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                temperature=self.temperature,
                max_tokens=8192,
            )
            
            assistant_message = response.choices[0].message.content
            
            self.history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            return f"Error: {str(e)}"


st.set_page_config(
    page_title="Chatbot :v",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Fondo general */
    .main {
        background-color: #2b2b2b !important;
        color: white !important;
    }

    /* Mensajes del chat */
    .stChatMessage {
        border-radius: 10px;
        padding: 12px 18px;
        margin: 8px 0;
        max-width: 80%;
        color: white !important;
    }

    /* Usuario: fondo negro */
    .stChatMessage.user {
        background-color: #000000 !important;
        color: #ffffff !important;
        text-align: right;
        align-self: flex-end;
    }

    /* Asistente: fondo gris */
    .stChatMessage.assistant {
        background-color: #3c3c3c !important;
        color: #ffffff !important;
        text-align: left;
        align-self: flex-start;
    }

    /* Forzar texto en blanco en todo */
    .stMarkdown, .stText, .stWrite, .stMarkdown p {
        color: white !important;
    }

    /* Input del chat */
    .stChatInput textarea {
        background-color: #1e1e1e !important;
        color: white !important;
    }

    /* Header */
    .chat-header {
        background: linear-gradient(135deg, #3c3c3c 0%, #1e1e1e 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }

    /* Tarjetas métricas */
    .metric-card {
        background-color: #3c3c3c !important;
        color: white !important;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="chat-header">
        <h1>🤖 Chatbot Inteligente</h1>
        <p>Powered by Groq API | Modelos LLaMA 3.3 & Mixtral</p>
    </div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.image(r"C:\Users\Gustavo\Desktop\mi_chatbot\images\queso.jpg", width=200)
    
    st.title("⚙️ Configuración")
    st.divider()
    

    model_info = {
        "llama-3.3-70b-versatile": "🦙 LLaMA 3.3 70B - El más potente",
        "llama-3.1-70b-versatile": "🦙 LLaMA 3.1 70B - Muy capaz", 
        "llama-3.1-8b-instant": "⚡ LLaMA 3.1 8B - Ultra rápido",
        "mixtral-8x7b-32768": "🔀 Mixtral 8x7B - Contexto largo",
        "gemma2-9b-it": "💎 Gemma2 9B - Compacto"
    }
    
    selected_model = st.selectbox(
        "🎯 Modelo de IA",
        options=list(model_info.keys()),
        format_func=lambda x: model_info[x],
        index=0
    )
    
    # Control de temperatura
    temperature = st.slider(
        "🌡️ Temperatura",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controla la creatividad: 0.0 = preciso, 2.0 = muy creativo"
    )
    

    with st.expander("📝 Prompt del Sistema", expanded=False):
        system_prompt = st.text_area(
            "Define la personalidad del agente",
            value="Eres un asistente amigable, útil y conciso que responde de manera clara y profesional.",
            height=150,
            help="Este mensaje define cómo se comportará el agente"
        )
    
    st.divider()
    
  
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reiniciar", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.agent = None
            st.rerun()
    
    with col2:
        if st.button("✅ Aplicar", use_container_width=True, type="primary"):
            st.session_state.agent = ChatAgent(
                model=selected_model,
                temperature=temperature,
                system_prompt=system_prompt
            )
            st.session_state.config_applied = True
            st.success("Configuración aplicada!")
    
    st.divider()
    
    st.subheader("📊 Estadísticas")
    
    num_messages = len(st.session_state.get("messages", []))
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mensajes", num_messages)
    with col2:
        st.metric("Modelo", selected_model.split("-")[0].upper())
    
    st.divider()
    
    with st.expander("ℹ️ Acerca de", expanded=False):
        st.markdown("""
        **Chatbot con Groq API**
        
        Características:
        - ✅ Modelos de última generación
        - ✅ Respuestas ultra rápidas
        - ✅ 100% gratuito
        - ✅ Privado y seguro
        - ✅ ta bacano
        
        Tecnologías:
        - Framework: Streamlit
        - Proveedor: Groq
        - Lenguaje: Python
        """)
    
    st.markdown("---")
    st.caption(f"Sesión iniciada: {datetime.now().strftime('%H:%M:%S')}")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = ChatAgent(
        model=selected_model,
        temperature=temperature,
        system_prompt=system_prompt
    )

if "config_applied" not in st.session_state:
    st.session_state.config_applied = False

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("💬 Escribe tu mensaje aquí...", key="chat_input"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Pensando..."):
                response = st.session_state.agent.chat(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if len(st.session_state.messages) == 0:
    st.markdown("### 💡 Ejemplos de preguntas:")
    
    col1, col2, col3 = st.columns(3)
    
    example_questions = [
        "Explícame qué es la inteligencia artificial",
        "Dame 5 consejos para ser más productivo",
        "Escribe un poema corto sobre la tecnología"
    ]
    
    for col, question in zip([col1, col2, col3], example_questions):
        with col:
            if st.button(question, use_container_width=True, key=f"example_{question[:10]}"):
                st.session_state.messages.append({"role": "user", "content": question})
                response = st.session_state.agent.chat(question)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

st.divider()
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.markdown(
        "<p style='text-align: center; color: #ccc;'>Desarrollado por Gustavo</p>",
        unsafe_allow_html=True
    )
