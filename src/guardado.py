import json
import os
from src.brainrot import BrainrotA, BrainrotB, BrainrotC

# Ruta del archivo de guardado dentro de la carpeta datos/.
RUTA_PARTIDA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos", "partida.json")

CLASES_BRAINROT = {
    "A": BrainrotA,
    "B": BrainrotB,
    "C": BrainrotC,
}

def _tipo_de_brainrot(brainrot):
    # Devuelve el identificador de tipo según la clase hija de la criatura.
    return brainrot.tipo_dieta

def _crear_brainrot(datos):
    # Instancia una criatura según el tipo guardado y restaura sus atributos.
    clase = CLASES_BRAINROT.get(datos["tipo"])
    if clase is None:
        return None

    brainrot = clase(datos["x"], datos["y"])
    brainrot.hambre = datos["hambre"]
    brainrot.salud = datos["salud"]
    return brainrot

def guardar_partida(dinero, tienda, lista_brainrots):
    # Empaqueta el estado actual y lo escribe en partida.json.
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
    # Lee partida.json si existe; de lo contrario, indica partida nueva con None.
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
