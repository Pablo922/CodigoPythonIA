import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AgenteProductividad:
    def __init__(self):
        # 1. Seguridad
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Error: No se encontró la GEMINI_API_KEY en el archivo .env")
            
        genai.configure(api_key=api_key)
        
        # 2. CAMBIO AQUÍ: Usamos 'gemini-2.0-flash-lite' que es la versión más compatible
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite-001')
        
        # 3. Instrucciones
        self.instrucciones_sistema = """
        Eres un Asistente Inteligente de Productividad Personal.
        Tu objetivo es ayudar al usuario a organizar su tiempo y tareas de forma eficiente.

        REGLAS DE RESPUESTA:
        1. LISTAS DE TAREAS: Priorízalas usando la Matriz de Eisenhower (Urgente/Importante).
        2. METAS VAGAS: Crea un plan de acción con bloques de tiempo (Técnica Pomodoro).
        3. TEXTOS LARGOS: Resume el contenido y extrae los "Action Items".
        4. FORMATO: Usa Markdown (negritas, listas) para que la respuesta sea clara.
        """

    def consultar(self, entrada_usuario):
        try:
            # En Gemini Pro, a veces es mejor pasar el prompt directo sin roles complejos
            prompt_completo = f"{self.instrucciones_sistema}\n\nSITUACIÓN DEL USUARIO:\n{entrada_usuario}"
            
            response = self.model.generate_content(prompt_completo)
            return response.text
            
        except Exception as e:
            return f"Ocurrió un error al conectar con Gemini: {str(e)}"