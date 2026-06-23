import os
import pygame

# ==============================================================================
# CONFIGURACIÓN DE RUTAS Y RECURSOS DE AUDIO
# ==============================================================================

# Lista de directorios alternativos donde buscar los archivos de sonido.
# Esto asegura que el juego encuentre los assets sin importar desde dónde se ejecute.
RUTAS_SONIDO = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds"),
    os.path.join(os.path.dirname(__file__), "assets", "sounds"),
]

# Formatos de archivo soportados por prioridad para cada recurso de audio
NOMBRES_SOUNDTRACK = ("soundtrack_1.mp3", "soundtrack_1.ogg", "soundtrack_1.wav")
NOMBRES_COIN_COLLECT = ("coin_collect.wav", "coin_collect.mp3", "coin_collect.ogg")
NOMBRES_CRUNCH = ("crunch.wav", "crunch.mp3", "crunch.ogg")

# Diccionario para almacenar los efectos de sonido (SFX) ya cargados en memoria (Cache)
_cache_sfx = {}

# ==============================================================================
# FUNCIONES INTERNAS (SOPORTE Y LOGÍSTICA)
# ==============================================================================

def _asegurar_mixer():
    """Verifica si el módulo mixer de pygame está inicializado; si no, lo inicia."""
    if not pygame.mixer.get_init():
        pygame.mixer.init()

def _resolver_archivo(nombres):
    """
    Busca un archivo de audio en las rutas configuradas probando diferentes extensiones.
    
    :param nombres: Lista o tupla con los nombres de archivo posibles (ej. .mp3, .wav).
    :return: Ruta absoluta del primer archivo encontrado en el sistema.
    :raises FileNotFoundError: Si el archivo no existe en ninguna de las rutas.
    """
    for carpeta in RUTAS_SONIDO:
        for nombre in nombres:
            ruta = os.path.join(carpeta, nombre)
            if os.path.exists(ruta):
                return ruta
    raise FileNotFoundError(
        f"No se encontró el sonido ({', '.join(nombres)}) en: {', '.join(RUTAS_SONIDO)}"
    )

def _resolver_soundtrack():
    """Obtiene la ruta del archivo de música de fondo principal."""
    return _resolver_archivo(NOMBRES_SOUNDTRACK)

def _reproducir_sfx(clave, volumen=0.7):
    """
    Controlador interno para reproducir efectos de sonido usando memoria caché.
    Si el sonido no está cargado en '_cache_sfx', fuerza su precarga.
    
    :param clave: Identificador del sonido en el diccionario de caché.
    :param volumen: Nivel de volumen del sonido (0.0 a 1.0).
    """
    if clave not in _cache_sfx:
        precargar_sfx()
    sonido = _cache_sfx[clave]
    sonido.set_volume(volumen)
    sonido.play()

# ==============================================================================
# CONTROL DE MÚSICA DE FONDO (STREAMINGDESDE DISCO)
# ==============================================================================

def iniciar_musica_fondo(volumen=0.5):
    """
    Carga y reproduce el tema musical de fondo en un bucle infinito.
    Usa 'music' de pygame porque hace streaming del archivo sin saturar la RAM.
    """
    _asegurar_mixer()
    pygame.mixer.music.load(_resolver_soundtrack())
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1)

def detener_musica_fondo():
    """Detiene la música de fondo de manera segura si el mixer está activo."""
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()

# ==============================================================================
# GESTIÓN Y REPRODUCCIÓN DE EFECTOS DE SONIDO (SFX EN MEMORIA)
# ==============================================================================

def precargar_sfx():
    """
    Carga todos los efectos de sonido de corta duración en la memoria RAM.
    Se recomienda llamar a esta función durante la pantalla de carga para evitar tirones.
    """
    _asegurar_mixer()
    _cache_sfx["coin_collect"] = pygame.mixer.Sound(_resolver_archivo(NOMBRES_COIN_COLLECT))
    _cache_sfx["crunch"] = pygame.mixer.Sound(_resolver_archivo(NOMBRES_CRUNCH))

def reproducir_recolectar_moneda(volumen=0.7):
    """Reproduce el efecto de sonido cuando el jugador recolecta una moneda."""
    _reproducir_sfx("coin_collect", volumen)

def reproducir_crunch(volumen=0.7):
    """Reproduce el efecto de sonido cuando un brainrot consume una galleta."""
    _reproducir_sfx("crunch", volumen)
