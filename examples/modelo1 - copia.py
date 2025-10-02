"""
Paso 1: Agente Básico con Groq API (GRATIS)
Tu primer agente de IA usando Groq API
"""

import os
import sys
from groq import Groq
from dotenv import load_dotenv


env_path = r"C:\Users\Gustavo\Desktop\mi_chatbot\.env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")

print("DEBUG → KEY LENGTH:", len(api_key) if api_key else "No encontrada")
print("DEBUG → KEY START:", api_key[:6] if api_key else "No encontrada")

# Configurar Groq
if not api_key:
    print("⚠️ ERROR: No se encontró la GROQ_API_KEY en el .env")
    sys.exit(1)


class AgentConfig:
    """Configuración del agente"""
    def __init__(self, name, model, temperature, system_prompt):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt


class BaseAgent:
    """Agente básico usando Groq API"""

    def __init__(self, config: AgentConfig):
        self.config = config
        
        # Crear cliente de Groq
        self.client = Groq(api_key=api_key)
        
        # Historial de conversación
        self.conversation_history = [
            {"role": "system", "content": config.system_prompt}
        ]

    def chat(self, user_message: str) -> str:
        """Envía un mensaje y obtiene respuesta"""
        try:
            # Agregar mensaje del usuario
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Llamar a la API
            chat_completion = self.client.chat.completions.create(
                messages=self.conversation_history,
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=8192,
            )
            
            # Extraer respuesta
            assistant_message = chat_completion.choices[0].message.content
            
            # Agregar respuesta al historial
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Error al comunicarse con Groq: {str(e)}"

    def get_history(self):
        """Obtener historial de conversación"""
        return self.conversation_history


def main():
    """Ejemplo de un agente básico con Groq"""

    print("=== PASO 1: Agente Básico con Groq API (GRATIS) ===")
    print("Creando tu primer agente de IA...\n")

    config = AgentConfig(
        name="MiPrimerAgente",
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        system_prompt="Eres un asistente amigable que responde de manera concisa y útil."
    )

    agent = BaseAgent(config)

    print("¡Agente creado exitosamente!")
    print(f"Nombre: {config.name}")
    print(f"Modelo: {config.model}")
    print(f"Temperatura: {config.temperature}")
    print("\n" + "="*50 + "\n")

    print("Ahora puedes chatear con tu agente. Escribe 'salir' para terminar.\n")

    while True:
        try:
            user_input = input("Tú: ").strip()
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("¡Hasta luego!")
                break

            if not user_input:
                print("Por favor, escribe algo o 'salir' para terminar.")
                continue

            print("Agente: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Intenta de nuevo o escribe 'salir' para terminar.")


if __name__ == "__main__":
    main()