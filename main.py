from cargo_manager import (
    validar_matrices,
    calcular_ocupacion_y_sobrecarga,
    evaluar_balance,
    extraer_submatriz_critica
)

def ejecutar_demostracion():
    cargas_reales = [
        [1200.0, 800.0,  900.0,  1500.0],
        [1000.0, 1100.0, 1050.0, 950.0],
        [600.0,  700.0,  650.0,  800.0]
    ]

    capacidades_maximas = [
        [1000.0, 1000.0, 1000.0, 1000.0],
        [1000.0, 1000.0, 1000.0, 1000.0],
        [800.0,  800.0,  800.0,  800.0]
    ]

    tolerancia_desbalance_kg = 500.0

    print("=== AUDITORÍA AEROCARGO-MATRIX ===")
    
    es_valido = validar_matrices(cargas_reales, capacidades_maximas)
    print(f"\n[1] Validación de Matrices: {'APROBADA' if es_valido else 'RECHAZADA'}")
    if not es_valido:
        return

    res_ocupacion = calcular_ocupacion_y_sobrecarga(cargas_reales, capacidades_maximas)
    print("\n[2] Matriz de Ocupación (%):")
    for fila in res_ocupacion["matriz_porcentajes"]:
        print("    ", [f"{v:.1f}%" for v in fila])
    
    print(f"Celdas sobrecargadas (Fila, Col): {res_ocupacion['coordenadas_sobrecarga']}")

    res_balance = evaluar_balance(cargas_reales, tolerancia_desbalance_kg)
    print("\n[3] Evaluación de Balance:")
    print(f"    Pesos por fila longitudinal [kg]: {res_balance['pesos_longitudinales']}")
    print(f"    Desbalance lateral: {res_balance['desbalance_lateral_kg']} kg")
    print(f"    Estado de Balance (Tol = {tolerancia_desbalance_kg} kg): {'APROBADO' if res_balance['esta_balanceado'] else 'RECHAZADO'}")

    k, p = 2, 2
    submatriz = extraer_submatriz_critica(res_ocupacion["matriz_porcentajes"], k, p)
    print(f"\n[4] Submatriz Crítica de Mayor Ocupación ({k}x{p}):")
    if submatriz:
        for fila in submatriz:
            print("    ", fila)
    print("\n==========================================")
    print("      AUDITORÍA COMPLETADA EXITOSAMENTE   ")
    print("==========================================")

if __name__ == "__main__":
    ejecutar_demostracion()