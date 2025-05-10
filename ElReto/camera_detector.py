import os
import cv2
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import time

# Cargar variables de entorno (para la clave API)
load_dotenv()
print("API KEY:", repr(os.getenv("GEMINI_API_KEY")))
def capture_image():
    """
    Captura una imagen desde la cámara web
    """
    print("Inicializando cámara web...")
    # Inicializa la cámara (0 es generalmente la cámara web integrada)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara web.")
        return None
    
    # Dar tiempo a la cámara para que se ajuste a la luz
    time.sleep(1)
    
    print("Tomando foto en 3 segundos...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Captura un frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: No se pudo capturar la imagen.")
        cap.release()
        return None
    
    # Guardar la imagen temporalmente
    filename = "captura.jpg"
    cv2.imwrite(filename, frame)
    
    # Mostrar la imagen capturada
    cv2.imshow("Imagen Capturada", frame)
    print("Presiona cualquier tecla para continuar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Liberar la cámara
    cap.release()
    
    print(f"Imagen guardada como {filename}")
    return filename

def configure_gemini():
    """
    Configura la API de Google Gemini
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: No se encontró la clave API de Gemini.")
        print("Por favor, crea un archivo .env con GEMINI_API_KEY=tu_clave_aqui")
        return None
    
    # Configurar la API de Gemini
    genai.configure(api_key=api_key)
    return True

def analyze_image(image_path):
    """
    Analiza la imagen usando Google Gemini
    """
    try:
        # Cambia aquí el modelo a gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Abrir la imagen
        image = Image.open(image_path)
        
        # Crear el prompt para la detección de personas y descripción de objetos
        prompt = """
        Analiza esta imagen y responde a las siguientes preguntas:
        1. ¿Hay alguna persona en la imagen? Responde con "Sí" o "No".
        2. Si hay personas, describe cuántas hay y qué están haciendo.
        3. Describe otros objetos importantes que se ven en la imagen.
        """
        
        # Enviar la solicitud a la API
        response = model.generate_content([prompt, image])
        
        return response.text
    except Exception as e:
        print(f"Error al analizar la imagen: {e}")
        return None

def main():
    print("=== Detector de Personas con Cámara Web y Google Gemini ===\n")
    
    # Paso 1: Capturar imagen
    image_path = capture_image()
    if not image_path:
        return
    
    # Paso 2: Configurar API de Gemini
    print("\nConfigurando API de Google Gemini...")
    if not configure_gemini():
        return
    
    # Paso 3: Analizar la imagen
    print("\nAnalizando imagen con IA...")
    result = analyze_image(image_path)
    
    # Paso 4: Mostrar resultados
    if result:
        print("\n=== Resultados del Análisis ===")
        print(result)
    else:
        print("\nNo se pudo completar el análisis de la imagen.")

if __name__ == "__main__":
    main()