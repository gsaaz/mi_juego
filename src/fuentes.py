import os
import pygame

RUTA_FUENTE_MENU = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "fonts", "04B_30__.TTF",
)
RUTA_FUENTE_JUEGO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "fonts", "determination.ttf",
)

# Tamaños para el menú principal (04B_30__).
TAMANO_MENU_TITULO = 56
TAMANO_MENU_OPCION = 28
TAMANO_MENU_ALERTA = 22

# Tamaños para la partida (determination.ttf).
TAMANO_TITULO = 38
TAMANO_NORMAL = 17
TAMANO_PEQUENO = 14
TAMANO_MINIMO = 10

_cache_menu = {}
_cache_juego = {}

def obtener_fuente_menu(tamano):
    # Fuente pixel del menú de inicio.
    if tamano not in _cache_menu:
        _cache_menu[tamano] = pygame.font.Font(RUTA_FUENTE_MENU, tamano)
    return _cache_menu[tamano]

def obtener_fuente_juego(tamano):
    # Fuente principal durante el juego.
    if tamano not in _cache_juego:
        _cache_juego[tamano] = pygame.font.Font(RUTA_FUENTE_JUEGO, tamano)
    return _cache_juego[tamano]

def obtener_fuente(tamano):
    # Alias de compatibilidad: la partida usa determination.
    return obtener_fuente_juego(tamano)

def obtener_fuente_para_rect(texto, ancho_max, alto_max, tamano_inicial=20, tamano_minimo=TAMANO_MINIMO):
    # Busca el mayor tamaño de fuente en el que el texto cabe dentro del rectángulo.
    for tamano in range(tamano_inicial, tamano_minimo - 1, -1):
        fuente = obtener_fuente_juego(tamano)
        imagen = fuente.render(texto, True, (0, 0, 0))
        if imagen.get_width() <= ancho_max and imagen.get_height() <= alto_max:
            return fuente
    return obtener_fuente_juego(tamano_minimo)
