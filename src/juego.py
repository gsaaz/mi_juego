import random
import pygame
from src.constantes import (ANCHO, ALTO, LINEA_HORIZONTE, FPS, ROJO)
from src.brainrot import BrainrotA, BrainrotB, BrainrotC, Brainrot, TAMANO_MAX_BRAINROT
from src.comida import Comida
from src.moneda import Moneda
from src.fondo import precargar_fondo, inicializar_entorno, dibujar_todo_el_entorno
from src.interfaz import (dibujar_hud_brainrot, dibujar_game_over, dibujar_indicador_monedas,
                           Tienda, COSTO_BRAINROT)
from src.guardado import guardar_partida, cargar_partida
from src.menu import MenuInicio
from src.audio import iniciar_musica_fondo, detener_musica_fondo, precargar_sfx, reproducir_recolectar_moneda
from src.fuentes import obtener_fuente, TAMANO_NORMAL

# Mapa de tipo de brainrot (string) a su clase concreta, usado al procesar compras.
_CLASES_BRAINROT = {"A": BrainrotA, "B": BrainrotB, "C": BrainrotC}


def _es_game_over(dinero, lista_brainrots):
    """
    Verifica las condiciones de derrota:
    El jugador pierde cuando no quedan criaturas vivas y tampoco hay dinero
    suficiente para adquirir un nuevo Brainrot en la tienda.
    """
    hay_vivos = any(brainrot.vivo for brainrot in lista_brainrots)
    return not hay_vivos and dinero < COSTO_BRAINROT

def _iniciar_partida_nueva(tienda):
    """Restablece los parámetros iniciales para empezar una partida desde cero."""
    tienda.cant_A = 5
    tienda.cant_B = 5
    tienda.cant_C = 5
    tienda.pestana_activa = "Comida"
    tienda.comida_seleccionada = "A"
    return {
        "dinero": 20,
        "lista_brainrots": [BrainrotA(400, 350)],
        "lista_comidas": [],
        "lista_monedas": [],
    }

def ejecutar_juego():
    """
    Función de arranque que inicializa los subsistemas de Pygame y 
    aloja el bucle infinito (Game Loop).
    """
    pygame.init() # Despierta submodulos internos de Pygame
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Villa Brainrot - Proyecto Final")

    iniciar_musica_fondo()
    precargar_sfx()

    precargar_fondo()  # Precarga el cielo antes de mostrar el menú
    menu = MenuInicio(ventana)
    menu.ejecutar()
    datos_cargados = menu.obtener_datos_cargados()

    Moneda.precargar()
    Comida.precargar()
    Brainrot.precargar()

    # Carga única de todo el escenario estático (prado + valla)
    mapa_prado, segmentos_valla = inicializar_entorno()

    reloj = pygame.time.Clock()
    fuente_chica = obtener_fuente(TAMANO_NORMAL)

    # Entidades y Estado
    lista_comidas = []
    lista_monedas = []
    frames_alerta_dinero = 0
    frames_alerta_stock  = 0

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
                    dinero          = estado_inicial["dinero"]
                    lista_brainrots = estado_inicial["lista_brainrots"]
                    lista_comidas   = estado_inicial["lista_comidas"]
                    lista_monedas   = estado_inicial["lista_monedas"]
                    frames_alerta_dinero = 0
                    frames_alerta_stock  = 0
                    game_over = False
                    guardar_partida(dinero, tienda, lista_brainrots)
                    continue

                pos_mouse = evento.pos

                # CAPA 1: INTERFAZ DE USUARIO
                # La tienda evalúa sus controles y reporta qué cambió.
                # Retorna None si el click no fue en ella.
                resultado_compra = tienda.procesar_click(pos_mouse, dinero)
                if resultado_compra is not None:
                    dinero = resultado_compra["dinero"]
                    if resultado_compra["alerta_dinero"]:
                        frames_alerta_dinero = resultado_compra["alerta_dinero"]
                    if resultado_compra["alerta_stock"]:
                        frames_alerta_stock = resultado_compra["alerta_stock"]
                    if resultado_compra["spawn_brainrot"]:
                        # El juego elige la posición y la clase concreta a instanciar
                        tipo = resultado_compra["spawn_brainrot"]
                        x = random.randint(0, ANCHO - TAMANO_MAX_BRAINROT)
                        y = random.randint(LINEA_HORIZONTE, ALTO - TAMANO_MAX_BRAINROT)
                        lista_brainrots.append(_CLASES_BRAINROT[tipo](x, y))
                    continue

                # CAPA 2: OBJETOS INTERACTIVOS
                moneda_recogida = False
                for moneda in lista_monedas:
                    hitbox_moneda = pygame.Rect(moneda.x, moneda.y, moneda.ancho, moneda.largo)
                    if hitbox_moneda.collidepoint(pos_mouse):
                        dinero += moneda.valor
                        lista_monedas.remove(moneda)
                        reproducir_recolectar_moneda()
                        moneda_recogida = True
                        break

                if moneda_recogida:
                    continue

                # CAPA 3: ACCIONES DEL MUNDO (lanzar comida al pasto)
                tipo  = tienda.comida_seleccionada
                stock = {"A": tienda.cant_A, "B": tienda.cant_B, "C": tienda.cant_C}[tipo]

                if stock > 0:
                    if tipo == "A":
                        tienda.cant_A -= 1
                    elif tipo == "B":
                        tienda.cant_B -= 1
                    else:
                        tienda.cant_C -= 1
                    lista_comidas.append(Comida(pos_mouse[0], pos_mouse[1], tipo))
                else:
                    frames_alerta_stock = 120

        # (b) ACTUALIZAR
        if not game_over:
            for brainrot in lista_brainrots:
                if brainrot.vivo:
                    brainrot.buscar_comida_cercana(lista_comidas)
                    brainrot.mover(lista_comidas)
                    brainrot.vivir(lista_monedas)

            for comida in lista_comidas:
                comida.caer()

            for moneda in lista_monedas:
                moneda.actualizar()

            if _es_game_over(dinero, lista_brainrots):
                game_over = True

        # (c) DIBUJAR — cielo, prado y valla en una sola llamada
        dibujar_todo_el_entorno(ventana, mapa_prado, segmentos_valla)

        # Alertas flotantes (zona del cielo, no tapan el prado)
        y_alertas = tienda.panel_superior.bottom + 12
        hay_alerta_dinero = frames_alerta_dinero > 0
        hay_alerta_stock  = frames_alerta_stock  > 0

        if hay_alerta_dinero:
            texto_alerta  = "¡FONDOS INSUFICIENTES!"
            imagen_alerta = fuente_chica.render(texto_alerta, True, ROJO)
            ventana.blit(imagen_alerta, ((ANCHO - imagen_alerta.get_width()) // 2, y_alertas))
            frames_alerta_dinero -= 1

        if hay_alerta_stock:
            texto_alerta  = "¡SIN STOCK!"
            imagen_alerta = fuente_chica.render(texto_alerta, True, ROJO)
            y_alerta = y_alertas + 32 if hay_alerta_dinero else y_alertas
            ventana.blit(imagen_alerta, ((ANCHO - imagen_alerta.get_width()) // 2, y_alerta))
            frames_alerta_stock -= 1

        # Entidades
        for brainrot in lista_brainrots:
            if brainrot.vivo:
                brainrot.dibujar(ventana)
                dibujar_hud_brainrot(ventana, fuente_chica, brainrot)

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
detener_musica_fondo()
