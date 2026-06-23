import os
import sys
import pygame
from src.constantes import ANCHO, ALTO, FPS, BLANCO, ROJO
from src.fondo import dibujar_fondo_cielo_completo, precargar_fondo_pantalla_completa
from src.guardado import RUTA_PARTIDA, cargar_partida
from src.fuentes import obtener_fuente_menu, TAMANO_MENU_TITULO, TAMANO_MENU_OPCION, TAMANO_MENU_ALERTA
from src.audio import detener_musica_fondo

COLOR_OPCION = BLANCO
COLOR_OPCION_ACTIVA = (255, 215, 0)
COLOR_OPCION_DESHABILITADA = (80, 80, 90)
COLOR_ALERTA = ROJO

OPCIONES = (
    "NUEVA PARTIDA",
    "CARGAR PARTIDA",
    "SALIR DEL JUEGO",
)

class MenuInicio:
    """
    Controlador interactivo del Menú de Inicio.
    """
    def __init__(self, ventana):
        self.ventana = ventana
        self.opcion_seleccionada = 0
        self.accion = None
        self.frames_alerta = 0
        self.mostrar_alerta_sin_partida = False

        precargar_fondo_pantalla_completa()

        self.fuente_titulo = obtener_fuente_menu(TAMANO_MENU_TITULO)
        self.fuente_opciones = obtener_fuente_menu(TAMANO_MENU_OPCION)
        self.fuente_alerta = obtener_fuente_menu(TAMANO_MENU_ALERTA)

    def _hay_partida_guardada(self):
        """Verifica la existencia del archivo JSON de guardado."""
        return os.path.exists(RUTA_PARTIDA)

    def _mover_seleccion(self, paso):
        """Permite navegar por las opciones con las teclas de dirección."""
        while True:
            self.opcion_seleccionada = (self.opcion_seleccionada + paso) % len(OPCIONES)
            if self.opcion_seleccionada != 1 or self._hay_partida_guardada():
                break

    def _activar_opcion(self):
        """Ejecuta la función seleccionada por el usuario."""
        if self.opcion_seleccionada == 0:
            if os.path.exists(RUTA_PARTIDA):
                os.remove(RUTA_PARTIDA)
            self.accion = "nueva"
            return True

        if self.opcion_seleccionada == 1:
            if not self._hay_partida_guardada():
                self.mostrar_alerta_sin_partida = True
                self.frames_alerta = 180
                return False
            self.accion = "cargar"
            return True

        self.accion = "salir"
        return True

    def _procesar_eventos(self):
        """Escucha eventos del teclado en la pantalla de inicio."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.accion = "salir"
                return True

            if evento.type != pygame.KEYDOWN:
                continue

            if evento.key in (pygame.K_UP, pygame.K_w):
                self._mover_seleccion(-1)
            elif evento.key in (pygame.K_DOWN, pygame.K_s):
                self._mover_seleccion(1)
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self._activar_opcion():
                    return True

        return False

    def _dibujar_texto_centrado(self, fuente, texto, y, color):
        # Dibuja una línea de texto centrada horizontalmente.
        imagen = fuente.render(texto, True, color)
        x = (ANCHO - imagen.get_width()) // 2
        self.ventana.blit(imagen, (x, y))
        return imagen.get_height()

    def _dibujar_opcion_centrada(self, texto, y, activa, deshabilitada):
        # Dibuja una opción centrada; el asterisco va a la izquierda sin mover el texto.
        if deshabilitada:
            color = COLOR_OPCION_DESHABILITADA
        elif activa:
            color = COLOR_OPCION_ACTIVA
        else:
            color = COLOR_OPCION

        imagen_texto = self.fuente_opciones.render(texto, True, color)
        x_texto = (ANCHO - imagen_texto.get_width()) // 2
        self.ventana.blit(imagen_texto, (x_texto, y))

        if activa:
            imagen_asterisco = self.fuente_opciones.render("*", True, color)
            self.ventana.blit(
                imagen_asterisco,
                (x_texto - imagen_asterisco.get_width() - 10, y),
            )

        return imagen_texto.get_height()

    def _dibujar(self):
        """Renderiza la gráfica general del Menú (cielo, logo, textos)."""
        dibujar_fondo_cielo_completo(self.ventana)

        separacion_titulo_opciones = self.fuente_titulo.get_height() + 36
        separacion_opciones = self.fuente_opciones.get_height() + 24
        altura_linea_opcion = self.fuente_opciones.get_height()
        altura_titulo = self.fuente_titulo.get_height()
        bloque_alto = (
            altura_titulo
            + separacion_titulo_opciones
            + (len(OPCIONES) - 1) * separacion_opciones
            + altura_linea_opcion
        )
        y_titulo = (ALTO - bloque_alto) // 2
        y_opciones = y_titulo + altura_titulo + separacion_titulo_opciones

        self._dibujar_texto_centrado(
            self.fuente_titulo, "VILLA BRAINROT", y_titulo, COLOR_OPCION_ACTIVA,
        )

        for indice, texto in enumerate(OPCIONES):
            activa = indice == self.opcion_seleccionada
            deshabilitada = indice == 1 and not self._hay_partida_guardada()
            self._dibujar_opcion_centrada(
                texto,
                y_opciones + indice * separacion_opciones,
                activa,
                deshabilitada,
            )

        if self.mostrar_alerta_sin_partida and self.frames_alerta > 0:
            alerta = self.fuente_alerta.render("No hay partida guardada", True, COLOR_ALERTA)
            self.ventana.blit(alerta, ((ANCHO - alerta.get_width()) // 2, ALTO - 80))
            self.frames_alerta -= 1

    def ejecutar(self):
        """Bucle continuo del menú hasta seleccionar acción."""
        reloj = pygame.time.Clock()
        corriendo = True

        while corriendo:
            reloj.tick(FPS)
            if self._procesar_eventos():
                corriendo = False
            self._dibujar()
            pygame.display.flip()

        if self.accion == "salir":
            detener_musica_fondo()
            pygame.quit()
            sys.exit()

        return self.accion

    def obtener_datos_cargados(self):
        """Carga y devuelve los datos del JSON si seleccionó Cargar."""
        if self.accion == "cargar":
            return cargar_partida()
        return None
