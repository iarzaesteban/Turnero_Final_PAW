import base64

# Función para convertir una imagen a cadena de bytes
def image_to_bytes(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

# Datos del archivo CSV
data = [
    {"short_description": "contacto", "title": "Contacto", "description": "¿Necesitas ayuda? ¡No dudes en contactarnos! Estamos aquí para responder a tus preguntas y brindarte el mejor servicio posible.", "icon_path": "init-scripts/icons/contacto.png"},
    {"short_description": "quienes_somos", "title": "¿Quiénes Somos?", "description": "Sistema de turnos de la Autoridad de Registro de la Universidad Nacional de Luján. Brindamos servicios de enrolamiento y gestión de turnos para la comunidad universitaria.", "icon_path": "init-scripts/icons/acerca_de.png"},
    {"short_description": "ubicacion", "title": "Ubicación", "description": "Encuéntranos en el campus universitario. Nuestra oficina de enrolamiento está ubicada en [Ubicación específica]. Visítanos para obtener asistencia personalizada.", "icon_path": "init-scripts/icons/ubicacion.png"}
]

# Procesar los datos y guardar en el archivo CSV
with open("init-scripts/csv/aditional_information.csv", "w") as csv_file:
    csv_file.write("short_description,title,description,icon\n")
    for row in data:
        icon_bytes = image_to_bytes(row["icon_path"])
        csv_file.write(f"{row['short_description']},{row['title']},{row['description']},{icon_bytes}\n")

print("Archivo CSV generado exitosamente.")
