import os
import pygame
import random
from src.constantes import ANCHO, ALTO, LINEA_HORIZONTE, BLANCO, TIPOS_BRAINROT
from src.moneda import Moneda, ANCHO_MONEDA

RUTAS_SPRITES = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites"),
    os.path.join(os.path.dirname(__file__), "assets"),
]

ALTO_BRAINROT = 75
ANCHO_BRAINROT = 75
_cache_sprites = {}

def _tamano_caja(factor=1.0):
    return max(1, int(ANCHO_BRAINROT * factor)), max(1, int(ALTO_BRAINROT * factor))

TAMANO_MAX_BRAINROT = max(
    _tamano_caja(datos.get("escala", 1.0))[0] for datos in TIPOS_BRAINROT.values()
)

class Brainrot:
    # Representa las entidades de la villa (brainrots).

    def __init__(self, x, y):
        self.ancho = ANCHO_BRAINROT
        self.alto = ALTO_BRAINROT
        self.color = BLANCO
        self.nombre = ""
        self.tipo_dieta = ""

        self.x = x
        self.y = y

        self.vx = 4
        self.vy = 2

        self.hambre = 100
        self.salud = 100
        self.edad = 0

        self.comida_objetivo = None
        self.estado = "paseando"

        self.reloj_moneda = 0
        self.vivo = True

        self.image_derecha = None
        self.image_izquierda = None
        self.image = None

    @classmethod
    def _resolver_ruta_sprite(cls, nombre_archivo):
        for carpeta in RUTAS_SPRITES:
            ruta = os.path.join(carpeta, nombre_archivo)
            if os.path.exists(ruta):
                return ruta
        raise FileNotFoundError(
            f"No se encontró '{nombre_archivo}' en: {', '.join(RUTAS_SPRITES)}"
        )

    @classmethod
    def _escalar_sprite_a_caja(cls, imagen, factor=1.0):
        # Escala el sprite para que quepa en una caja fija y quede centrado.
        ancho_caja, alto_caja = _tamano_caja(factor)
        ancho_origen, alto_origen = imagen.get_size()
        escala = min(ancho_caja / ancho_origen, alto_caja / alto_origen)
        ancho_escalado = max(1, int(ancho_origen * escala))
        alto_escalado = max(1, int(alto_origen * escala))
        escalada = pygame.transform.scale(imagen, (ancho_escalado, alto_escalado))

        superficie = pygame.Surface((ancho_caja, alto_caja), pygame.SRCALPHA)
        offset_x = (ancho_caja - ancho_escalado) // 2
        offset_y = (alto_caja - alto_escalado) // 2
        superficie.blit(escalada, (offset_x, offset_y))
        return superficie

    @classmethod
    def _obtener_par_sprites(cls, nombre_archivo, factor=1.0):
        clave = (nombre_archivo, factor)
        if clave not in _cache_sprites:
            ruta = cls._resolver_ruta_sprite(nombre_archivo)
            original = pygame.image.load(ruta).convert_alpha()
            derecha = cls._escalar_sprite_a_caja(original, factor)
            izquierda = pygame.transform.flip(derecha, True, False)
            _cache_sprites[clave] = (derecha, izquierda)
        return _cache_sprites[clave]

    @classmethod
    def precargar(cls):
        # Precarga todos los sprites de brainrot tras crear la ventana.
        for datos in TIPOS_BRAINROT.values():
            cls._obtener_par_sprites(datos["sprite"], datos.get("escala", 1.0))

    def _cargar_sprites(self, tipo):
        # Asigna las variantes derecha/izquierda según el tipo de criatura.
        datos = TIPOS_BRAINROT[tipo]
        factor = datos.get("escala", 1.0)
        self.image_derecha, self.image_izquierda = Brainrot._obtener_par_sprites(
            datos["sprite"], factor,
        )
        self.image = self.image_derecha
        self.ancho, self.alto = _tamano_caja(factor)

    def actualizar(self):
        # Orienta el sprite según la velocidad horizontal actual.
        if self.vx > 0:
            self.image = self.image_derecha
        elif self.vx < 0:
            self.image = self.image_izquierda

    def buscar_comida_cercana(self, lista_comidas):
        comidas_listas = [c for c in lista_comidas if c.y >= c.y_destino]

        if not comidas_listas:
            self.estado = "paseando"
            self.comida_objetivo = None
            return

        comida_mas_cercana = None
        distancia_minima = float("inf")

        for comida in comidas_listas:
            dx = comida.x - self.x
            dy = comida.y - self.y
            distancia = (dx ** 2 + dy ** 2) ** 0.5

            if distancia < distancia_minima:
                distancia_minima = distancia
                comida_mas_cercana = comida

        if comida_mas_cercana:
            self.comida_objetivo = comida_mas_cercana
            self.estado = "buscando_comida"

    def mover(self, lista_comidas):
        if self.estado == "paseando":
            self.vx += random.uniform(-0.5, 0.5)
            self.vy += random.uniform(-1, 1)

            if self.vx > 5:
                self.vx = 5
            if self.vx < -5:
                self.vx = -5
            if self.vy > 3:
                self.vy = 3
            if self.vy < -3:
                self.vy = -3

        elif self.estado == "buscando_comida" and self.comida_objetivo:
            if self.comida_objetivo not in lista_comidas:
                self.estado = "paseando"
                self.comida_objetivo = None
            else:
                distancia_x = self.comida_objetivo.x - self.x
                distancia_y = self.comida_objetivo.y - self.y

                if abs(distancia_x) < 4:
                    self.x = self.comida_objetivo.x
                    self.vx = 0
                else:
                    self.vx = 4 if distancia_x > 0 else -4

                if abs(distancia_y) < 4:
                    self.y = self.comida_objetivo.y
                    self.vy = 0
                else:
                    self.vy = 4 if distancia_y > 0 else -4

        self.x += self.vx
        self.y += self.vy

        if self.x <= 0:
            self.x = 0
            self.vx *= -1
        elif self.x >= ANCHO - self.ancho:
            self.x = ANCHO - self.ancho
            self.vx *= -1

        if self.y <= LINEA_HORIZONTE:
            self.y = LINEA_HORIZONTE
            self.vy *= -1
        elif self.y >= ALTO - self.alto:
            self.y = ALTO - self.alto
            self.vy *= -1

        if self.estado == "buscando_comida" and self.comida_objetivo:
            rect_brain = pygame.Rect(self.x, self.y, self.ancho, self.alto)
            rect_comida = pygame.Rect(
                self.comida_objetivo.x, self.comida_objetivo.y,
                self.comida_objetivo.ancho, self.comida_objetivo.alto,
            )

            if rect_brain.colliderect(rect_comida):
                lista_comidas.remove(self.comida_objetivo)
                self.comida_objetivo = None
                self.estado = "paseando"
                self.hambre = 100

        self.actualizar()

    def vivir(self, lista_monedas):
        self.hambre -= 0.015
        self.edad += 0.01

        if self.hambre <= 0:
            self.hambre = 0
            self.salud -= 0.05

        if self.salud <= 0:
            self.salud = 0
            self.vivo = False

        if self.salud >= 95 and self.hambre >= 50:
            self.reloj_moneda += 1
            if self.reloj_moneda >= 300:
                self.spawnear_monedas(lista_monedas)
                self.reloj_moneda = 0
        else:
            self.reloj_moneda = 0

    def spawnear_monedas(self, lista_monedas):
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
        if self.image is not None:
            superficie.blit(self.image, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(
                superficie, self.color, (int(self.x), int(self.y), self.ancho, self.alto),
            )


class BrainrotA(Brainrot):
    def __init__(self, x, y):
        super().__init__(x, y)
        datos = TIPOS_BRAINROT["A"]
        self.color = datos["color"]
        self.nombre = datos["nombre"]
        self.tipo_dieta = "A"
        self._cargar_sprites("A")

    def buscar_comida_cercana(self, lista_comidas):
        comidas_que_me_gustan = [c for c in lista_comidas if c.tipo == self.tipo_dieta]
        super().buscar_comida_cercana(comidas_que_me_gustan)


class BrainrotB(Brainrot):
    def __init__(self, x, y):
        super().__init__(x, y)
        datos = TIPOS_BRAINROT["B"]
        self.color = datos["color"]
        self.nombre = datos["nombre"]
        self.tipo_dieta = "B"
        self._cargar_sprites("B")

    def buscar_comida_cercana(self, lista_comidas):
        comidas_que_me_gustan = [c for c in lista_comidas if c.tipo == self.tipo_dieta]
        super().buscar_comida_cercana(comidas_que_me_gustan)


class BrainrotC(Brainrot):
    def __init__(self, x, y):
        super().__init__(x, y)
        datos = TIPOS_BRAINROT["C"]
        self.color = datos["color"]
        self.nombre = datos["nombre"]
        self.tipo_dieta = "C"
        self._cargar_sprites("C")

    def buscar_comida_cercana(self, lista_comidas):
        comidas_que_me_gustan = [c for c in lista_comidas if c.tipo == self.tipo_dieta]
        super().buscar_comida_cercana(comidas_que_me_gustan)
