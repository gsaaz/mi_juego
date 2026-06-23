import pygame
from src.constantes import (BLANCO, NEGRO, AMARILLO_ORO, MARRON, ROJO,
                            AZUL_NIEBLA, KHAKI, ROSADO, ANCHO, ALTO)
from src.fuentes import obtener_fuente, obtener_fuente_para_rect, TAMANO_MINIMO, TAMANO_PEQUENO, TAMANO_NORMAL, TAMANO_TITULO

def dibujar_indicador_monedas(superficie, fuente, dinero, rect):
    # Muestra el saldo alineado con la tienda, centrado en su propio recuadro.
    texto_dinero = f"Dinero: $ {dinero}"
    _dibujar_texto_en_rect(superficie, texto_dinero, rect, NEGRO, tamano_inicial=TAMANO_NORMAL, padding=2)

def dibujar_hud_brainrot(superficie, fuente, brainrot):
    texto_hambre = f"{brainrot.nombre} H:{int(brainrot.hambre)}% S:{int(brainrot.salud)}%"
    imagen_texto = fuente.render(texto_hambre, True, BLANCO)
    centro_x = int(brainrot.x) + brainrot.ancho // 2
    x = centro_x - imagen_texto.get_width() // 2
    y = int(brainrot.y) - imagen_texto.get_height() - 6
    superficie.blit(imagen_texto, (x, y))

