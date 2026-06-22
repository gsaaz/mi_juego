import pygame
import os

RUTA_SPRITES = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "sprites", "coins-chests-etc-2-0-noborders.png",
)

# Configuración de cada tipo: valor económico y fila Y en el spritesheet
_CONFIGS = {
    "oro":    {"valor": 50, "fila_y": 16},
    "plata":  {"valor": 25, "fila_y": 32},
    "bronce": {"valor": 10, "fila_y": 48},
}

_FRAME_X_INICIO  = 16   # El spritesheet tiene 16px de margen vacío a la izquierda
_FRAME_W         = 16   # Ancho de cada frame en el spritesheet
_FRAME_H         = 16   # Alto de cada frame en el spritesheet
_NUM_FRAMES      = 9    # Frames de rotación completa por moneda
_ESCALA          = 3    # Factor de escala: 16×16 → 48×48 píxeles en pantalla
_TICKS_POR_FRAME = 6    # Cada cuántos ticks del juego se avanza un frame

ANCHO_MONEDA = _FRAME_W * _ESCALA   # 48 px
ALTO_MONEDA  = _FRAME_H * _ESCALA   # 48 px


class Moneda:
    # Spritesheet y frames pre-escalados compartidos entre todas las instancias
    _spritesheet   = None
    _cache_frames  = {}

    def __init__(self, x, y, tipo="bronce"):
        self.x    = float(x)
        self.y    = float(y)
        self.tipo = tipo

        config     = _CONFIGS.get(tipo, _CONFIGS["bronce"])
        self.valor = config["valor"]
        self._fila_y = config["fila_y"]

        # Dimensiones expuestas para el cálculo de hitbox en juego.py
        self.ancho = ANCHO_MONEDA
        self.largo = ALTO_MONEDA

        self._frame_actual    = 0
        self._reloj_animacion = 0

        self._frames = self._obtener_frames(tipo, self._fila_y)

    @classmethod
    def precargar(cls):
        # Carga el spritesheet y todos los frames tras inicializar la ventana.
        for tipo, config in _CONFIGS.items():
            cls._obtener_frames(tipo, config["fila_y"])

    @classmethod
    def _cargar_spritesheet(cls):
        # Carga la imagen una sola vez para toda la sesión
        if cls._spritesheet is None:
            if not os.path.exists(RUTA_SPRITES):
                raise FileNotFoundError(f"No se encontró el spritesheet: {RUTA_SPRITES}")
            cls._spritesheet = pygame.image.load(RUTA_SPRITES).convert_alpha()
        return cls._spritesheet

    @classmethod
    def _obtener_frames(cls, tipo, fila_y):
        # Devuelve la lista de frames desde la caché; los genera si no existen
        if tipo not in cls._cache_frames:
            sheet  = cls._cargar_spritesheet()
            frames = []
            for i in range(_NUM_FRAMES):
                rect = pygame.Rect(
                    _FRAME_X_INICIO + i * _FRAME_W,
                    fila_y,
                    _FRAME_W,
                    _FRAME_H,
                )
                surf = sheet.subsurface(rect)
                frames.append(pygame.transform.scale(surf, (ANCHO_MONEDA, ALTO_MONEDA)))
            cls._cache_frames[tipo] = frames
        return cls._cache_frames[tipo]

    def actualizar(self):
        # Avanza solo la animación de rotación en el punto de aparición.
        self._reloj_animacion += 1
        if self._reloj_animacion >= _TICKS_POR_FRAME:
            self._reloj_animacion = 0
            self._frame_actual = (self._frame_actual + 1) % _NUM_FRAMES

    def dibujar(self, superficie):
        superficie.blit(self._frames[self._frame_actual], (int(self.x), int(self.y)))
