# Villa Brainrot 🎮

Un divertido juego casual de simulación desarrollado en **Python** y **Pygame** donde gestionas criaturas, recolectas monedas y administras una tienda para mantener tu villa con vida.

---

## Características principales

- **Sistema de tienda por pestañas** — Compra comida o nuevos Brainrots desde un panel superior con pestañas *Comida* y *Brainrots*, cada una con tres tipos disponibles (67, tt, bc).
- **IA de criaturas** — Cada Brainrot recorre el prado buscando la comida más cercana de forma autónoma. Si su hambre llega a 0, su salud baja hasta morir.
- **Recolección de monedas** — Las criaturas generan monedas al estar bien alimentados.
- **Guardado automático en JSON** — El estado completo de la partida (dinero, stock, criaturas vivas con su salud) se guarda automáticamente en `datos/partida.json` al cerrar el juego y se restaura al cargar partida desde el menu principal
- **Game Over recuperable** — Si te quedas sin criaturas vivas y sin dinero para comprar una nueva, aparece la pantalla de Game Over. Un clic reinicia la partida desde cero.
- **Arquitectura modular** — Cada responsabilidad está aislada en su propio módulo dentro de `src/`, lo que hace el código fácil de leer, extender y mantener.

---

## Estructura del proyecto

```
mi_juego/
├── main.py                  # Punto de entrada: lanza ejecutar_juego()
├── requirements.txt         # Dependencias del proyecto
├── datos/
│   └── partida.json         # Guardado automático de la partida (se crea al jugar)
├── assets/
│   ├── sprites/             # Imágenes de criaturas, comida, monedas, cielo y pasto
│   └── sounds/              # Efectos de sonido y música de fondo
└── src/
    ├── constantes.py        # Dimensiones de pantalla, colores, FPS y catálogo de Brainrots
    ├── juego.py             # Controlador principal: bucle de eventos, actualización y dibujo
    ├── fondo.py             # Escenario: carga y dibuja cielo, prado y valla
    ├── interfaz.py          # HUD, tienda (clase Tienda con procesar_click) y pantallas
    ├── brainrot.py          # Clase base Brainrot y subclases BrainrotA, B y C con su IA
    ├── comida.py            # Clase Comida: sprite de galleta que cae al hacer clic
    ├── moneda.py            # Clase Moneda: animación y recolección por clic
    ├── guardado.py          # Serialización y deserialización de la partida en JSON
    ├── menu.py              # Menú de inicio con opciones Nueva Partida y Continuar
    ├── audio.py             # Música de fondo y efectos de sonido (mixer de Pygame)
    └── fuentes.py           # Gestión centralizada de tipografías y tamaños de texto
```

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/gsaaz/mi_juego.git
cd mi_juego
```

### 2. (Opcional) Crear un entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el juego

```bash
python main.py
```

> **Requisito mínimo:** Python 3.10 o superior.

---

## Cómo jugar

| Acción | Cómo hacerlo |
|---|---|
| **Lanzar comida** | Selecciona un tipo (A / B / C) en el panel de inventario y haz clic en el prado |
| **Comprar comida** | Pestaña *Comida* → botón de compra (cuesta $10 por unidad) |
| **Comprar un Brainrot** | Pestaña *Brainrots* → botón de compra (cuesta $50) |
| **Recolectar monedas** | Haz clic sobre las monedas que aparecen en el prado |
| **Cerrar el juego** | La partida se guarda automáticamente al cerrar la ventana |

### Condición de derrota

Si **no tienes criaturas vivas** y tu saldo es **menor a $50** (sin poder comprar una nueva), el juego muestra la pantalla de **Game Over**. Haz clic en cualquier lugar para reiniciar.

---

## Tecnologías utilizadas

- **Python 3.10+**
- **Pygame 2.5+**

---

## Licencia

Proyecto académico de desarrollo. Sin licencia de distribución comercial.
