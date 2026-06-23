import pygame
import os

RUTA_SPRITES = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "sprites", "coins-chests-etc-2-0-noborders.png",
)

# Configuración de los tipos de moneda: valor económico y ubicación Y en el spritesheet.
_CONFIGS = {
    "oro":    {"valor": 50, "fila_y": 16},
    "plata":  {"valor": 25, "fila_y": 32},
    "bronce": {"valor": 10, "fila_y": 48},
}

_FRAME_X_INICIO  = 16   # El spritesheet tiene 16px de margen vacío a la izquierda
_FRAME_W         = 16   # Ancho de cada frame en el spritesheet
_FRAME_H         = 16   # Alto de cada frame en el spritesheet
_NUM_FRAMES      = 9    # Frames requeridos para una rotación completa
_ESCALA          = 3    # Factor de escala (16x16 pasa a 48x48)
_TICKS_POR_FRAME = 6    # Velocidad de animación (cada cuántos ticks avanza un frame)

ANCHO_MONEDA = _FRAME_W * _ESCALA   # 48 px
ALTO_MONEDA  = _FRAME_H * _ESCALA   # 48 px


class Moneda:
    """
    Representa una moneda en el juego (Oro, Plata, Bronce).
    Genera animaciones de rotación leyendo sub-superficies de un spritesheet.
    """
    # Variables de clase compartidas por todas las monedas para ahorrar RAM
    _spritesheet   = None
    _cache_frames  = {}

    def __init__(self, x, y, tipo="bronce"):
        """
        Inicializa una moneda en la posición indicada.
        
        :param x: Posición X en la pantalla.
        :param y: Posición Y en la pantalla.
        :param tipo: "oro", "plata" o "bronce".
        """
        self.x    = float(x)
        self.y    = float(y)
        self.tipo = tipo

        config     = _CONFIGS.get(tipo, _CONFIGS["bronce"])
        self.valor = config["valor"]
        self._fila_y = config["fila_y"]

        self.ancho = ANCHO_MONEDA
        self.largo = ALTO_MONEDA

        self._frame_actual    = 0
        self._reloj_animacion = 0

        self._frames = self._obtener_frames(tipo, self._fila_y)

    @classmethod
    def precargar(cls):
        """Carga y procesa el spritesheet y sus frames al inicio del juego."""
        for tipo, config in _CONFIGS.items():
            cls._obtener_frames(tipo, config["fila_y"])

    @classmethod
    def _cargar_spritesheet(cls):
        """Carga la imagen maestra (spritesheet) a memoria una sola vez."""
        if cls._spritesheet is None:
            if not os.path.exists(RUTA_SPRITES):
                raise FileNotFoundError(f"No se encontró el spritesheet: {RUTA_SPRITES}")
            cls._spritesheet = pygame.image.load(RUTA_SPRITES).convert_alpha()
        return cls._spritesheet

    @classmethod
    def _obtener_frames(cls, tipo, fila_y):
        """Devuelve o genera la lista de frames escalados para un tipo de moneda."""
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
        """Avanza la animación (frame) de la moneda según los ticks."""
        self._reloj_animacion += 1
        if self._reloj_animacion >= _TICKS_POR_FRAME:
            self._reloj_animacion = 0
            self._frame_actual = (self._frame_actual + 1) % _NUM_FRAMES

    def dibujar(self, superficie):
        """
        Renderiza el frame actual de la moneda.
        
        :param superficie: Pantalla de pygame donde se dibujará.
        """
        superficie.blit(self._frames[self._frame_actual], (int(self.x), int(self.y)))