def dibujar_game_over(superficie):
    # Superpone la pantalla de derrota cuando no quedan criaturas ni fondos para continuar.
    capa = pygame.Surface((ANCHO, ALTO))
    capa.set_alpha(180)
    capa.fill(NEGRO)
    superficie.blit(capa, (0, 0))

    lineas = [
        ("GAME OVER", ROJO, TAMANO_TITULO),
        ("Sin brainrots vivos y sin", BLANCO, TAMANO_PEQUENO + 1),
        ("dinero para comprar uno nuevo.", BLANCO, TAMANO_PEQUENO + 1),
        ("Haz clic para reiniciar.", BLANCO, TAMANO_PEQUENO),
    ]
    _dibujar_columna_textos(superficie, lineas, ALTO // 2, ancho_max=ANCHO - 80, espacio=14)

def _subrect_linea(rect, indice, total=2, gap=2):
    # Divide un rectángulo en franjas horizontales con separación entre líneas.
    alto_util = rect.height - gap * (total - 1)
    alto_linea = alto_util // total
    y = rect.y + indice * (alto_linea + gap)
    return pygame.Rect(rect.x, y, rect.width, alto_linea)

def _dibujar_texto_en_rect(superficie, texto, rect, color=NEGRO, tamano_inicial=TAMANO_PEQUENO, padding=1):
    # Dibuja texto centrado, reduciendo el tamaño si no cabe en el recuadro.
    area = pygame.Rect(
        rect.x + padding,
        rect.y + padding,
        max(1, rect.width - 2 * padding),
        max(1, rect.height - 2 * padding),
    )
    fuente = obtener_fuente_para_rect(
        texto, area.width, area.height, tamano_inicial=tamano_inicial,
    )
    imagen = fuente.render(texto, True, color)
    x = area.x + (area.width - imagen.get_width()) // 2
    y = area.y + (area.height - imagen.get_height()) // 2
    superficie.blit(imagen, (x, y))
    return imagen.get_height()

def _dibujar_boton_compra(superficie, rect, linea_superior, linea_inferior, color=NEGRO):
    # Dibuja etiqueta y precio centrados en dos filas dentro del botón de compra.
    borde = 2
    margen = 2
    interior = pygame.Rect(
        rect.x + borde + margen,
        rect.y + borde + margen,
        max(1, rect.width - 2 * (borde + margen)),
        max(1, rect.height - 2 * (borde + margen)),
    )
    gap = 3
    alto_superior = (interior.height - gap) // 2
    alto_inferior = interior.height - gap - alto_superior
    rect_superior = pygame.Rect(interior.x, interior.y, interior.width, alto_superior)
    rect_inferior = pygame.Rect(
        interior.x, interior.y + alto_superior + gap, interior.width, alto_inferior,
    )
    _dibujar_texto_en_rect(
        superficie, linea_superior, rect_superior, color, tamano_inicial=TAMANO_PEQUENO, padding=0,
    )
    _dibujar_texto_en_rect(
        superficie, linea_inferior, rect_inferior, color, tamano_inicial=TAMANO_MINIMO + 1, padding=0,
    )

def _dibujar_dos_lineas_en_rect(superficie, texto_arriba, texto_abajo, rect, color=NEGRO):
    # Coloca dos textos en filas separadas sin que se solapen.
    _dibujar_texto_en_rect(
        superficie, texto_arriba, _subrect_linea(rect, 0), color, tamano_inicial=TAMANO_PEQUENO, padding=1,
    )
    _dibujar_texto_en_rect(
        superficie, texto_abajo, _subrect_linea(rect, 1), color, tamano_inicial=TAMANO_MINIMO + 1, padding=1,
    )

def _dibujar_columna_textos(superficie, lineas, centro_y, ancho_max=None, espacio=12):
    # Apila líneas centradas vertical y horizontalmente sin superponerlas.
    if ancho_max is None:
        ancho_max = ANCHO - 80

    imagenes = []
    for texto, color, tamano_inicial in lineas:
        fuente = obtener_fuente_para_rect(texto, ancho_max, 80, tamano_inicial=tamano_inicial)
        imagenes.append((fuente.render(texto, True, color), espacio))

    alto_total = sum(img.get_height() for img, _ in imagenes)
    alto_total += espacio * (len(imagenes) - 1)
    y = centro_y - alto_total // 2

    for imagen, separacion in imagenes:
        x = (ANCHO - imagen.get_width()) // 2
        superficie.blit(imagen, (x, y))
        y += imagen.get_height() + separacion

def _rect_envolvente(rects, padding=2):
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
        ancho_btn = 104
        alto_btn = 52
        separacion = 8
        y_pestana = 4
        alto_pestana = 28
        y_compra = y_pestana + alto_pestana + 5
        self.btn_compra_A = pygame.Rect(0, y_compra, ancho_btn, alto_btn)
        self.btn_compra_B = pygame.Rect(ancho_btn + separacion, y_compra, ancho_btn, alto_btn)
        self.btn_compra_C = pygame.Rect(2 * (ancho_btn + separacion), y_compra, ancho_btn, alto_btn)

        # Pestañas centradas respecto al ancho de la fila de compra
        ancho_pestana = 108
        sep_pestanas = 8
        ancho_fila_pestanas = 2 * ancho_pestana + sep_pestanas
        x_pestanas = (self.btn_compra_C.right - ancho_fila_pestanas) // 2
        self.btn_pestana_comida = pygame.Rect(x_pestanas, y_pestana, ancho_pestana, alto_pestana)
        self.btn_pestana_brainrots = pygame.Rect(x_pestanas + ancho_pestana + sep_pestanas, y_pestana, ancho_pestana, alto_pestana)
        rects_superior = [
            self.btn_pestana_comida, self.btn_pestana_brainrots,
            self.btn_compra_A, self.btn_compra_B, self.btn_compra_C,
        ]
        self.panel_superior = _rect_envolvente(rects_superior)

        # --- INVENTARIO HORIZONTAL (selector de comida) ---
        separacion_barra = 14
        margen_superior = 6
        ancho_sel = 56
        alto_sel = self.panel_superior.height - 4
        sep_sel = 4
        self.btn_sel_A = pygame.Rect(0, 0, ancho_sel, alto_sel)
        self.btn_sel_B = pygame.Rect(ancho_sel + sep_sel, 0, ancho_sel, alto_sel)
        self.btn_sel_C = pygame.Rect(2 * (ancho_sel + sep_sel), 0, ancho_sel, alto_sel)
        rects_inventario = [self.btn_sel_A, self.btn_sel_B, self.btn_sel_C]
        self.panel_lateral = _rect_envolvente(rects_inventario, padding=2)

        self._posicionar_barra_superior(
            rects_superior, rects_inventario, separacion_barra, margen_superior,
        )

    def _posicionar_barra_superior(
        self, rects_tienda, rects_inventario, separacion, margen_superior,
    ):
        # Centra monedas, tienda e inventario como un solo bloque en la parte superior.
        panel_tienda = _rect_envolvente(rects_tienda)
        panel_inventario = _rect_envolvente(rects_inventario, padding=2)

        fuente_monedas = obtener_fuente(TAMANO_NORMAL)
        ancho_monedas = fuente_monedas.render("Monedas: $999", True, NEGRO).get_width() + 12
        ancho_grupo = (
            ancho_monedas + separacion + panel_tienda.width
            + separacion + panel_inventario.width
        )
        x_grupo = (ANCHO - ancho_grupo) // 2

        dx_tienda = x_grupo + ancho_monedas + separacion - panel_tienda.x
        dy_tienda = margen_superior - panel_tienda.y
        _desplazar_rects(rects_tienda, dx_tienda, dy_tienda)
        self.panel_superior = _rect_envolvente(rects_tienda)

        self.rect_monedas = pygame.Rect(
            x_grupo,
            self.panel_superior.y,
            ancho_monedas,
            self.panel_superior.height,
        )

        x_inventario = self.panel_superior.right + separacion
        y_inventario = self.panel_superior.y + (
            self.panel_superior.height - panel_inventario.height
        ) // 2
        _desplazar_rects(
            rects_inventario,
            x_inventario - panel_inventario.x,
            y_inventario - panel_inventario.y,
        )
        self.panel_lateral = _rect_envolvente(rects_inventario, padding=2)

    def dibujar(self, superficie, fuente):
        # Renderiza la barra superior de la tienda y el selector lateral de comida.
        # --- BARRA SUPERIOR DE LA TIENDA ---
        pygame.draw.rect(superficie, MARRON, self.panel_superior)

        color_tab_comida = AMARILLO_ORO if self.pestana_activa == "Comida" else (100, 80, 60)
        color_tab_brainrots = AMARILLO_ORO if self.pestana_activa == "Brainrots" else (100, 80, 60)

        pygame.draw.rect(superficie, color_tab_comida, self.btn_pestana_comida)
        pygame.draw.rect(superficie, color_tab_brainrots, self.btn_pestana_brainrots)
        pygame.draw.rect(superficie, NEGRO, self.btn_pestana_comida, 2)
        pygame.draw.rect(superficie, NEGRO, self.btn_pestana_brainrots, 2)

        _dibujar_texto_en_rect(superficie, "Comida", self.btn_pestana_comida, tamano_inicial=TAMANO_PEQUENO)
        _dibujar_texto_en_rect(superficie, "Brainrot", self.btn_pestana_brainrots, tamano_inicial=TAMANO_MINIMO + 2)

        botones_compra = [
            (self.btn_compra_A, "A", AZUL_NIEBLA),
            (self.btn_compra_B, "B", KHAKI),
            (self.btn_compra_C, "C", ROSADO),
        ]
        costo = 10 if self.pestana_activa == "Comida" else 50
        prefijo = "Cda" if self.pestana_activa == "Comida" else "Br"

        for rect, letra, color_tipo in botones_compra:
            pygame.draw.rect(superficie, color_tipo, rect)
            pygame.draw.rect(superficie, NEGRO, rect, 2)
            _dibujar_boton_compra(
                superficie, rect, f"{prefijo} {letra}", f"${costo}",
            )

        # --- INVENTARIO SUPERIOR (selector de comida, a la derecha de la tienda) ---
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

            _dibujar_dos_lineas_en_rect(superficie, letra, f"x{cantidad}", rect)
