# 🐱 vs 🐭: Simulador de Gato y Ratón con IA
### Un juego de estrategia por consola donde un Ratón intenta conseguir queso y escapar, mientras un Gato intenta cazarlo. El proyecto implementa algoritmos de Inteligencia Artificial clásica para la toma de decisiones.

## 📋 Tabla de Contenidos
1. Descripción

2. Características

3. Instalación y Ejecución

4. Cómo Jugar

5. Cómo Funciona (La Lógica)

6. Personalización

## 📖 Descripción
### Este proyecto es una simulación en Python que utiliza el algoritmo Minimax para controlar a los personajes en un entorno de cuadrícula. El objetivo es demostrar cómo una IA puede planificar movimientos futuros para maximizar su victoria (o minimizar su derrota).

### El juego se ejecuta directamente en la terminal y ofrece una visualización paso a paso de la partida.

## ✨ Características
### 3 Modos de Juego:

    · Jugar como Ratón (vs IA).

    · Jugar como Gato (vs IA).

    · Modo Espectador (IA vs IA).

· Niveles de Dificultad: Ajusta la "inteligencia" del oponente (Fácil, Medio, Difícil).

· Gráficos ASCII: Visualización clara usando emojis en la consola.

· Sin dependencias externas: Funciona con las librerías estándar de Python.

## 🚀 Instalación y Ejecución
### Requisitos previos

· Tener instalado Python 3.x.

### Pasos
1. Clona este repositorio o descarga el archivo minimax_lab.py.

2. Abre tu terminal o línea de comandos.

3. Navega hasta la carpeta donde guardaste el archivo.

4. Ejecuta el siguiente comando:

### Bash
### python minimax_lab.py

## 🎮 Cómo Jugar
### Una vez iniciado el juego, sigue las instrucciones en pantalla:

1. Selecciona tu Rol: Elige si quieres ser la presa, el cazador o solo mirar.

2. Elige la Dificultad: Esto determina qué tan lejos "piensa" la IA en el futuro.

3. Controles (si juegas como humano):

· W: Arriba

· S: Abajo

· A: Izquierda

· D: Derecha

### Objetivo del Ratón: Agarrar el queso (🧀) y llegar a la salida (🚪).
### Objetivo del Gato: Atrapar al ratón antes de que escape.

## 🧠 Cómo Funciona (La Lógica)
Este juego no usa "if/else" simples para moverse, sino algoritmos de Ciencias de la Computación:

### 1. Algoritmo Minimax

Es el cerebro de la IA. Permite al Gato y al Ratón "imaginar" el futuro.

· La IA simula todos los movimientos posibles (y los movimientos de su oponente) varios turnos adelante.

· Elige el camino que le garantiza el mejor resultado, asumiendo que el oponente también jugará de forma óptima.

· Profundidad: En modo "Difícil", la IA mira hasta 7 jugadas en el futuro.

### 2. Distancia Manhattan
### Es la forma en que la IA mide qué tan "buena" es una posición.

· Calcula cuántos pasos reales (sin diagonales) faltan para llegar al objetivo.

· Fórmula: |x1 - x2| + |y1 - y2|

## ⚙️ Personalización
### Puedes modificar el código fuente para cambiar el mapa:

### Busca la variable MAPA al inicio del archivo:

· 0: Camino libre

· 1: Pared (🧱)

· 2: Queso (🧀)

· 3: Salida (🚪)

### ¡FIN!
