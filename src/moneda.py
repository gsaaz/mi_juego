import pygame
from src.constantes import AMARILLO_ORO

class Moneda:
# Modela el comportamiento y las dimensiones de las monedas
    
    def __init__(self, x, y):
        self.ancho = 30
        self.largo = 30
        
        self.x = x
        self.y = y
    
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, AMARILLO_ORO,(int(self.x),int(self.y),self.ancho,self.largo))