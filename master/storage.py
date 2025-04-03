import json
import time
import os

DIRECTORY = "/sd"  # Directorio en la SD donde se guardarán los archivos

def save_data(data):
    """ Guarda datos en un nuevo archivo JSON sin sobrescribir los existentes. """
    timestamp = int(time.time())  # Marca de tiempo única
    filename = f"{DIRECTORY}/datos_{timestamp}.json"

    try:
        with open(filename, "w") as file:
            json.dump(data, file)
        print(f"Datos guardados en {filename}")
    except Exception as e:
        print(f"Error guardando datos en JSON: {e}")

def get_latest_file():
    """ Obtiene el archivo más reciente de datos en la SD. """
    try:
        files = [f for f in os.listdir(DIRECTORY) if f.startswith("datos_") and f.endswith(".json")]
        if not files:
            return None
        latest_file = max(files, key=lambda f: int(f.split("_")[1].split(".")[0]))
        return f"{DIRECTORY}/{latest_file}"
    except Exception as e:
        print(f"Error obteniendo el archivo más reciente: {e}")
        return None

def load_data():
    """ Carga los datos del archivo más reciente almacenado en la SD. """
    latest_file = get_latest_file()
    if not latest_file:
        return []
    
    try:
        with open(latest_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error cargando datos desde {latest_file}: {e}")
        return []


