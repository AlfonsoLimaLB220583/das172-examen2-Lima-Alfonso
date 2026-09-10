import unittest
from cargo_manager import (
    validar_matrices,
    calcular_ocupacion_y_sobrecarga,
    evaluar_balance,
    extraer_submatriz_critica
)

class TestCargoManager(unittest.TestCase):

    def test_validar_dimensiones_invalidas(self):
        cargas = [[100, 200]]
        caps = [[100, 200]]
        self.assertFalse(validar_matrices(cargas, caps))

    def test_desbalance_columnas_impares(self):
        cargas = [
            [500, 9999, 500],
            [300, 8888, 300]
        ]
        resultado = evaluar_balance(cargas, tolerancia_kg=10)
        self.assertEqual(resultado["desbalance_lateral_kg"], 0.0)
        self.assertTrue(resultado["esta_balanceado"])

    def test_sobrecarga_deteccion(self):
        cargas = [[150, 50], [50, 50]]
        caps = [[100, 100], [100, 100]]
        res = calcular_ocupacion_y_sobrecarga(cargas, caps)
        self.assertIn((0, 0), res["coordenadas_sobrecarga"])
        self.assertEqual(len(res["coordenadas_sobrecarga"]), 1)

if __name__ == "__main__":
    unittest.main()