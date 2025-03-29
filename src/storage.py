import json

FILENAME = "data/datos.json"

def save_data(data):
    """ Guarda datos en un archivo JSON """
    try:
        with open(FILENAME, "r") as file:
            dataset = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        dataset = []

    dataset.append(data)  # Agregar nueva muestra

    with open(FILENAME, "w") as file:
        json.dump(dataset, file)

def load_data():
    """ Carga todos los datos almacenados en JSON """
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def clear_data():
    """ Borra el contenido del archivo JSON """
    with open(FILENAME, "w") as file:
        json.dump([], file)  # Reemplaza con una lista vacía
