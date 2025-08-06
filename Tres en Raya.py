def crear_tablero():
    return [[" " for _ in range(3)] for _ in range(3)]

def mostrar_tablero(tablero):
    print("\n")
    for fila in tablero:
        print(" | ".join(fila))
        print("-" * 9)

def verificar_victoria(tablero, jugador):
    # Revisar filas
    for fila in tablero:
        if all(celda == jugador for celda in fila):
            return True

    # Revisar columnas
    for col in range(3):
        if all(tablero[fila][col] == jugador for fila in range(3)):
            return True

    # Revisar diagonales
    if all(tablero[i][i] == jugador for i in range(3)):
        return True
    if all(tablero[i][2 - i] == jugador for i in range(3)):
        return True

    return False

def tablero_lleno(tablero):
    return all(celda != " " for fila in tablero for celda in fila)

def obtener_jugada(jugador, tablero):
    while True:
        try:
            fila = int(input(f"Jugador {jugador}, ingresa la fila (0-2): "))
            columna = int(input(f"Jugador {jugador}, ingresa la columna (0-2): "))
            if fila not in range(3) or columna not in range(3):
                print("❌ Posición fuera del rango. Intenta de nuevo.")
            elif tablero[fila][columna] != " ":
                print("❌ Esa casilla ya está ocupada. Intenta de nuevo.")
            else:
                return fila, columna
        except ValueError:
            print("❌ Entrada inválida. Debes ingresar números enteros del 0 al 2.")

def jugar():
    tablero = crear_tablero()
    jugador_actual = "X"
    mostrar_tablero(tablero)

    while True:
        fila, columna = obtener_jugada(jugador_actual, tablero)
        tablero[fila][columna] = jugador_actual
        mostrar_tablero(tablero)

        if verificar_victoria(tablero, jugador_actual):
            print(f"🎉 ¡Jugador {jugador_actual} gana!")
            break
        elif tablero_lleno(tablero):
            print("🤝 ¡Empate!")
            break

        jugador_actual = "O" if jugador_actual == "X" else "X"

if __name__ == "__main__":
    jugar()
