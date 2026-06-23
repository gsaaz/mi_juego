import pygame
import random
from src.constantes import ANCHO, ALTO, LINEA_HORIZONTE, BLANCO, TIPOS_BRAINROT
from src.moneda import Moneda, ANCHO_MONEDA

class Brainrot:
# Representa las entidades de la villa (brainrots)
    
    def __init__(self, x, y):
    # Se ejecuta al instanciar el personaje
        # Atributos fisicos
        self.ancho = 50
        self.alto = 50
        self.color = BLANCO
        self.nombre = ""
        self.tipo_dieta = ""

        # Posicion espacial
        self.x = x
        self.y = y
        
        # Atributos de velocidad
        self.vx = 4
        self.vy = 2
        
        # Atributos biologicos
        self.hambre = 100
        self.salud = 100
        self.edad = 0
        
        # Atributos de estado y decision
        self.comida_objetivo = None  
        self.estado = "paseando"
        
        self.reloj_moneda = 0
        
        self.vivo = True
    
    def buscar_comida_cercana(self, lista_comidas):
    # Calcula donde esta la comida mas cercana que ya aterrizo para ir por ella
        comidas_listas = [c for c in lista_comidas if c.y >= c.y_destino]
        # Sublista en memoria que incluye SOLO las comidas que ya terminaron de caer
        
        if not comidas_listas:
        # Si la sublista esta vacia (no hay comida en el suelo)...
            self.estado = "paseando"    # Regresa a su comportamiento aleatorio por defecto
            self.comida_objetivo = None # Limpia cualquier objetivo antiguo
            return                      # Corta la función inmediatamente para no gastar procesador
        
        comida_mas_cercana = None
        distancia_minima = float("inf")
        # Inicializamos la distancia con "Infinito" (float("inf")) para asegurarnos de que 
        # cualquier distancia real calculada en el primer intento sea menor que este valor inicial
        
        for comida in comidas_listas:
            dx = comida.x - self.x
            dy = comida.y - self.y
            distancia = (dx**2 + dy**2)**0.5
            # Formula de distancia entre dos puntos en espacio cartesiano: sqrt(dx^2 + dy^2) 
            
            if distancia < distancia_minima:
            # Si esta galleta está más cerca que la anterior que habíamos guardado...
                distancia_minima = distancia    # Actualizamos el récord de la distancia más corta
                comida_mas_cercana = comida     # Guardamos temporalmente esta galleta como la favorita
                
        if comida_mas_cercana:
            self.comida_objetivo = comida_mas_cercana  # Anclamos la galleta elegida a la memoria del brainrot
            self.estado = "buscando_comida"            # Cambiamos su estado mental para activar la persecución

    def mover(self, lista_comidas):
    # Controla el desplazamiento del brainrot por la pantalla según su estado mental,
    # reubica su posición ante choques con los límites y gestiona el mordisco.
    #=========================================================
    # SECCIÓN A: ESTADOS
    #=========================================================
       # --- ESTADO 1: COMPORTAMIENTO ALEATORIO (PASEANDO) ---
       if self.estado == "paseando":
       # Sumamos pequeñas variaciones de aceleración en cada frame
           self.vx += random.uniform(-0.5, 0.5)
           self.vy += random.uniform(-1, 1)
           
           # Límites de Velocidad
           if self.vx > 5:
               self.vx = 5
           if self.vx < -5:  
                self.vx = -5
           if self.vy > 3:   
                self.vy = 3
           if self.vy < -3:  
                self.vy = -3
                
       # --- ESTADO 2: PERSECUCIÓN ACTIVA (BUSCANDO COMIDA) ---
       elif self.estado == "buscando_comida" and self.comida_objetivo:
           if self.comida_objetivo not in lista_comidas:
           # Si otro brainrot se comió nuestra galleta antes...
                self.estado = "paseando"        # Abandona la persecución
                self.comida_objetivo = None     # Resetea el objetivo
           else:
           # Calculamos el vector de distancia entre el personaje y su objetivo
               distancia_x = self.comida_objetivo.x - self.x
               distancia_y = self.comida_objetivo.y - self.y
                
               if abs(distancia_x) < 4:
               # Si estamos a menos de 4 píxeles, nos alineamos exactamente para evitar vibraciones
                    self.x = self.comida_objetivo.x
                    self.vx = 0     # Frenamos el movimiento horizontal
               else:
               # Si estamos lejos, avanzamos a velocidad 4 en la dirección correcta hacia la comida
                    self.vx = 4 if distancia_x > 0 else -4
                
               if abs(distancia_y) < 4:
               # Si estamos a menos de 4 píxeles en vertical, nos alineamos
                    self.y = self.comida_objetivo.y
                    self.vy = 0     # Frenamos el movimiento vertical
               else:
               # Si estamos lejos, avanzamos a velocidad 4 hacia arriba o hacia abajo    
                    self.vy = 4 if distancia_y > 0 else -4
    #=========================================================
    # SECCION B: APLICACIÓN DEL PASO
    #=========================================================
       # Desplazamos físicamente el objeto sumando los vectores de velocidad a sus coordenadas
       self.x += self.vx
       self.y += self.vy
       
       # Colisiones Horizontales
       if self.x <= 0:
            self.x = 0      # Reubicación forzada en el origen izquierdo
            self.vx *= -1   # Invierte el sentido del vector horizontal
       elif self.x >= ANCHO - self.ancho:
            self.x = ANCHO - self.ancho     # Reubicación forzada en el borde derecho
            self.vx *= -1                   # Invierte el sentido del vector horizontal
        
       # Colisiones Verticales (Fronteras del suelo)
       if self.y <= LINEA_HORIZONTE:
            self.y = LINEA_HORIZONTE  # Evita que el brainrot flote hacia el cielo
            self.vy *= -1             # Invierte el sentido del vector vertical
       elif self.y >= ALTO - self.alto:
            self.y = ALTO - self.alto # Evita que la criatura caiga al vacío por el suelo
            self.vy *= -1             # Invierte el sentido del vector vertical
    #=========================================================
    # SECCION D: PROCESAMIENTO DEL MORDISCO
    #=========================================================
       if self.estado == "buscando_comida" and self.comida_objetivo:
       # Generamos hitboxes rectangulares para evaluar superposicion
            rect_brain = pygame.Rect(self.x, self.y, self.ancho, self.alto)
            rect_comida = pygame.Rect(self.comida_objetivo.x, self.comida_objetivo.y, self.comida_objetivo.ancho, self.comida_objetivo.alto)
            
            if rect_brain.colliderect(rect_comida):
            # Si los rectángulos colisionan...
                lista_comidas.remove(self.comida_objetivo) # Remueve el objeto de la lista global
                self.comida_objetivo = None                # Vuelve a liberar el puntero de memoria
                self.estado = "paseando"                   # Cambia la conducta a descanso
                self.hambre = 100                          # Sacia el parámetro biológico al límite 
    
    def vivir(self, lista_monedas):
    # Suma edad y drena el hambre de la criatura en cada fotograma. 
    # Si el hambre llega a cero, castiga la salud simulando inanición.
        self.hambre -= 0.015
        # Restamos hambre en cada frame
        self.edad += 0.01
        # Incrementamos el contador de edad
        
        if self.hambre <= 0: 
            self.hambre = 0      # Evita que el hambre tenga valores negativos
            self.salud -= 0.05    # Drena la vida por falta de nutrientes 
            
        if self.salud <= 0:
            self.salud = 0       # Evita que el hambre tenga valores
            self.vivo = False
        
        if self.salud >= 95 and self.hambre >= 50:
            self.reloj_moneda += 1
            
            if self.reloj_moneda >= 300:
                self.spawnear_monedas(lista_monedas)
                
                self.reloj_moneda = 0
        
        else:
            self.reloj_moneda = 0
    
    def spawnear_monedas(self, lista_monedas):
        # Probabilidades: 70% bronce, 25% plata, 5% oro
        rand = random.random()
        if rand < 0.70:
            tipo = "bronce"
        elif rand < 0.95:
            tipo = "plata"
        else:
            tipo = "oro"
        lista_monedas.append(Moneda(
            int(self.x) + self.ancho // 2 - ANCHO_MONEDA // 2,
            int(self.y) + self.alto,
            tipo,
        ))
    
    def dibujar(self, superficie): 
    # Dibuja el cuerpo de la criatura en la pantalla del juego.
         pygame.draw.rect(superficie, self.color, (int(self.x), int(self.y), self.ancho, self.alto))
         # Convertimos self.x y self.y a enteros (int) porque las pantallas no pueden pintar "medios píxeles"

