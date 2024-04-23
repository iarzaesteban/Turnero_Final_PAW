import os
import io
import base64
import json
from PIL import Image

# Función para convertir una imagen a cadena base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        img = Image.open(image_file)
        img = img.resize((50, 50))
        
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        encoded_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return encoded_string

script_dir = os.path.dirname(os.path.realpath(__file__))

# Datos del archivo JSON
data = [
    {"model": "aditional_information.AditionalInformation", "pk": 1, "fields": {"short_description": "contacto", "title": "Contacto", "description": "¿Necesitas ayuda? ¡No dudes en contactarnos! Estamos aquí para responder a tus preguntas y brindarte el mejor servicio posible.", "icon": "phone", "link": "tel:+123456789"}},
    {"model": "aditional_information.AditionalInformation", "pk": 2, "fields": {"short_description": "quienes_somos", "title": "¿Quiénes Somos?", "description": "Sistema de turnos de la Autoridad de Registro de la Universidad Nacional de Luján. Brindamos servicios de enrolamiento y gestión de turnos para la comunidad universitaria.", "icon": "acerca_de"}},
    {"model": "aditional_information.AditionalInformation", "pk": 3, "fields": {"short_description": "ubicacion", "title": "Ubicación", "description": "Encuéntranos en el campus universitario. Nuestra oficina de enrolamiento está ubicada en [Ubicación específica]. Visítanos para obtener asistencia personalizada.", "icon": "gps", "link": "https://www.example.com"}}
]

# Procesar los datos y guardar en el archivo JSON
for row in data:
    icon_base64 = image_to_base64(os.path.join(script_dir, f"icons/{row['fields']['icon']}.png"))
    row['fields']['icon'] = f"data:image/png;base64,{icon_base64}"

with open("/opt/turnero_paw_2024/applications/aditional_information/fixtures/aditional_information.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Archivo JSON generado exitosamente.")
