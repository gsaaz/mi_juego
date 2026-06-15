import pygame
from src.constantes import (ANCHO, ALTO, LINEA_HORIZONTE, FPS, 
                            NEGRO, ROJO, CELESTE, VERDE_PASTO)
from src.brainrot import Brainrot
from src.comida import Comida

def ejecutar_juego():
    pygame.init() # Despierta submodulos internos de Pygame
    ventana = pygame.display.set_mode((ANCHO, ALTO)) 
    pygame.display.set_caption("Villa Brainrot - Proyecto Final") 
    reloj = pygame.time.Clock()  

    fuente_chica = pygame.font.SysFont("Arial", 22)

    # Entidades y Estado
    mi_criatura = Brainrot(400, 300) # Creamos a nuestro primer brainrot
    lista_comidas = [] # Creamos la lista dinámica que guardará las galletas vivas
    lista_monedas = []
    dinero = 100
    frames_alerta_dinero = 0

    corriendo = True  # Variable de control (Flag) que mantiene el juego encendido
    while corriendo:
        reloj.tick(FPS)
        
        # (a) EVENTOS (Interacción del Usuario con la PC)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
            # CASO 1: Si el usuario presiona la "X" roja para cerrar la ventana...
                corriendo = False        # Rompe el bucle while y apaga el juego
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
            # CASO 2: Si el usuario hace un clic con cualquiera de los botones del mouse...
                if evento.button == 1:   # Control de entrada: 1 significa Clic Izquierdo
                    mouse_x, mouse_y = evento.pos               # Extrae las coordenadas exactas del cursor
                    moneda_recogida = False
                    
                    for moneda in lista_monedas:
                        hitbox_moneda = pygame.Rect(moneda.x, moneda.y, moneda.ancho, moneda.largo)
                        if hitbox_moneda.collidepoint(evento.pos):
                            dinero += 20
                            lista_monedas.remove(moneda)
                            moneda_recogida = True
                            break
                    
                    if not moneda_recogida:
                        if dinero >= 5:
                            dinero -= 5
                            nueva_comida = Comida(mouse_x, mouse_y)     # Instanciamos una nueva comida
                            lista_comidas.append(nueva_comida)          # Guardamos la comida dentro de nuestra lista global
                        else:
                                frames_alerta_dinero = 120

        # (b) ACTUALIZAR
        if mi_criatura.vivo:
            mi_criatura.buscar_comida_cercana(lista_comidas)
            mi_criatura.mover(lista_comidas) # Pasamos la lista corregida aquí
            mi_criatura.vivir(lista_monedas)
            
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

        if mi_criatura.vivo:
                mi_criatura.dibujar(ventana)
                mi_criatura.dibujar_info(ventana, fuente_chica)
        # Le ordenamos a la criatura que dibuje su cuerpo blanco en la ventana
        # Dibujamos el texto flotante con las estadísticas vitales de la mascota

        for moneda in lista_monedas:
            moneda.dibujar(ventana)
        
        for comida in lista_comidas:
                comida.dibujar(ventana)
                
        pygame.display.flip()
        # Envía el lienzo finalizado a la tarjeta de video para que lo muestre en el monitor

pygame.quit() # Apaga los submódulos de Pygame de forma ordenada para evitar que la ventana se congele

    


