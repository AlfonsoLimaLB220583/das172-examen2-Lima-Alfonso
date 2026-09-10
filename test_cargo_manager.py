"""
Módulo de pruebas unitarias para el sistema AeroCargo-Matrix.

Asignatura: Desarrollo de Algoritmos para la Simulación de Sistemas [DAS172]
Evaluación: EVA106 - Examen Teórico Unidad II
"""

import unittest
from cargo_manager import (
    validar_matrices,
    calcular_ocupacion_y_sobrecarga,
    evaluar_balance,
    extraer_submatriz_critica
)

class TestCargoManager(unittest.TestCase):

    def test_validar_dimensiones_invalidas(self):
        """Verifica que matrices de tamaño menor a 2x2 sean rechazadas."""
        cargas = [[100, 200]]
        caps = [[100, 200]]
        self.assertFalse(validar_matrices(cargas, caps))

    def test_capacidad_invalida_cero_o_negativa(self):
        """Verifica que el sistema rechace capacidades menores o iguales a cero."""
        cargas_validas = [[100, 100], [100, 100]]
        
        # Caso con capacidad igual a 0
        caps_cero = [[100, 0], [100, 100]]
        self.assertFalse(validar_matrices(cargas_validas, caps_cero))

        # Caso con capacidad negativa
        caps_negativa = [[100, -50], [100, 100]]
        self.assertFalse(validar_matrices(cargas_validas, caps_negativa))

    def test_desbalance_columnas_impares(self):
        """Verifica que la columna central se omita correctamente al evaluar desbalance con columnas impares."""
        cargas = [
            [500, 9999, 500],
            [300, 8888, 300]
        ]
        # Izquierda: 500 + 300 = 800 | Derecha: 500 + 300 = 800 -> Desbalance = 0
        resultado = evaluar_balance(cargas, tolerancia_kg=10)
        self.assertEqual(resultado["desbalance_lateral_kg"], 0.0)
        self.assertTrue(resultado["esta_balanceado"])

    def test_sobrecarga_deteccion(self):
        """Verifica el cálculo correcto de porcentajes y la detección de celdas sobrecargadas (> 100%)."""
        cargas = [[150, 50], [50, 50]]
        caps = [[100, 100], [100, 100]]
        res = calcular_ocupacion_y_sobrecarga(cargas, caps)
        self.assertIn((0, 0), res["coordenadas_sobrecarga"])
        self.assertEqual(len(res["coordenadas_sobrecarga"]), 1)

    def test_extraccion_submatriz_critica(self):
        """Verifica la extracción de la ventana k x p con mayor ocupación promedio."""
        matriz_pct = [
            [50.0, 60.0, 70.0],
            [80.0, 90.0, 100.0],
            [10.0, 20.0, 30.0]
        ]
        submatriz = extraer_submatriz_critica(matriz_pct, 2, 2)
        esperada = [[60.0, 70.0], [90.0, 100.0]]
        self.assertEqual(submatriz, esperada)

if __name__ == "__main__":
    unittest.main()