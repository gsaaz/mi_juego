import os
import pygame

RUTAS_SONIDO = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds"),
    os.path.join(os.path.dirname(__file__), "assets", "sounds"),
]

NOMBRES_SOUNDTRACK = ("soundtrack_1.mp3", "soundtrack_1.ogg", "soundtrack_1.wav")
NOMBRES_COIN_COLLECT = ("coin_collect.wav", "coin_collect.mp3", "coin_collect.ogg")
NOMBRES_CRUNCH = ("crunch.wav", "crunch.mp3", "crunch.ogg")

_cache_sfx = {}

def _asegurar_mixer():
    if not pygame.mixer.get_init():
        pygame.mixer.init()

def _resolver_archivo(nombres):
    for carpeta in RUTAS_SONIDO:
        for nombre in nombres:
            ruta = os.path.join(carpeta, nombre)
            if os.path.exists(ruta):
                return ruta
    raise FileNotFoundError(
        f"No se encontró el sonido ({', '.join(nombres)}) en: {', '.join(RUTAS_SONIDO)}"
    )

def _resolver_soundtrack():
    return _resolver_archivo(NOMBRES_SOUNDTRACK)

def iniciar_musica_fondo(volumen=0.5):
    # Reproduce el tema de fondo en bucle continuo.
    _asegurar_mixer()
    pygame.mixer.music.load(_resolver_soundtrack())
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1)

def detener_musica_fondo():
    # Detiene el tema de fondo.
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()

def precargar_sfx():
    # Carga los efectos de sonido en memoria.
    _asegurar_mixer()
    _cache_sfx["coin_collect"] = pygame.mixer.Sound(_resolver_archivo(NOMBRES_COIN_COLLECT))
    _cache_sfx["crunch"] = pygame.mixer.Sound(_resolver_archivo(NOMBRES_CRUNCH))

def _reproducir_sfx(clave, volumen=0.7):
    if clave not in _cache_sfx:
        precargar_sfx()
    sonido = _cache_sfx[clave]
    sonido.set_volume(volumen)
    sonido.play()

def reproducir_recolectar_moneda(volumen=0.7):
    # SFX al recoger una moneda del suelo.
    _reproducir_sfx("coin_collect", volumen)

def reproducir_crunch(volumen=0.7):
    # SFX cuando un brainrot come una galleta.
    _reproducir_sfx("crunch", volumen)
