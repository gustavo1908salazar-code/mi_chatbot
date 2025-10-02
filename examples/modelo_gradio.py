import os
from groq import Groq
from dotenv import load_dotenv
import gradio as gr

env_path = r"C:\Users\Gustavo\Desktop\mi_chatbot\.env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("⚠️ No se encontró GROQ_API_KEY en el archivo .env")


class ChatAgent:
    """Agente de chat con Groq"""
    
    def __init__(self, model="llama-3.3-70b-versatile", temperature=0.7, system_prompt=""):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.reset_conversation()
    
    def reset_conversation(self):
        """Reiniciar el historial de conversación"""
        self.history = []
        if self.system_prompt:
            self.history.append({
                "role": "system",
                "content": self.system_prompt
            })
    
    def chat(self, message):
        """Enviar mensaje y obtener respuesta"""
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
            return f"❌ Error: {str(e)}"


agent = None


def initialize_agent(model, temperature, system_prompt):
    """Inicializar o reinicializar el agente"""
    global agent
    agent = ChatAgent(
        model=model,
        temperature=temperature,
        system_prompt=system_prompt
    )
    return None  


def chat_function(message, history):
    """Función principal de chat para Gradio"""
    if agent is None:
        return "⚠️ Por favor configura el agente primero en la pestaña de Configuración"
    
    if not message.strip():
        return ""
    
    response = agent.chat(message)
    return response


