import os
import random
import pygame
from src.constantes import ANCHO, ALTO, LINEA_HORIZONTE

# ─── CIELO ────────────────────────────────────────────────────────────────────

RUTAS_CIELO = [
    os.path.join(os.path.dirname(__file__), "assets"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites"),
]

_fondo_cielo = None
_fondo_cielo_pantalla = None

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

def _escalar_cielo_cover(ancho_destino, alto_destino):
    # Escala sky1 en modo "cover" para cubrir un rectángulo sin deformar la imagen.
    imagen = pygame.image.load(_resolver_ruta_cielo()).convert()
    ancho_origen, alto_origen = imagen.get_size()
    escala = max(ancho_destino / ancho_origen, alto_destino / alto_origen)
    ancho_escalado = int(ancho_origen * escala)
    alto_escalado = int(alto_origen * escala)
    imagen_escalada = pygame.transform.scale(imagen, (ancho_escalado, alto_escalado))
    recorte_x = (ancho_escalado - ancho_destino) // 2
    recorte_y = (alto_escalado - alto_destino) // 2
    return imagen_escalada.subsurface(
        (recorte_x, recorte_y, ancho_destino, alto_destino)
    ).copy()

def precargar_fondo_pantalla_completa():
    # Escala sky1 para cubrir toda la ventana (800×600), usado en el menú de inicio.
    global _fondo_cielo_pantalla
    if _fondo_cielo_pantalla is not None:
        return _fondo_cielo_pantalla

    _fondo_cielo_pantalla = _escalar_cielo_cover(ANCHO, ALTO)
    return _fondo_cielo_pantalla

def dibujar_fondo_cielo_completo(superficie):
    # Pinta el cielo escalado a pantalla completa.
    superficie.blit(precargar_fondo_pantalla_completa(), (0, 0))

# ─── PRADO Y VALLA ────────────────────────────────────────────────────────────

TAMANO_BLOQUE = 32
ANCHO_VALLA   = 64
ALTO_VALLA    = 48
OFFSET_VALLA_Y = 16  # La base de la valla se hunde en el pasto (LINEA_HORIZONTE - OFFSET)

RUTAS_ASSETS = [
    os.path.join(os.path.dirname(__file__), "assets"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites"),
]
NOMBRES_VALLA = ("valla.png", "valla.jpg", "fence.png", "fence.jpg")

def _resolver_ruta_valla():
    # Busca el sprite de la valla en src/assets o assets/sprites.
    for carpeta in RUTAS_ASSETS:
        for nombre in NOMBRES_VALLA:
            ruta = os.path.join(carpeta, nombre)
            if os.path.exists(ruta):
                return ruta
    raise FileNotFoundError(
        f"No se encontró la valla (valla.png / fence.jpg) en: {', '.join(RUTAS_ASSETS)}"
    )

def _cargar_valla():
    # Carga y escala el segmento de valla para repetirlo a lo largo del horizonte.
    imagen = pygame.image.load(_resolver_ruta_valla()).convert_alpha()
    return pygame.transform.scale(imagen, (ANCHO_VALLA, ALTO_VALLA))

def _construir_segmentos_valla(sprite_valla):
    # Precalcula los segmentos de valla para cubrir todo el ancho sin huecos.
    segmentos = []
    x = 0
    while x < ANCHO:
        ancho_restante = ANCHO - x
        if ancho_restante >= ANCHO_VALLA:
            segmentos.append((x, sprite_valla))
        else:
            segmentos.append((
                x,
                sprite_valla.subsurface((0, 0, ancho_restante, ALTO_VALLA)).copy(),
            ))
        x += ANCHO_VALLA
    return segmentos

def _dibujar_valla(superficie, segmentos_valla):
    # Pinta la cerca sobre el horizonte, tapando la unión entre cielo y pasto.
    pos_y = LINEA_HORIZONTE - OFFSET_VALLA_Y
    for x, imagen in segmentos_valla:
        superficie.blit(imagen, (x, pos_y))

def _resolver_ruta_textura(nombre_base):
    # Busca la textura en src/assets o assets/sprites (.jpg o .png).
    for carpeta in RUTAS_ASSETS:
        for extension in (".jpg", ".jpeg", ".png"):
            ruta = os.path.join(carpeta, f"{nombre_base}{extension}")
            if os.path.exists(ruta):
                return ruta
    raise FileNotFoundError(
        f"No se encontró la textura '{nombre_base}' en: {', '.join(RUTAS_ASSETS)}"
    )

def _cargar_textura_pasto(nombre_base):
    # Carga una textura del prado y la escala a un bloque de 32×32 píxeles.
    imagen = pygame.image.load(_resolver_ruta_textura(nombre_base)).convert()
    return pygame.transform.scale(imagen, (TAMANO_BLOQUE, TAMANO_BLOQUE))

def _celda_textura(textura, ancho, alto):
    # Ajusta el bloque al borde del prado (solo al generar el mapa, no en el bucle de dibujo).
    if ancho == TAMANO_BLOQUE and alto == TAMANO_BLOQUE:
        return textura
    return textura.subsurface((0, 0, ancho, alto)).copy()

def _generar_mapa_prado(tile_pasto_base, tile_pasto_flores, tile_pasto_alto):
    # Construye una sola vez la matriz estática del prado (85% base, 10% flores, 5% alto).
    mapa_prado = []
    for y in range(LINEA_HORIZONTE, ALTO, TAMANO_BLOQUE):
        for x in range(0, ANCHO, TAMANO_BLOQUE):
            ancho = min(TAMANO_BLOQUE, ANCHO - x)
            alto  = min(TAMANO_BLOQUE, ALTO - y)
            probabilidad = random.random()

            if probabilidad < 0.85:
                textura = tile_pasto_base
            elif probabilidad < 0.95:
                textura = tile_pasto_flores
            else:
                textura = tile_pasto_alto

            mapa_prado.append((x, y, _celda_textura(textura, ancho, alto)))
    return mapa_prado

# ─── API PÚBLICA DEL ESCENARIO ────────────────────────────────────────────────

def preparar_valla():
    # Carga la valla y calcula los segmentos una sola vez antes del bucle principal.
    sprite_valla = _cargar_valla()
    return _construir_segmentos_valla(sprite_valla)

def preparar_prado():
    # Carga los tiles y genera el mapa estático del prado una sola vez antes del bucle.
    tile_base   = _cargar_textura_pasto("grass_1")
    tile_flores = _cargar_textura_pasto("grass_2")
    tile_alto   = _cargar_textura_pasto("grass_3")
    return _generar_mapa_prado(tile_base, tile_flores, tile_alto)

def dibujar_escenario(superficie, mapa_prado, segmentos_valla):
    # Dibuja en orden: cielo → prado → valla sobre el horizonte.
    dibujar_fondo_cielo(superficie)
    for x, y, imagen_pasto in mapa_prado:
        superficie.blit(imagen_pasto, (x, y))
    _dibujar_valla(superficie, segmentos_valla)
