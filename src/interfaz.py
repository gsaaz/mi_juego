import pygame
from src.constantes import (BLANCO, NEGRO, AMARILLO_ORO, MARRON, ROJO,
                            AZUL_NIEBLA, KHAKI, ROSADO, ANCHO, ALTO)

def dibujar_hud_brainrot(superficie, fuente, brainrot):
    texto_hambre = f"Hambre: {int(brainrot.hambre)}% | Salud: {int(brainrot.salud)}%"
    imagen_texto = fuente.render(texto_hambre, True, BLANCO)
    superficie.blit(imagen_texto, (int(brainrot.x) - 100, int(brainrot.y) - 25))

def _centrar_texto(superficie, fuente, texto, rect, color=NEGRO, offset_y=0):
    # Dibuja un texto centrado dentro de un rectángulo.
    imagen = fuente.render(texto, True, color)
    x = rect.x + (rect.width - imagen.get_width()) // 2
    y = rect.y + (rect.height - imagen.get_height()) // 2 + offset_y
    superficie.blit(imagen, (x, y))

def _rect_envolvente(rects, padding=5):
    # Calcula el rectángulo mínimo que rodea a un grupo de elementos.
    izquierda = min(r.x for r in rects)
    arriba = min(r.y for r in rects)
    derecha = max(r.right for r in rects)
    abajo = max(r.bottom for r in rects)
    return pygame.Rect(izquierda - padding, arriba - padding,
                       derecha - izquierda + 2 * padding,
                       abajo - arriba + 2 * padding)

def _desplazar_rects(rects, dx, dy):
    # Mueve un grupo de rectángulos manteniendo sus proporciones relativas.
    for rect in rects:
        rect.x += dx
        rect.y += dy

