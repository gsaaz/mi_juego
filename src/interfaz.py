import pygame
from src.constantes import BLANCO

def dibujar_hud_brainrot(superficie, fuente, brainrot):
    texto_hambre = f"Hambre: {int(brainrot.hambre)}% | Salud: {int(brainrot.salud)}%"
    imagen_texto = fuente.render(texto_hambre, True, BLANCO)
    superficie.blit(imagen_texto, (int(brainrot.x) - 100, int(brainrot.y) - 25))

class Tienda:
    def __init__(self):
        # --- ESTADOS DE LA INTERFAZ ---
        self.pestana_activa = "Comida"  # "Comida" o "Brainrots" (Para la barra de arriba)
        self.comida_seleccionada = "A"   # "A", "B" o "C" (Para la barra de la derecha)

        # --- INVENTARIO DE COMIDA (Cantidad disponible para lanzar) ---
        self.cant_A = 5
        self.cant_B = 5
        self.cant_C = 5

        # --- GEOMETRÍA: BARRA HORIZONTAL (Tienda - Arriba) ---
        # Pestañas para cambiar el modo de la tienda
        self.btn_pestana_comida = pygame.Rect(200, 10, 120, 30)
        self.btn_pestana_brainrots = pygame.Rect(330, 10, 120, 30)
        
        # Botones de compra de la tienda (comparten posición, cambia su función)
        self.btn_compra_A = pygame.Rect(200, 45, 70, 35)
        self.btn_compra_B = pygame.Rect(280, 45, 70, 35)
        self.btn_compra_C = pygame.Rect(360, 45, 70, 35)

        # --- GEOMETRÍA: BARRA VERTICAL (Inventario/Selector - Derecha) ---
        # Estará siempre visible en el lateral derecho de la pantalla
        self.btn_sel_A = pygame.Rect(720, 120, 70, 50)
        self.btn_sel_B = pygame.Rect(720, 180, 70, 50)
        self.btn_sel_C = pygame.Rect(720, 240, 70, 50)