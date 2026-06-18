import pygame
import random
from src.constantes import LINEA_HORIZONTE, ALTO, MARRON

class Comida:
# Modela el comportamiento y las dimensiones de la comida

    def __init__(self, x, y, tipo):
    # Inicializa las dimensiones, la velocidad y calcula el punto exacto de aterrizaje aleatorio dentro de la zona terrestre.\
        # Dimension fisica
        self.ancho = 15
        self.alto = 15
        
        # Posicion espacial
        self.x = x
        self.y = y
        
        # Atributos de velocidad de caida
        self.vy = 3
        
        # Selecciona un punto aleatorio en el eje Y que esté estrictamente dentro del pasto.
        self.y_destino = random.randint(LINEA_HORIZONTE, ALTO-100)

        self.tipo = tipo
    
    def caer(self):
    # Desplaza la comida verticalmente hacia abajo y activa un anclaje rígido en el momento en que toca su coordenada de destino.
    # Parecido a mover()
        if self.y < self.y_destino:
        # Mientras no hayamos alcanzado la altura de aterrizaje...
            self.y += self.vy   # Incrementamos la posición en Y (caída libre)
        else:
        # Al llegar o pasarnos, forzamos la posición en el destino exacto
            self.y = self.y_destino 
    
    def dibujar(self, superficie):
    # Dibuja físicamente el activo de comida en la pantalla del juego.
        pygame.draw.rect(superficie, MARRON, (int(self.x), int(self.y), self.ancho, self.alto))