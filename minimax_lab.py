import os
import time
import random

# --- CONFIGURACIÓN GLOBAL ---
# Representación del mapa: 1=Pared, 0=Vacío, 2=Queso, 3=Salida
MAPA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1],
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class JuegoSimulacion:
    def __init__(self, dificultad, rol_usuario):
        """Inicializa los parámetros del juego, posiciones y niveles de dificultad."""
        self.mapa = [fila[:] for fila in MAPA] # Copia profunda del mapa
        self.alto = len(self.mapa)
        self.ancho = len(self.mapa[0])
        self.gato = [1, 1]        # Posición inicial Gato
        self.raton = [13, 7]      # Posición inicial Ratón
        self.tiene_queso = False
        self.salida = (1, 3)
        self.movimientos_restantes = 80
        self.tiempo_actualizacion = 0.3
        self.rol_usuario = rol_usuario
        
        # Ajuste de dificultad: afecta la probabilidad de error y la profundidad de búsqueda de la IA
        if dificultad == "1":
            self.prob_error_gato = 0.70 # El gato falla mucho
            self.nombre_dif = "FÁCIL"
            self.profundidad = 3
        elif dificultad == "2":
            self.prob_error_gato = 0.40
            self.nombre_dif = "MEDIO"
            self.profundidad = 5
        else:
            self.prob_error_gato = 0.10 # El gato es casi perfecto
            self.nombre_dif = "DIFÍCIL"
            self.profundidad = 7

    def obtener_quesos(self):
        """Escanea el mapa para encontrar las coordenadas de los quesos."""
        return [(x, y) for y in range(self.alto) for x in range(self.ancho) if self.mapa[y][x] == 2]

    def dibujar(self, mensaje=""):
        """Limpia la pantalla y renderiza el mapa con emojis."""
        os.system('cls' if os.name == 'nt' else 'clear')
        personaje = "🐭 TÚ" if self.rol_usuario == "1" else ("🐱 TÚ" if self.rol_usuario == "2" else "🤖 IA vs IA")
        
        print(f"=== JUGANDO COMO: {personaje} | DIFICULTAD: {self.nombre_dif} ===")
        print(f"⏳ Movs: {self.movimientos_restantes} | Queso: {'✅' if self.tiene_queso else '❌'}")
        print(f"INFO: {mensaje}")
        print("-" * 45)
        
        for y in range(self.alto):
            linea = ""
            for x in range(self.ancho):
                if [x, y] == self.gato: linea += "🐱"
                elif [x, y] == self.raton: linea += "🐭"
                elif self.mapa[y][x] == 1: linea += "🧱"
                elif self.mapa[y][x] == 2: linea += "🧀"
                elif self.mapa[y][x] == 3: linea += "🚪"
                else: linea += "  "
            print(linea)

    def mov_validos(self, pos):
        """Devuelve una lista de coordenadas adyacentes que no son paredes."""
        x, y = pos
        res = []
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.ancho and 0 <= ny < self.alto and self.mapa[ny][nx] != 1:
                res.append((nx, ny))
        return res

    def mover_humano(self, pos_actual):
        """Gestiona la entrada de teclado para el jugador humano."""
        print("\n(W: Arriba, S: Abajo, A: Izquierda, D: Derecha)")
        mov = input("Tu movimiento: ").lower()
        mapping = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}
        
        if mov in mapping:
            dx, dy = mapping[mov]
            nueva_pos = (pos_actual[0] + dx, pos_actual[1] + dy)
            if nueva_pos in self.mov_validos(tuple(pos_actual)):
                return list(nueva_pos)
        print("¡Movimiento inválido o contra la pared!")
        return pos_actual

    # --- LÓGICA DE IA (MINIMAX) ---
    def evaluar(self, g_pos, r_pos):
        """Función heurística: calcula qué tan buena es una posición para el gato."""
        # Distancia Manhattan entre gato y ratón
        dist_g_r = abs(g_pos[0]-r_pos[0]) + abs(g_pos[1]-r_pos[1])
        # Distancia Manhattan entre ratón y salida
        dist_r_s = abs(r_pos[0]-self.salida[0]) + abs(r_pos[1]-self.salida[1])
        # El gato quiere distancia mínima a ratón y que el ratón esté lejos de la salida
        return -dist_g_r + (dist_r_s * 1.2)

    def minimax(self, g_pos, r_pos, prof, alfa, beta, es_max):
        """Algoritmo de decisión para predecir movimientos futuros."""
        if prof == 0 or g_pos == r_pos:
            return self.evaluar(g_pos, r_pos)
            
        if es_max: # Turno del Gato (maximizar ventaja)
            val = -float('inf')
            for m in self.mov_validos(g_pos):
                val = max(val, self.minimax(m, r_pos, prof-1, alfa, beta, False))
                alfa = max(alfa, val); 
                if beta <= alfa: break # Poda Alfa-Beta
            return val
        else: # Turno del Ratón (minimizar ventaja del gato)
            val = float('inf')
            for m in self.mov_validos(r_pos):
                val = min(val, self.minimax(g_pos, m, prof-1, alfa, beta, True))
                beta = min(beta, val); 
                if beta <= alfa: break # Poda Alfa-Beta
            return val

    def mover_raton(self):
        """Controla el movimiento del ratón (Humano o IA básica/Minimax)."""
        if self.rol_usuario == "1":
            self.raton = self.mover_humano(self.raton)
        else:
            movs = self.mov_validos(tuple(self.raton))
            if not self.tiene_queso:
                # Si no tiene queso, va al queso más cercano (Greedy)
                obj = self.obtener_quesos()[0]
                self.raton = list(min(movs, key=lambda m: abs(m[0]-obj[0]) + abs(m[1]-obj[1])))
            else:
                # Si tiene queso, usa Minimax para escapar del gato hacia la salida
                mejor_mov = min(movs, key=lambda m: self.minimax(tuple(self.gato), m, 4, -float('inf'), float('inf'), True))
                self.raton = list(mejor_mov)

        # Verificar si recogió el queso
        if self.mapa[self.raton[1]][self.raton[0]] == 2:
            self.mapa[self.raton[1]][self.raton[0]] = 0
            self.tiene_queso = True

    def mover_gato(self):
        """Controla el movimiento del gato (Humano o IA Minimax)."""
        if not self.tiene_queso: 
            return "El gato espera a que agarres el queso..."
        
        if self.rol_usuario == "2":
            self.gato = self.mover_humano(self.gato)
            return "¡Te toca mover, Gato!"
        else:
            movs = self.mov_validos(tuple(self.gato))
            # Simular errores según dificultad
            if random.random() < self.prob_error_gato:
                self.gato = list(random.choice(movs))
                return "¡El gato se distrajo!"
            else:
                # IA Profesional usando Minimax
                mejor_mov = max(movs, key=lambda m: self.minimax(m, tuple(self.raton), self.profundidad, -float('inf'), float('inf'), False))
                self.gato = list(mejor_mov)
                return "El gato te está cazando..."

    def ejecutar(self):
        """Bucle principal del juego."""
        msg = "El ratón debe buscar el queso 🧀"
        while self.movimientos_restantes > 0:
            self.dibujar(msg)
            
            # --- Turno Ratón ---
            self.mover_raton()
            self.movimientos_restantes -= 1
            
            if self.gato == self.raton:
                self.dibujar("¡ATRAPADO!"); print("\n💀 FINAL: El Gato ganó."); return
            if self.tiene_queso and tuple(self.raton) == self.salida:
                self.dibujar("¡ESCAPE EXITOSO!"); print("\n🎉 FINAL: El Ratón ganó."); return
            
            # --- Turno Gato ---
            self.dibujar("Moviendo gato...")
            if self.rol_usuario == "3": time.sleep(self.tiempo_actualizacion)
            
            msg = self.mover_gato()
            if self.gato == self.raton:
                self.dibujar("¡ATRAPADO!"); print("\n💀 FINAL: El Gato ganó."); return

        print("\n⌛ ¡TIEMPO AGOTADO! Nadie ganó.")

# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    print("--- BIENVENIDO AL JUEGO DEL GATO Y EL RATÓN ---")
    print("Selecciona tu rol:")
    print("1. Ser el RATÓN (🐭)")
    print("2. Ser el GATO (🐱)")
    print("3. Ver simulación (IA vs IA)")
    rol = input("Opción: ")
    
    print("\nSelecciona Dificultad de la IA:")
    print("1. Fácil | 2. Medio | 3. Difícil")
    dif = input("Opción: ")
    
    # Validación básica de entradas
    juego = JuegoSimulacion(dif if dif in ["1","2","3"] else "2", rol if rol in ["1","2","3"] else "3")
    juego.ejecutar()