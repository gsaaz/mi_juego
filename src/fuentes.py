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

# Tamaños estándar para el menú principal (04B_30__).
TAMANO_MENU_TITULO = 56
TAMANO_MENU_OPCION = 28
TAMANO_MENU_ALERTA = 22

# Tamaños estándar para la partida (determination.ttf).
TAMANO_TITULO = 38
TAMANO_NORMAL = 17
TAMANO_PEQUENO = 14
TAMANO_MINIMO = 10

# Diccionarios de caché para no cargar la misma fuente de disco múltiples veces.
_cache_menu = {}
_cache_juego = {}

def obtener_fuente_menu(tamano):
    """
    Obtiene la fuente pixelada utilizada en el menú de inicio.
    
    :param tamano: Tamaño de la fuente en puntos.
    :return: Objeto pygame.font.Font.
    """
    if tamano not in _cache_menu:
        _cache_menu[tamano] = pygame.font.Font(RUTA_FUENTE_MENU, tamano)
    return _cache_menu[tamano]

def obtener_fuente_juego(tamano):
    """
    Obtiene la fuente principal utilizada durante la partida (determination).
    
    :param tamano: Tamaño de la fuente en puntos.
    :return: Objeto pygame.font.Font.
    """
    if tamano not in _cache_juego:
        _cache_juego[tamano] = pygame.font.Font(RUTA_FUENTE_JUEGO, tamano)
    return _cache_juego[tamano]

def obtener_fuente(tamano):
    """Alias de compatibilidad que retorna la fuente principal del juego."""
    return obtener_fuente_juego(tamano)

def obtener_fuente_para_rect(texto, ancho_max, alto_max, tamano_inicial=20, tamano_minimo=TAMANO_MINIMO):
    """
    Busca de manera dinámica el mayor tamaño de fuente posible para que
    el texto encaje dentro de unas dimensiones máximas (rectángulo).
    
    :param texto: El texto que se desea renderizar.
    :param ancho_max: Anchura máxima permitida.
    :param alto_max: Altura máxima permitida.
    :param tamano_inicial: Tamaño desde donde empezar a reducir.
    :param tamano_minimo: Tamaño mínimo garantizado.
    :return: Objeto pygame.font.Font ajustado.
    """
    for tamano in range(tamano_inicial, tamano_minimo - 1, -1):
        fuente = obtener_fuente_juego(tamano)
        imagen = fuente.render(texto, True, (0, 0, 0))
        if imagen.get_width() <= ancho_max and imagen.get_height() <= alto_max:
            return fuente
    return obtener_fuente_juego(tamano_minimo)