class BrainrotA(Brainrot):
    # Brainrot 67 — come comida tipo A.
    def __init__(self, x, y):
        super().__init__(x, y)
        datos = TIPOS_BRAINROT["A"]
        self.color = datos["color"]
        self.nombre = datos["nombre"]
        self.tipo_dieta = "A"
    
    def buscar_comida_cercana(self, lista_comidas):
        comidas_que_me_gustan = [c for c in lista_comidas if c.tipo == self.tipo_dieta]

        super().buscar_comida_cercana(comidas_que_me_gustan)

class BrainrotB(Brainrot):
    # Brainrot tt — come comida tipo B.
    def __init__(self, x, y):
        super().__init__(x, y)
        datos = TIPOS_BRAINROT["B"]
        self.color = datos["color"]
        self.nombre = datos["nombre"]
        self.tipo_dieta = "B"
    
    def buscar_comida_cercana(self, lista_comidas):
        comidas_que_me_gustan = [c for c in lista_comidas if c.tipo == self.tipo_dieta]

        super().buscar_comida_cercana(comidas_que_me_gustan)


class BrainrotC(Brainrot):
    # Brainrot bc — come comida tipo C.
    def __init__(self, x, y):
        super().__init__(x, y)
        datos = TIPOS_BRAINROT["C"]
        self.color = datos["color"]
        self.nombre = datos["nombre"]
        self.tipo_dieta = "C"
    
    def buscar_comida_cercana(self, lista_comidas):
        comidas_que_me_gustan = [c for c in lista_comidas if c.tipo == self.tipo_dieta]

        super().buscar_comida_cercana(comidas_que_me_gustan)
