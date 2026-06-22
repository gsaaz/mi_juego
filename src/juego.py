import pygame
import random
from src.constantes import (ANCHO, ALTO, LINEA_HORIZONTE, FPS, 
                            NEGRO, ROJO, CELESTE, VERDE_PASTO)
from src.brainrot import BrainrotA, BrainrotB, BrainrotC
from src.comida import Comida
from src.interfaz import dibujar_hud_brainrot, Tienda

def ejecutar_juego():
    pygame.init() # Despierta submodulos internos de Pygame
    ventana = pygame.display.set_mode((ANCHO, ALTO)) 
    pygame.display.set_caption("Villa Brainrot - Proyecto Final") 
    reloj = pygame.time.Clock()  

    fuente_chica = pygame.font.SysFont("Arial", 22)

    # Entidades y Estado
    lista_brainrots = [] # Creamos a nuestro primer brainrot
    lista_comidas = [] # Creamos la lista dinámica que guardará las galletas vivas
    lista_monedas = []
    dinero = 100
    frames_alerta_dinero = 0
    frames_alerta_stock = 0

    tienda = Tienda()

    lista_brainrots.append(BrainrotA(400,350))
    lista_brainrots.append(BrainrotB(400,350))
    lista_brainrots.append(BrainrotC(400,350))

    corriendo = True  # Variable de control (Flag) que mantiene el juego encendido
    while corriendo:
        reloj.tick(FPS)
        
        # (a) EVENTOS (Interacción del Usuario con la PC)
        
        for evento in pygame.event.get():
             if evento.type == pygame.QUIT:
                  corriendo = False
                  continue
             
             if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
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
                        if dinero >= 50:
                            dinero -= 50
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
                        if dinero >= 50:
                            dinero -= 50
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
                        if dinero >= 50:
                            dinero -= 50
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
                        dinero += 20
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
        for brainrot in lista_brainrots:
            if brainrot.vivo:
                brainrot.buscar_comida_cercana(lista_comidas)
                brainrot.mover(lista_comidas) # Pasamos la lista corregida aquí
                brainrot.vivir(lista_monedas)
            
        for comida in lista_comidas:
            comida.caer()
    
        # (c) DIBUJAR
        # Pintamos toda la ventana de celeste para borrar los dibujos del frame anterior
        ventana.fill((CELESTE))

        texto_dinero = f"Monedas: ${dinero}"
        imagen_dinero = fuente_chica.render(texto_dinero, True, NEGRO)
        ventana.blit(imagen_dinero, (20, 20))

        if frames_alerta_dinero > 0:
            texto_alerta = "¡FONDOS INSUFICIENTES!"
            imagen_alerta = fuente_chica.render(texto_alerta, True, ROJO)
            ventana.blit(imagen_alerta, (200, 100))
            frames_alerta_dinero -= 1

        if frames_alerta_stock > 0:
            texto_alerta = "¡SIN STOCK!"
            imagen_alerta = fuente_chica.render(texto_alerta, True, ROJO)
            ventana.blit(imagen_alerta, (200, 100))
            frames_alerta_stock -= 1

        pygame.draw.rect(ventana, VERDE_PASTO, (0, LINEA_HORIZONTE, ANCHO, ALTO - LINEA_HORIZONTE))
        # Dibujamos el rectángulo verde que representa el jardín terrestre

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
                
        pygame.display.flip()
        # Envía el lienzo finalizado a la tarjeta de video para que lo muestre en el monitor

pygame.quit() # Apaga los submódulos de Pygame de forma ordenada para evitar que la ventana se congele
