import os
import pygame
from src.constantes import ANCHO, LINEA_HORIZONTE

RUTAS_CIELO = [
    os.path.join(os.path.dirname(__file__), "assets"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites"),
]

_fondo_cielo = None

def _resolver_ruta_cielo():
    # Busca sky1 en src/assets o assets/sprites (.png o .jpg).
    for carpeta in RUTAS_CIELO:
        for extension in (".png", ".jpg", ".jpeg"):
            ruta = os.path.join(carpeta, f"sky1{extension}")
            if os.path.exists(ruta):
                return ruta
    raise FileNotFoundError(
        f"No se encontró sky1 en: {', '.join(RUTAS_CIELO)}"
    )

def precargar_fondo():
    # Escala sky1 para cubrir la franja del cielo (800×250) sin deformar la imagen.
    global _fondo_cielo
    if _fondo_cielo is not None:
        return _fondo_cielo

    imagen = pygame.image.load(_resolver_ruta_cielo()).convert()
    ancho_destino = ANCHO
    alto_destino = LINEA_HORIZONTE
    ancho_origen, alto_origen = imagen.get_size()

    # Escala tipo "cover": llena todo el cielo manteniendo proporción.
    escala = max(ancho_destino / ancho_origen, alto_destino / alto_origen)
    ancho_escalado = int(ancho_origen * escala)
    alto_escalado = int(alto_origen * escala)
    imagen_escalada = pygame.transform.scale(imagen, (ancho_escalado, alto_escalado))

    # Centrado horizontal; alineado abajo para que el cielo se una al horizonte.
    recorte_x = (ancho_escalado - ancho_destino) // 2
    recorte_y = alto_escalado - alto_destino
    _fondo_cielo = imagen_escalada.subsurface(
        (recorte_x, recorte_y, ancho_destino, alto_destino)
    ).copy()
    return _fondo_cielo

def dibujar_fondo_cielo(superficie):
    # Pinta la textura del cielo en la zona superior de la pantalla.
    superficie.blit(precargar_fondo(), (0, 0))
