import os
import pygame
import random
from src.constantes import LINEA_HORIZONTE, ALTO

RUTAS_COOKIE = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites", "cookie.png"),
    os.path.join(os.path.dirname(__file__), "assets", "cookie.png"),
]

TAMANO_COOKIE = 28

class Comida:
    """
    Representa el elemento coleccionable 'galleta' dentro del juego.
    """
    _sprite = None

    @classmethod
    def _resolver_ruta_cookie(cls):
        """Busca el archivo de imagen de la galleta."""
        for ruta in RUTAS_COOKIE:
            if os.path.exists(ruta):
                return ruta
        raise FileNotFoundError(
            f"No se encontró cookie.png en: {', '.join(RUTAS_COOKIE)}"
        )

    @classmethod
    def precargar(cls):
        """Carga y escala el sprite de la galleta a la memoria caché."""
        if cls._sprite is not None:
            return cls._sprite

        imagen = pygame.image.load(cls._resolver_ruta_cookie()).convert_alpha()
        cls._sprite = pygame.transform.scale(imagen, (TAMANO_COOKIE, TAMANO_COOKIE))
        return cls._sprite

    def __init__(self, x, y, tipo):
        """
        Inicializa la galleta y establece su punto de aterrizaje.
        
        :param x: Posición horizontal (cursor del mouse).
        :param y: Posición vertical inicial.
        :param tipo: Tipo de comida ("A", "B", "C").
        """
        Comida.precargar()

        self.ancho = TAMANO_COOKIE
        self.alto = TAMANO_COOKIE
        self.x = x - self.ancho // 2
        self.y = y - self.alto // 2
        self.vy = 3
        # La comida caerá hasta un punto aleatorio dentro de la zona de pasto
        self.y_destino = random.randint(LINEA_HORIZONTE, ALTO - 100)
        self.tipo = tipo

    def caer(self):
        """Actualiza la posición Y de la galleta hasta llegar al suelo."""
        if self.y < self.y_destino:
            self.y += self.vy
        else:
            self.y = self.y_destino

    def dibujar(self, superficie):
        """Renderiza la galleta en la pantalla."""
        superficie.blit(Comida._sprite, (int(self.x), int(self.y)))
