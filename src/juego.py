import os
import pygame
import random
from src.constantes import (ANCHO, ALTO, LINEA_HORIZONTE, FPS, 
                            NEGRO, BLANCO, ROJO)
from src.brainrot import BrainrotA, BrainrotB, BrainrotC
from src.comida import Comida
from src.moneda import Moneda
from src.fondo import precargar_fondo, dibujar_fondo_cielo
from src.interfaz import dibujar_hud_brainrot, dibujar_game_over, dibujar_indicador_monedas, Tienda
from src.guardado import guardar_partida, cargar_partida
from src.menu import MenuInicio
from src.fuentes import obtener_fuente, TAMANO_NORMAL

COSTO_BRAINROT = 50
TAMANO_BLOQUE = 32
ANCHO_VALLA = 64
ALTO_VALLA = 48
OFFSET_VALLA_Y = 16  # La base de la valla se hunde en el pasto (LINEA_HORIZONTE - OFFSET)
RUTAS_PASTO = [
    os.path.join(os.path.dirname(__file__), "assets"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites"),
]
RUTAS_VALLA = [
    os.path.join(os.path.dirname(__file__), "assets"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites"),
]
NOMBRES_VALLA = ("valla.png", "valla.jpg", "fence.png", "fence.jpg")

def _resolver_ruta_valla():
    # Busca el sprite de la valla en src/assets o assets/sprites.
    for carpeta in RUTAS_VALLA:
        for nombre in NOMBRES_VALLA:
            ruta = os.path.join(carpeta, nombre)
            if os.path.exists(ruta):
                return ruta
    raise FileNotFoundError(
        f"No se encontró la valla (valla.png / fence.jpg) en: {', '.join(RUTAS_VALLA)}"
    )

def _cargar_valla():
    # Carga y escala el segmento de valla (3 postes) para repetirlo a lo largo del horizonte.
    imagen = pygame.image.load(_resolver_ruta_valla()).convert_alpha()
    return pygame.transform.scale(imagen, (ANCHO_VALLA, ALTO_VALLA))

def _construir_segmentos_valla(sprite_valla):
    # Precalcula los segmentos de valla para cubrir todo el ancho sin huecos.
    segmentos = []
    x = 0
    while x < ANCHO:
        ancho_restante = ANCHO - x
        if ancho_restante >= ANCHO_VALLA:
            segmentos.append((x, sprite_valla))
        else:
            segmentos.append((
                x,
                sprite_valla.subsurface((0, 0, ancho_restante, ALTO_VALLA)).copy(),
            ))
        x += ANCHO_VALLA
    return segmentos

def _dibujar_valla(superficie, segmentos_valla):
    # Pinta la cerca sobre el horizonte, tapando la unión entre cielo y pasto.
    pos_y = LINEA_HORIZONTE - OFFSET_VALLA_Y
    for x, imagen in segmentos_valla:
        superficie.blit(imagen, (x, pos_y))

def _resolver_ruta_textura(nombre_base):
    # Busca la textura en src/assets o assets/sprites (.jpg o .png).
    for carpeta in RUTAS_PASTO:
        for extension in (".jpg", ".jpeg", ".png"):
            ruta = os.path.join(carpeta, f"{nombre_base}{extension}")
            if os.path.exists(ruta):
                return ruta
    raise FileNotFoundError(
        f"No se encontró la textura '{nombre_base}' en: {', '.join(RUTAS_PASTO)}"
    )

def _cargar_textura_pasto(nombre_base):
    # Carga una textura del prado y la escala a un bloque de 32×32 píxeles.
    imagen = pygame.image.load(_resolver_ruta_textura(nombre_base)).convert()
    return pygame.transform.scale(imagen, (TAMANO_BLOQUE, TAMANO_BLOQUE))

def _es_game_over(dinero, lista_brainrots):
    # Derrota: no hay criaturas vivas y no alcanza el dinero para comprar una nueva.
    hay_vivos = any(brainrot.vivo for brainrot in lista_brainrots)
    return not hay_vivos and dinero < COSTO_BRAINROT

def _iniciar_partida_nueva(tienda):
    # Restablece el estado inicial de una partida desde cero.
    tienda.cant_A = 5
    tienda.cant_B = 5
    tienda.cant_C = 5
    tienda.pestana_activa = "Comida"
    tienda.comida_seleccionada = "A"
    return {
        "dinero": 20,
        "lista_brainrots": [
            BrainrotA(400, 350)
        ],
        "lista_comidas": [],
        "lista_monedas": [],
    }

def _celda_textura(textura, ancho, alto):
    # Ajusta el bloque al borde del prado (solo al generar el mapa, no en el bucle de dibujo).
    if ancho == TAMANO_BLOQUE and alto == TAMANO_BLOQUE:
        return textura
    return textura.subsurface((0, 0, ancho, alto)).copy()

def _generar_mapa_prado(tile_pasto_base, tile_pasto_flores, tile_pasto_alto):
    # Construye una sola vez la matriz estática del prado (85% base, 10% flores, 5% alto).
    mapa_prado = []

    for y in range(LINEA_HORIZONTE, ALTO, TAMANO_BLOQUE):
        for x in range(0, ANCHO, TAMANO_BLOQUE):
            ancho = min(TAMANO_BLOQUE, ANCHO - x)
            alto = min(TAMANO_BLOQUE, ALTO - y)
            probabilidad = random.random()

            if probabilidad < 0.85:
                textura = tile_pasto_base
            elif probabilidad < 0.95:
                textura = tile_pasto_flores
            else:
                textura = tile_pasto_alto

            mapa_prado.append((x, y, _celda_textura(textura, ancho, alto)))

    return mapa_prado

def ejecutar_juego():
    pygame.init() # Despierta submodulos internos de Pygame
    ventana = pygame.display.set_mode((ANCHO, ALTO)) 
    pygame.display.set_caption("Villa Brainrot - Proyecto Final") 

    precargar_fondo()
    menu = MenuInicio(ventana)
    menu.ejecutar()
    datos_cargados = menu.obtener_datos_cargados()

    Moneda.precargar()

    tile_pasto_base = _cargar_textura_pasto("grass_1")
    tile_pasto_flores = _cargar_textura_pasto("grass_2")
    tile_pasto_alto = _cargar_textura_pasto("grass_3")
    mapa_prado = _generar_mapa_prado(tile_pasto_base, tile_pasto_flores, tile_pasto_alto)

    sprite_valla = _cargar_valla()
    segmentos_valla = _construir_segmentos_valla(sprite_valla)

    reloj = pygame.time.Clock()

    fuente_chica = obtener_fuente(TAMANO_NORMAL)

    # Entidades y Estado
    lista_comidas = [] # Creamos la lista dinámica que guardará las galletas vivas
    lista_monedas = []
    frames_alerta_dinero = 0
    frames_alerta_stock = 0

    tienda = Tienda()

    if datos_cargados:
        dinero = datos_cargados["dinero"]
        tienda.cant_A = datos_cargados["cant_A"]
        tienda.cant_B = datos_cargados["cant_B"]
        tienda.cant_C = datos_cargados["cant_C"]
        lista_brainrots = datos_cargados["lista_brainrots"]
    else:
        estado_inicial = _iniciar_partida_nueva(tienda)
        dinero = estado_inicial["dinero"]
        lista_brainrots = estado_inicial["lista_brainrots"]

    game_over = _es_game_over(dinero, lista_brainrots)

    corriendo = True  # Variable de control (Flag) que mantiene el juego encendido
    while corriendo:
        reloj.tick(FPS)
        
        # (a) EVENTOS (Interacción del Usuario con la PC)
        
        for evento in pygame.event.get():
             if evento.type == pygame.QUIT:
                  guardar_partida(dinero, tienda, lista_brainrots)
                  corriendo = False
                  continue
             
             if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if game_over:
                    estado_inicial = _iniciar_partida_nueva(tienda)
                    dinero = estado_inicial["dinero"]
                    lista_brainrots = estado_inicial["lista_brainrots"]
                    lista_comidas = estado_inicial["lista_comidas"]
                    lista_monedas = estado_inicial["lista_monedas"]
                    frames_alerta_dinero = 0
                    frames_alerta_stock = 0
                    game_over = False
                    guardar_partida(dinero, tienda, lista_brainrots)
                    continue

                pos_mouse = evento.pos

                # CAPA 1: INTERFAZ DE USUARIO
                click_en_tienda = False

                if tienda.btn_pestana_comida.collidepoint(pos_mouse):
                    tienda.pestana_activa = "Comida"
                    click_en_tienda = True
                elif tienda.btn_pestana_brainrots.collidepoint(pos_mouse):
                    tienda.pestana_activa = "Brainrots"
                    click_en_tienda = True
                elif tienda.btn_sel_A.collidepoint(pos_mouse):
                    tienda.comida_seleccionada = "A"
                    click_en_tienda = True
                elif tienda.btn_sel_B.collidepoint(pos_mouse):
                    tienda.comida_seleccionada = "B"
                    click_en_tienda = True
                elif tienda.btn_sel_C.collidepoint(pos_mouse):
                    tienda.comida_seleccionada = "C"
                    click_en_tienda = True
                elif tienda.btn_compra_A.collidepoint(pos_mouse):
                    click_en_tienda = True
                    if tienda.pestana_activa == "Brainrots":
                        if dinero >= COSTO_BRAINROT:
                            dinero -= COSTO_BRAINROT
                            x = random.randint(0, ANCHO - 50)
                            y = random.randint(LINEA_HORIZONTE, ALTO - 50)
                            lista_brainrots.append(BrainrotA(x, y))
                        else:
                            frames_alerta_dinero = 120
                    else:
                        if dinero >= 10:
                            dinero -= 10
                            tienda.cant_A += 1
                        else:
                            frames_alerta_dinero = 120
                elif tienda.btn_compra_B.collidepoint(pos_mouse):
                    click_en_tienda = True
                    if tienda.pestana_activa == "Brainrots":
                        if dinero >= COSTO_BRAINROT:
                            dinero -= COSTO_BRAINROT
                            x = random.randint(0, ANCHO - 50)
                            y = random.randint(LINEA_HORIZONTE, ALTO - 50)
                            lista_brainrots.append(BrainrotB(x, y))
                        else:
                            frames_alerta_dinero = 120
                    else:
                        if dinero >= 10:
                            dinero -= 10
                            tienda.cant_B += 1
                        else:
                            frames_alerta_dinero = 120
                elif tienda.btn_compra_C.collidepoint(pos_mouse):
                    click_en_tienda = True
                    if tienda.pestana_activa == "Brainrots":
                        if dinero >= COSTO_BRAINROT:
                            dinero -= COSTO_BRAINROT
                            x = random.randint(0, ANCHO - 50)
                            y = random.randint(LINEA_HORIZONTE, ALTO - 50)
                            lista_brainrots.append(BrainrotC(x, y))
                        else:
                            frames_alerta_dinero = 120
                    else:
                        if dinero >= 10:
                            dinero -= 10
                            tienda.cant_C += 1
                        else:
                            frames_alerta_dinero = 120

                if click_en_tienda:
                    continue

                # CAPA 2: OBJETOS INTERACTIVOS
                moneda_recogida = False
                for moneda in lista_monedas:
                    hitbox_moneda = pygame.Rect(moneda.x, moneda.y, moneda.ancho, moneda.largo)
                    if hitbox_moneda.collidepoint(pos_mouse):
                        dinero += moneda.valor
                        lista_monedas.remove(moneda)
                        moneda_recogida = True
                        break
                
                if moneda_recogida:
                     continue
                
                # CAPA 3: ACCIONES DEL MUNDO (cielo o pasto)
                tipo = tienda.comida_seleccionada
                stock = {"A": tienda.cant_A, "B": tienda.cant_B, "C": tienda.cant_C}[tipo]

                if stock > 0:
                    if tipo == "A":
                        tienda.cant_A -= 1
                    elif tipo == "B":
                        tienda.cant_B -= 1
                    else:
                        tienda.cant_C -= 1
                    nueva_comida = Comida(pos_mouse[0], pos_mouse[1], tipo)
                    lista_comidas.append(nueva_comida)
                else:
                    frames_alerta_stock = 120

        # (b) ACTUALIZAR
        if not game_over:
            for brainrot in lista_brainrots:
                if brainrot.vivo:
                    brainrot.buscar_comida_cercana(lista_comidas)
                    brainrot.mover(lista_comidas) # Pasamos la lista corregida aquí
                    brainrot.vivir(lista_monedas)
            
            for comida in lista_comidas:
                comida.caer()

            for moneda in lista_monedas:
                moneda.actualizar()

            if _es_game_over(dinero, lista_brainrots):
                game_over = True
    
        # (c) DIBUJAR
        dibujar_fondo_cielo(ventana)

        y_alertas = tienda.panel_superior.bottom + 12
        hay_alerta_dinero = frames_alerta_dinero > 0
        hay_alerta_stock = frames_alerta_stock > 0

        if hay_alerta_dinero:
            texto_alerta = "¡FONDOS INSUFICIENTES!"
            imagen_alerta = fuente_chica.render(texto_alerta, True, ROJO)
            ventana.blit(imagen_alerta, ((ANCHO - imagen_alerta.get_width()) // 2, y_alertas))
            frames_alerta_dinero -= 1

        if hay_alerta_stock:
            texto_alerta = "¡SIN STOCK!"
            imagen_alerta = fuente_chica.render(texto_alerta, True, ROJO)
            y_alerta = y_alertas + 32 if hay_alerta_dinero else y_alertas
            ventana.blit(imagen_alerta, ((ANCHO - imagen_alerta.get_width()) // 2, y_alerta))
            frames_alerta_stock -= 1

        for x, y, imagen_pasto in mapa_prado:
            ventana.blit(imagen_pasto, (x, y))

        _dibujar_valla(ventana, segmentos_valla)

        for brainrot in lista_brainrots:
            if brainrot.vivo:
                    brainrot.dibujar(ventana)
                    dibujar_hud_brainrot(ventana,fuente_chica,brainrot)
        # Le ordenamos a la criatura que dibuje su cuerpo blanco en la ventana
        # Dibujamos el texto flotante con las estadísticas vitales de la mascota

        for moneda in lista_monedas:
            moneda.dibujar(ventana)
        
        for comida in lista_comidas:
                comida.dibujar(ventana)

        tienda.dibujar(ventana, fuente_chica)
        dibujar_indicador_monedas(ventana, fuente_chica, dinero, tienda.rect_monedas)

        if game_over:
            dibujar_game_over(ventana)
                
        pygame.display.flip()
        # Envía el lienzo finalizado a la tarjeta de video para que lo muestre en el monitor

pygame.quit() # Apaga los submódulos de Pygame de forma ordenada para evitar que la ventana se congele
