import pygame
from src.constantes import BLANCO

def dibujar_hud_brainrot(superficie, fuente, brainrot):
    texto_hambre = f"Hambre: {int(brainrot.hambre)}% | Salud: {int(brainrot.salud)}%"
    imagen_texto = fuente.render(texto_hambre, True, BLANCO)
    superficie.blit(imagen_texto, (int(brainrot.x) - 100, int(brainrot.y) - 25))
