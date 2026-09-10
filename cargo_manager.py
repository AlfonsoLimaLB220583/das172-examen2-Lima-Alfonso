"""
Módulo de procesamiento matricial para balance y auditoría de carga (AeroCargo-Matrix).

Asignatura: Desarrollo de Algoritmos para la Simulación de Sistemas [DAS172]
Evaluación: EVA106 - Examen Teórico Unidad II
"""

from typing import List, Tuple, Dict, Any, Optional

def validar_matrices(cargas: List[List[float]], capacidades: List[List[float]]) -> bool:
    """
    Valida la coherencia dimensional y las restricciones de valores para las matrices de entrada.

    Parámetros:
    ----------
    cargas : List[List[float]]
        Matriz bidimensional de N x M con los pesos reales colocados en cada celda [kg].
    capacidades : List[List[float]]
        Matriz bidimensional de N x M con la capacidad máxima soportada por celda [kg].

    Retorna:
    -------
    bool
        True si ambas matrices cumplen las dimensiones mínimas (N >= 2, M >= 2), son regulares,
        tienen el mismo tamaño, cargas >= 0 y capacidades > 0. False en caso contrario.
    """
    if not cargas or not capacidades:
        return False

    N = len(cargas)
    M = len(cargas[0]) if N > 0 else 0

    if N < 2 or M < 2:
        return False

    if len(capacidades) != N:
        return False

    for i in range(N):
        if len(cargas[i]) != M or len(capacidades[i]) != M:
            return False

        for j in range(M):
            if cargas[i][j] < 0 or capacidades[i][j] <= 0:
                return False

    return True


def calcular_ocupacion_y_sobrecarga(
    cargas: List[List[float]], capacidades: List[List[float]]
) -> Dict[str, Any]:
    """
    Calcula el porcentaje de ocupación de cada celda y registra las celdas con sobrecarga.

    Parámetros:
    ----------
    cargas : List[List[float]]
        Matriz bidimensional de N x M con los pesos reales [kg].
    capacidades : List[List[float]]
        Matriz bidimensional de N x M con las capacidades máximas [kg].

    Retorna:
    -------
    Dict[str, Any]
        Diccionario con la siguiente estructura:
        - "matriz_porcentajes": Matriz de N x M con los porcentajes de ocupación ((Carga/Capacidad)*100).
        - "coordenadas_sobrecarga": Lista de tuplas (fila, columna) indicando celdas que superan el 100.0%.
    """
    N = len(cargas)
    M = len(cargas[0])

    matriz_porcentajes: List[List[float]] = []
    coordenadas_sobrecarga: List[Tuple[int, int]] = []

    for i in range(N):
        fila_porcentajes: List[float] = []
        for j in range(M):
            porcentaje = (cargas[i][j] / capacidades[i][j]) * 100.0
            fila_porcentajes.append(round(porcentaje, 2))
            
            if porcentaje > 100.0:
                coordenadas_sobrecarga.append((i, j))
                
        matriz_porcentajes.append(fila_porcentajes)

    return {
        "matriz_porcentajes": matriz_porcentajes,
        "coordenadas_sobrecarga": coordenadas_sobrecarga
    }


def evaluar_balance(cargas: List[List[float]], tolerancia_kg: float) -> Dict[str, Any]:
    """
    Evalúa el peso total por filas longitudinales y calcula el desbalance lateral en kg.

    Parámetros:
    ----------
    cargas : List[List[float]]
        Matriz bidimensional de N x M con los pesos reales [kg].
    tolerancia_kg : float
        Umbral máximo permitido de desbalance lateral expresado en kilogramos [kg].

    Retorna:
    -------
    Dict[str, Any]
        Diccionario con la siguiente estructura:
        - "pesos_longitudinales": Lista de N elementos con la suma total de peso por fila.
        - "desbalance_lateral_kg": Diferencia absoluta de peso entre el lado izquierdo y derecho [kg].
        - "esta_balanceado": Booleano que indica si el desbalance lateral es <= tolerancia_kg.
    """
    N = len(cargas)
    M = len(cargas[0])

    pesos_longitudinales = [sum(fila) for fila in cargas]

    mitad = M // 2
    peso_izquierda = 0.0
    peso_derecha = 0.0

    for fila in cargas:
        peso_izquierda += sum(fila[:mitad])
        if M % 2 == 0:
            peso_derecha += sum(fila[mitad:])
        else:
            # Si M es impar, se omite la columna central por ubicarse sobre el eje de simetría
            peso_derecha += sum(fila[mitad + 1:])

    desbalance_lateral = abs(peso_izquierda - peso_derecha)
    esta_balanceado = desbalance_lateral <= tolerancia_kg

    return {
        "pesos_longitudinales": pesos_longitudinales,
        "desbalance_lateral_kg": round(desbalance_lateral, 2),
        "esta_balanceado": esta_balanceado
    }


def extraer_submatriz_critica(
    matriz_porcentajes: List[List[float]], k: int, p: int
) -> Optional[List[List[float]]]:
    """
    Recorre la matriz de ocupación mediante una ventana de k x p para identificar la submatriz crítica.

    Parámetros:
    ----------
    matriz_porcentajes : List[List[float]]
        Matriz bidimensional de N x M con los porcentajes de ocupación por celda.
    k : int
        Número de filas de la ventana/submatriz de búsqueda.
    p : int
        Número de columnas de la ventana/submatriz de búsqueda.

    Retorna:
    -------
    Optional[List[List[float]]]
        Submatriz de k x p que presenta la mayor concentración promedio de ocupación.
        Retorna None si las dimensiones (k, p) no son válidas o superan el tamaño de la matriz.
    """
    N = len(matriz_porcentajes)
    M = len(matriz_porcentajes[0])

    if k > N or p > M or k <= 0 or p <= 0:
        return None

    max_promedio = -1.0
    submatriz_optima: Optional[List[List[float]]] = None

    for i in range(N - k + 1):
        for j in range(M - p + 1):
            submatriz_actual = [fila[j:j + p] for fila in matriz_porcentajes[i:i + k]]
            suma_total = sum(sum(fila) for fila in submatriz_actual)
            promedio = suma_total / (k * p)

            if promedio > max_promedio:
                max_promedio = promedio
                submatriz_optima = submatriz_actual

    return submatriz_optima