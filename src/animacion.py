"""
src/animacion.py  -  Carga de sprites y animacion de los brainrots.

Este modulo es NUEVO. Centraliza todo lo visual de los personajes para no
ensuciar la logica de brainrot.py:

  - cargar_sprite(nombre, mirando): devuelve el Surface escalado (y volteado
    segun la direccion en la que mira el brainrot). Carga perezosa y cacheada.
  - blit_rotado(...): dibuja una imagen rotada fijando un pivote (los pies o el
    centro), que es lo que produce el bamboleo al caminar y el cabeceo al flotar.
  - dibujar_sombra(...): sombra tenue en el piso para los que flotan.

DONDE VAN LOS PNG:
  Coloca brainrot_a.png, brainrot_b.png y brainrot_c.png en  assets/sprites/
  (la misma carpeta donde ya tienes el spritesheet de monedas) o en src/assets/.
  Este modulo los busca en ambas rutas, igual que fondo.py y moneda.py.
"""
import os
import pygame

# --- Tamano en pantalla de los brainrots ---
# OJO: la hitbox del juego sigue siendo 50x50 (no se toca); esto es solo lo visual.
ALTO_SPRITE = 72      # alto del personaje en px
ANCHO_MAX = 110       # tope de ancho (para que el dirigible no quede gigante)

# --- Parametros del bamboleo (caminar) ---
TILT = 8.0            # grados de ladeo de lado a lado
HOP = 7.0             # rebote vertical (px)
VEL_PASO = 0.30       # cuanto avanza la fase por frame al caminar

# --- Parametros de flotar (dirigible / cocodrilo) ---
PITCH = 6.0           # grados de cabeceo (asiente)
BOB = 6.0             # subir / bajar (px)
HOVER = 12.0          # cuanto se eleva sobre su base
VEL_FLOT = 0.06       # cuanto avanza la fase por frame flotando

# --- Salto al comer (para los tres) ---
SALTO_ALTURA = 22.0   # alto del salto (px)
SALTO_FRAMES = 22     # duracion del salto (frames; a 60 FPS ~0.37 s)

# Mismas rutas que usan fondo.py / moneda.py
_RUTAS = [
    os.path.join(os.path.dirname(__file__), "assets"),                              # src/assets
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites"),  # raiz/assets/sprites
]

_cache = {}


def _resolver_ruta(nombre):
    for carpeta in _RUTAS:
        ruta = os.path.join(carpeta, nombre)
        if os.path.exists(ruta):
            return ruta
    raise FileNotFoundError(
        f"No se encontro el sprite '{nombre}' en: {', '.join(_RUTAS)}"
    )


def cargar_sprite(nombre, mirando=1):
    """Carga, escala y cachea el sprite (y su version volteada).
    Carga perezosa: ocurre la 1a vez que se dibuja, con la ventana ya creada,
    por lo que convert_alpha() funciona sin problemas."""
    if nombre not in _cache:
        imagen = pygame.image.load(_resolver_ruta(nombre)).convert_alpha()
        w0, h0 = imagen.get_size()
        escala = ALTO_SPRITE / h0
        nw, nh = round(w0 * escala), ALTO_SPRITE
        if nw > ANCHO_MAX:                       # limitar ancho (caso dirigible)
            escala = ANCHO_MAX / w0
            nw, nh = ANCHO_MAX, round(h0 * escala)
        imagen = pygame.transform.smoothscale(imagen, (nw, nh))
        _cache[nombre] = {1: imagen, -1: pygame.transform.flip(imagen, True, False)}
    return _cache[nombre][1 if mirando >= 0 else -1]


def blit_rotado(superficie, imagen, ancla, angulo, pivote="pies"):
    """Dibuja 'imagen' rotada 'angulo' grados fijando un pivote en 'ancla'.
       pivote="pies"   -> centro-inferior: el personaje se mece sobre el piso.
       pivote="centro" -> centro:           el personaje cabecea en el aire.
    Asi la rotacion no 'flota' descontrolada: el punto de apoyo queda fijo."""
    w, h = imagen.get_size()
    piv = pygame.math.Vector2(w / 2, h) if pivote == "pies" else pygame.math.Vector2(w / 2, h / 2)
    centro = pygame.math.Vector2(w / 2, h / 2)
    off = piv - centro
    rot = pygame.transform.rotate(imagen, angulo)
    rot_off = off.rotate(-angulo)
    centro_rot = pygame.math.Vector2(ancla) - rot_off
    rect = rot.get_rect(center=(round(centro_rot.x), round(centro_rot.y)))
    superficie.blit(rot, rect.topleft)


def dibujar_sombra(superficie, cx, base_y, ancho):
    """Sombra ovalada tenue en el piso (da sensacion de altura al que flota)."""
    sombra = pygame.Surface((ancho, max(6, ancho // 4)), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 70), sombra.get_rect())
    superficie.blit(sombra, (cx - ancho // 2, base_y - sombra.get_height() // 2))
