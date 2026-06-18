import pygame
from src.constantes import (ANCHO, ALTO, LINEA_HORIZONTE, FPS, 
                            NEGRO, ROJO, CELESTE, VERDE_PASTO)
from src.brainrot import Brainrot, BrainrotA, BrainrotB, BrainrotC
from src.comida import Comida
from src.interfaz import dibujar_hud_brainrot

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

                # CAPA 2: OBJETOS INTERACTIVOS
                moneda_recogida = False
                for moneda in lista_monedas:
                    hitbox_moneda = pygame.Rect(moneda.x, moneda.y, moneda.ancho, moneda.largo)
                    if hitbox_moneda.collidepoint(pos_mouse):
                        dinero += 20
                        lista_monedas.remove()
                        moneda_recogida = True
                        break
                
                if moneda_recogida:
                     continue
                
                # CAPA 3: ACCIONES DEL MUNDO
                if dinero < 5:
                     frames_alerta_dinero = 120
                     continue
                
                dinero -= 5
                nueva_comida = Comida(pos_mouse[0],pos_mouse[1],"A")
                lista_comidas.append(nueva_comida)

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
            ventana.blit(imagen_alerta, (200, 20))
            frames_alerta_dinero -= 1

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
                
        pygame.display.flip()
        # Envía el lienzo finalizado a la tarjeta de video para que lo muestre en el monitor

pygame.quit() # Apaga los submódulos de Pygame de forma ordenada para evitar que la ventana se congele
