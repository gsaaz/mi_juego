import json
import os
from src.brainrot import BrainrotA, BrainrotB, BrainrotC

# Ruta del archivo de guardado dentro de la carpeta 'datos/'.
RUTA_PARTIDA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos", "partida.json")

# Diccionario para mapear los tipos de texto guardados con sus clases respectivas.
CLASES_BRAINROT = {
    "A": BrainrotA,
    "B": BrainrotB,
    "C": BrainrotC,
}

def _tipo_de_brainrot(brainrot):
    """
    Obtiene el identificador de tipo (dieta) de un brainrot.
    
    :param brainrot: Instancia de Brainrot.
    :return: String con el tipo ("A", "B" o "C").
    """
    return brainrot.tipo_dieta

def _crear_brainrot(datos):
    """
    Instancia y restaura una criatura utilizando los datos guardados.
    
    :param datos: Diccionario con los atributos de la criatura.
    :return: Instancia de la clase correspondiente o None si hay error.
    """
    clase = CLASES_BRAINROT.get(datos["tipo"])
    if clase is None:
        return None

    brainrot = clase(datos["x"], datos["y"])
    brainrot.hambre = datos["hambre"]
    brainrot.salud = datos["salud"]
    return brainrot

def guardar_partida(dinero, tienda, lista_brainrots):
    """
    Empaqueta el estado actual del juego y lo escribe en el archivo JSON.
    
    :param dinero: Dinero actual del jugador.
    :param tienda: Instancia de la tienda (para guardar stock de comida).
    :param lista_brainrots: Lista de instancias de criaturas activas.
    """
    brainrots_guardados = []
    for brainrot in lista_brainrots:
        if not brainrot.vivo:
            continue
        brainrots_guardados.append({
            "tipo": _tipo_de_brainrot(brainrot),
            "x": brainrot.x,
            "y": brainrot.y,
            "hambre": brainrot.hambre,
            "salud": brainrot.salud,
        })

    partida = {
        "dinero": dinero,
        "cant_A": tienda.cant_A,
        "cant_B": tienda.cant_B,
        "cant_C": tienda.cant_C,
        "brainrots": brainrots_guardados,
    }

    with open(RUTA_PARTIDA, "w", encoding="utf-8") as archivo:
        json.dump(partida, archivo, indent=2)

def cargar_partida():
    """
    Lee el archivo 'partida.json' si existe.
    
    :return: Un diccionario con el estado de la partida, o None si no hay archivo.
    """
    if not os.path.exists(RUTA_PARTIDA):
        return None

    with open(RUTA_PARTIDA, "r", encoding="utf-8") as archivo:
        partida = json.load(archivo)

    lista_brainrots = []
    for datos in partida.get("brainrots", []):
        brainrot = _crear_brainrot(datos)
        if brainrot is not None:
            lista_brainrots.append(brainrot)

    return {
        "dinero": partida["dinero"],
        "cant_A": partida["cant_A"],
        "cant_B": partida["cant_B"],
        "cant_C": partida["cant_C"],
        "lista_brainrots": lista_brainrots,
    }