class Tienda:
    def __init__(self):
        # --- ESTADOS DE LA INTERFAZ ---
        self.pestana_activa = "Comida"  # "Comida" o "Brainrots" (Para la barra de arriba)
        self.comida_seleccionada = "A"   # "A", "B" o "C" (Para la barra de la derecha)

        # --- INVENTARIO DE COMIDA (Cantidad disponible para lanzar) ---
        self.cant_A = 5
        self.cant_B = 5
        self.cant_C = 5

        # --- GEOMETRÍA LOCAL: BARRA HORIZONTAL (Tienda - Arriba) ---
        ancho_btn = 92
        alto_btn = 36
        separacion = 8
        y_compra = 42
        self.btn_compra_A = pygame.Rect(0, y_compra, ancho_btn, alto_btn)
        self.btn_compra_B = pygame.Rect(ancho_btn + separacion, y_compra, ancho_btn, alto_btn)
        self.btn_compra_C = pygame.Rect(2 * (ancho_btn + separacion), y_compra, ancho_btn, alto_btn)

        # Pestañas centradas respecto al ancho de la fila de compra
        ancho_pestana = 110
        sep_pestanas = 6
        ancho_fila_pestanas = 2 * ancho_pestana + sep_pestanas
        x_pestanas = (self.btn_compra_C.right - ancho_fila_pestanas) // 2
        self.btn_pestana_comida = pygame.Rect(x_pestanas, 10, ancho_pestana, 26)
        self.btn_pestana_brainrots = pygame.Rect(x_pestanas + ancho_pestana + sep_pestanas, 10, ancho_pestana, 26)
        rects_superior = [
            self.btn_pestana_comida, self.btn_pestana_brainrots,
            self.btn_compra_A, self.btn_compra_B, self.btn_compra_C,
        ]
        self.panel_superior = _rect_envolvente(rects_superior)
        _desplazar_rects(rects_superior, (ANCHO - self.panel_superior.width) // 2 - self.panel_superior.x, 0)
        self.panel_superior = _rect_envolvente(rects_superior)

        # --- GEOMETRÍA LOCAL: BARRA VERTICAL (Inventario/Selector - Derecha) ---
        ancho_sel = 72
        alto_sel = 48
        paso_sel = 54
        self.btn_sel_A = pygame.Rect(0, 0, ancho_sel, alto_sel)
        self.btn_sel_B = pygame.Rect(0, paso_sel, ancho_sel, alto_sel)
        self.btn_sel_C = pygame.Rect(0, 2 * paso_sel, ancho_sel, alto_sel)

        rects_lateral = [self.btn_sel_A, self.btn_sel_B, self.btn_sel_C]
        self.panel_lateral = _rect_envolvente(rects_lateral)
        margen = 8
        destino_x = ANCHO - self.panel_lateral.width - margen
        destino_y = (ALTO - self.panel_lateral.height) // 2
        _desplazar_rects(rects_lateral, destino_x - self.panel_lateral.x, destino_y - self.panel_lateral.y)
        self.panel_lateral = _rect_envolvente(rects_lateral)

    def dibujar(self, superficie, fuente):
    # Renderiza la barra superior de la tienda y el selector lateral de comida.
        fuente_peq = pygame.font.SysFont("Arial", 17)
        fuente_etiq = pygame.font.SysFont("Arial", 20)

        # --- BARRA SUPERIOR DE LA TIENDA ---
        pygame.draw.rect(superficie, MARRON, self.panel_superior)

        color_tab_comida = AMARILLO_ORO if self.pestana_activa == "Comida" else (100, 80, 60)
        color_tab_brainrots = AMARILLO_ORO if self.pestana_activa == "Brainrots" else (100, 80, 60)

        pygame.draw.rect(superficie, color_tab_comida, self.btn_pestana_comida)
        pygame.draw.rect(superficie, color_tab_brainrots, self.btn_pestana_brainrots)
        pygame.draw.rect(superficie, NEGRO, self.btn_pestana_comida, 2)
        pygame.draw.rect(superficie, NEGRO, self.btn_pestana_brainrots, 2)

        _centrar_texto(superficie, fuente_peq, "Comida", self.btn_pestana_comida)
        _centrar_texto(superficie, fuente_peq, "Brainrots", self.btn_pestana_brainrots)

        botones_compra = [
            (self.btn_compra_A, "A", AZUL_NIEBLA),
            (self.btn_compra_B, "B", KHAKI),
            (self.btn_compra_C, "C", ROSADO),
        ]
        costo = 10 if self.pestana_activa == "Comida" else 50
        prefijo = "Comida" if self.pestana_activa == "Comida" else "Brain"

        for rect, letra, color_tipo in botones_compra:
            pygame.draw.rect(superficie, color_tipo, rect)
            pygame.draw.rect(superficie, NEGRO, rect, 2)
            _centrar_texto(superficie, fuente_peq, f"{prefijo} {letra}", rect, offset_y=-8)
            _centrar_texto(superficie, fuente_etiq, f"${costo}", rect, offset_y=9)

        # --- BARRA LATERAL DERECHA (Selector de comida) ---
        pygame.draw.rect(superficie, MARRON, self.panel_lateral)

        selectores = [
            (self.btn_sel_A, "A", self.cant_A, AZUL_NIEBLA),
            (self.btn_sel_B, "B", self.cant_B, KHAKI),
            (self.btn_sel_C, "C", self.cant_C, ROSADO),
        ]

        for rect, letra, cantidad, color_tipo in selectores:
            seleccionado = self.comida_seleccionada == letra
            color_fondo = AMARILLO_ORO if seleccionado else color_tipo
            grosor_borde = 4 if seleccionado else 2

            pygame.draw.rect(superficie, color_fondo, rect)
            pygame.draw.rect(superficie, ROJO if seleccionado else NEGRO, rect, grosor_borde)

            _centrar_texto(superficie, fuente_peq, f"Comida {letra}", rect, offset_y=-9)
            _centrar_texto(superficie, fuente_etiq, f"x{cantidad}", rect, offset_y=11)
