import os
import time
import random

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
        self.mapa = [fila[:] for fila in MAPA]
        self.alto = len(self.mapa)
        self.ancho = len(self.mapa[0])
        self.gato = [1, 1]
        self.raton = [13, 7]
        self.tiene_queso = False
        self.salida = (1, 3)
        self.movimientos_restantes = 80
        self.tiempo_actualizacion = 0.3
        self.rol_usuario = rol_usuario
        
        
        if dificultad == "1":
            self.prob_error_gato = 0.70
            self.nombre_dif = "FÁCIL"
            self.profundidad = 3
        elif dificultad == "2":
            self.prob_error_gato = 0.40
            self.nombre_dif = "MEDIO"
            self.profundidad = 5
        else:
            self.prob_error_gato = 0.10
            self.nombre_dif = "DIFÍCIL"
            self.profundidad = 7

    def obtener_quesos(self):
        return [(x, y) for y in range(self.alto) for x in range(self.ancho) if self.mapa[y][x] == 2]

    def dibujar(self, mensaje=""):
        os.system('cls' if os.name == 'nt' else 'clear')
        personaje = "🐭 TÚ" if self.rol_usuario == 1 else ("🐱 TÚ" if self.rol_usuario == "2" else "🤖 IA vs IA")
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
        x, y = pos
        res = []
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.ancho and 0 <= ny < self.alto and self.mapa[ny][nx] != 1:
                res.append((nx, ny))
        return res

    def mover_humano(self, pos_actual):
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
        dist_g_r = abs(g_pos[0]-r_pos[0]) + abs(g_pos[1]-r_pos[1])
        dist_r_s = abs(r_pos[0]-self.salida[0]) + abs(r_pos[1]-self.salida[1])
        return -dist_g_r + (dist_r_s * 1.2)

    def minimax(self, g_pos, r_pos, prof, alfa, beta, es_max):
        if prof == 0 or g_pos == r_pos:
            return self.evaluar(g_pos, r_pos)
        if es_max:
            val = -float('inf')
            for m in self.mov_validos(g_pos):
                val = max(val, self.minimax(m, r_pos, prof-1, alfa, beta, False))
                alfa = max(alfa, val); 
                if beta <= alfa: break
            return val
        else:
            val = float('inf')
            for m in self.mov_validos(r_pos):
                val = min(val, self.minimax(g_pos, m, prof-1, alfa, beta, True))
                beta = min(beta, val); 
                if beta <= alfa: break
            return val

    def mover_raton(self):
        if self.rol_usuario == "1":
            self.raton = self.mover_humano(self.raton)
        else:
            movs = self.mov_validos(tuple(self.raton))
            if not self.tiene_queso:
                obj = self.obtener_quesos()[0]
                self.raton = list(min(movs, key=lambda m: abs(m[0]-obj[0]) + abs(m[1]-obj[1])))
            else:
                mejor_mov = min(movs, key=lambda m: self.minimax(tuple(self.gato), m, 4, -float('inf'), float('inf'), True))
                self.raton = list(mejor_mov)

        if self.mapa[self.raton[1]][self.raton[0]] == 2:
            self.mapa[self.raton[1]][self.raton[0]] = 0
            self.tiene_queso = True

    def mover_gato(self):
        if not self.tiene_queso: return "El gato espera a que agarres el queso..."
        
        if self.rol_usuario == "2":
            self.gato = self.mover_humano(self.gato)
            return "¡Te toca mover, Gato!"
        else:
            movs = self.mov_validos(tuple(self.gato))
            if random.random() < self.prob_error_gato:
                self.gato = list(random.choice(movs))
                return "¡El gato se distrajo!"
            else:
                mejor_mov = max(movs, key=lambda m: self.minimax(m, tuple(self.raton), self.profundidad, -float('inf'), float('inf'), False))
                self.gato = list(mejor_mov)
                return "El gato te está cazando..."

    def ejecutar(self):
        msg = "El ratón debe buscar el queso 🧀"
        while self.movimientos_restantes > 0:
            self.dibujar(msg)
            
            # Turno Ratón
            self.mover_raton()
            self.movimientos_restantes -= 1
            if self.gato == self.raton:
                self.dibujar("¡ATRAPADO!"); print("\n💀 FINAL: El Gato ganó."); return
            if self.tiene_queso and tuple(self.raton) == self.salida:
                self.dibujar("¡ESCAPE EXITOSO!"); print("\n🎉 FINAL: El Ratón ganó."); return
            
            # Turno Gato
            self.dibujar("Moviendo gato...")
            if self.rol_usuario == "3": time.sleep(self.tiempo_actualizacion)
            
            msg = self.mover_gato()
            if self.gato == self.raton:
                self.dibujar("¡ATRAPADO!"); print("\n💀 FINAL: El Gato ganó."); return

        print("\n⌛ ¡TIEMPO AGOTADO! Nadie ganó.")

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
    
    juego = JuegoSimulacion(dif if dif in ["1","2","3"] else "2", rol if rol in ["1","2","3"] else "3")
    juego.ejecutar()