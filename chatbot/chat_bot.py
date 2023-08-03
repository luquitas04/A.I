import nltk
from nltk.chat.util import Chat, reflections
from transformers import pipeline 

# Entrenamiento de pares de patrones y respuestas
pares = [
    ["Mi nombre es (.*)", ["Hola %, ¿cómo puedo ayudarte?"] ],
    ["¿cuál es tu nombre?", ["Mi nombre es Wizi, un ChatBot basico"] ],
    ["¿comó estas?", ["Estoy bien, gracias. ¿Y tú?"] ],
    ["(.*) edad?", ["No tengo edad ya que soy un programa de computadora"] ],
    ["(.*) color favorito?", ["Mi color favorito es el azul"] ],
    ["(.*) clima en (.*)", ["El clima en %2 es genial"] ],
    ["(.*) pelicula favorita?", ["Mi pelicula favorita es Blade Runner."] ],
    ["adios", ["Hasta luego"] ],
    ["(.*)", ["Lo siento, no entiendo esa pregunta. ¿Podrias intentar reformularla?"] ],
]

# Inicializamos el modelo GPT-Neo
chatbotm_model = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

# Funcion que ejecuta el programa
def chat():
    print("Hola, soy Wizi. ¿En qué puedo ayudarte?")
    # chatbot = Chat(pares, reflections)
    while True:
        entrada = input("Tú: ")
        if entrada.lower() == 'salir':
            break
        # respuesta = chatbot.respond(entrada)
        respuesta = chatbotm_model(entrada, max_length = 100, do_sample = True) [0] ["generated_text"]
        print("Wizi: " + respuesta)

if __name__ == "__main__":
    nltk.download('punkt')
    chat()