with gr.Blocks(
    title="Chatbot con Groq API",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="cyan",
    ),
    css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        #chatbot {
            height: 600px !important;
        }
    """
) as demo:
    
    gr.Markdown(
        """
        # 🤖 Chatbot Inteligente con Groq API
        ### Conversaciones potenciadas por IA de última generación
        ---
        """
    )
    
    with gr.Tabs() as tabs:
        
        # TAB 1: CHAT
        with gr.Tab("💬 Chat", id=0):
            
            chatbot = gr.Chatbot(
                label="Conversación",
                height=600,
                show_copy_button=True,
                avatar_images=(None, r"C:\Users\Gustavo\Desktop\mi_chatbot\images\queso.jpg"),
                bubble_full_width=False,
                elem_id="chatbot"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Tu mensaje",
                    placeholder="Escribe tu mensaje aquí y presiona Enter...",
                    lines=2,
                    scale=4,
                    autofocus=True
                )
                
            with gr.Row():
                send_btn = gr.Button("📤 Enviar", variant="primary", scale=1)
                clear_btn = gr.Button("🗑️ Limpiar", variant="secondary", scale=1)
            
            gr.Examples(
                examples=[
                    "Hola, ¿cómo estás?",
                    "Explícame qué es la inteligencia artificial",
                    "Dame 3 consejos para ser más productivo",
                    "Escribe un poema corto sobre la tecnología",
                ],
                inputs=msg,
                label="💡 Ejemplos de preguntas"
            )
        
        with gr.Tab("⚙️ Configuración", id=1):
            
            gr.Markdown("### Personaliza tu agente de IA")
            
            model_dropdown = gr.Dropdown(
                choices=[
                    "llama-3.3-70b-versatile",
                    "llama-3.1-70b-versatile", 
                    "llama-3.1-8b-instant",
                    "mixtral-8x7b-32768",
                    "gemma2-9b-it"
                ],
                value="llama-3.3-70b-versatile",
                label="🎯 Modelo de IA",
                info="Selecciona el modelo que procesará tus mensajes"
            )
            
            temperature_slider = gr.Slider(
                minimum=0.0,
                maximum=2.0,
                value=0.7,
                step=0.1,
                label="🌡️ Temperatura",
                info="Controla la creatividad (0.0 = preciso, 2.0 = muy creativo)"
            )
            
            system_prompt_textbox = gr.Textbox(
                label="📝 Prompt del Sistema",
                placeholder="Ej: Eres un asistente experto en programación...",
                value="Eres un asistente amigable, útil y conciso que responde de manera clara y profesional.",
                lines=4,
                info="Define la personalidad y comportamiento del agente"
            )
            
            apply_btn = gr.Button("✅ Aplicar Configuración", variant="primary", size="lg")
            
            config_status = gr.Markdown("ℹ️ Haz clic en 'Aplicar Configuración' para inicializar el agente")
            
            
            with gr.Accordion("📚 Información sobre los modelos", open=False):
                gr.Markdown(
                    """
                    | Modelo | Descripción | Velocidad | Tokens |
                    |--------|-------------|-----------|---------|
                    | **llama-3.3-70b-versatile** | El más potente y equilibrado | 🟢 Media | 8K |
                    | **llama-3.1-70b-versatile** | Versión anterior, muy capaz | 🟢 Media | 8K |
                    | **llama-3.1-8b-instant** | Rápido y eficiente | 🟢🟢 Rápida | 8K |
                    | **mixtral-8x7b-32768** | Excelente para contextos largos | 🟢 Media | 32K |
                    | **gemma2-9b-it** | Modelo compacto de Google | 🟢🟢 Rápida | 8K |
                    """
                )
        
        
        with gr.Tab("ℹ️ Información", id=2):
            gr.Markdown(
                """
                ## 🚀 Acerca de este Chatbot
                
                Este chatbot utiliza la **API de Groq**, que ofrece:
                
                - ✅ **Modelos de última generación** (Llama 3.3, Mixtral, Gemma)
                - ✅ **Velocidad ultrarrápida** gracias a hardware especializado
                - ✅ **Completamente gratis** para uso personal
                - ✅ **Sin límites restrictivos** en el tier gratuito
                
                ### 📖 Cómo usar:
                
                1. **Ve a la pestaña Configuración** y personaliza tu agente
                2. **Haz clic en "Aplicar Configuración"**
                3. **Regresa a la pestaña Chat** y comienza a conversar
                4. **Usa el botón Limpiar** para reiniciar la conversación
                
                ### 🔐 Privacidad:
                
                - Tus conversaciones NO se almacenan en ningún servidor
                - Todo se procesa localmente en tu computadora
                - La API de Groq solo recibe los mensajes durante la sesión activa
                
                ### 🛠️ Tecnologías:
                
                - **Framework UI**: Gradio
                - **Proveedor de IA**: Groq
                - **Modelos**: LLaMA 3.3, Mixtral, Gemma2
                - **Lenguaje**: Python
                
                ---
                
                **Desarrollado por muted**
                """
            )
    
    def respond(message, chat_history):
        """Manejar respuesta del bot"""
        if not message.strip():
            return "", chat_history
        
        bot_message = chat_function(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    def clear_chat():
        """Limpiar el chat y reiniciar el agente"""
        if agent:
            agent.reset_conversation()
        return None
    
    def apply_config(model, temperature, system_prompt):
        """Aplicar configuración y reiniciar agente"""
        initialize_agent(model, temperature, system_prompt)
        return f"✅ Configuración aplicada correctamente!\n\n**Modelo**: {model}\n**Temperatura**: {temperature}"
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    send_btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(clear_chat, None, chatbot)
    apply_btn.click(
        apply_config,
        [model_dropdown, temperature_slider, system_prompt_textbox],
        config_status
    )
    
    demo.load(
        apply_config,
        [model_dropdown, temperature_slider, system_prompt_textbox],
        config_status
    )


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 INICIANDO CHATBOT CON GROQ API")
    print("="*70)
    print("\n✓ Interfaz: Gradio")
    print("✓ Proveedor: Groq")
    print("✓ Modelos disponibles: 5")
    print("\n👉 La interfaz se abrirá automáticamente en tu navegador")
    print("👉 URL local: http://127.0.0.1:7860")
    print("👉 Presiona Ctrl+C para detener\n")
    print("="*70 + "\n")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False, 
        show_error=True,
        quiet=False
    )