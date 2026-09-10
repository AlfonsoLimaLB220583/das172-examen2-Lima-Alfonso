"""
Módulo de procesamiento matricial para balance y auditoría de carga (AeroCargo-Matrix).
Asignatura: Desarrollo de Algoritmos para la Simulación de Sistemas [DAS172]
"""

from typing import List, Tuple, Dict, Any, Optional

def validar_matrices(cargas: List[List[float]], capacidades: List[List[float]]) -> bool:
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