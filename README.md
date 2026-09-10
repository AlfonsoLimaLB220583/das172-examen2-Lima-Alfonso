# AeroCargo-Matrix: Auditoría y Balance Matricial

Sistema modular en Python diseñado para auditar la distribución de peso en la bodega de una aeronave, previniendo sobrecargas estructurales y desbalances laterales.

## 1. Importancia Operativa
- **Capacidad de Piso:** Previene deformaciones en el fuselaje al validar los límites de carga por celda.
- **Balance Lateral:** Mantiene la simetría del centro de gravedad entre el lado izquierdo y derecho de la aeronave.

## 2. Arquitectura Modular
- `cargo_manager.py`: Módulo con funciones puras de cálculo.
- `main.py`: Ejecución interactiva y demostración de datos.
- `test_cargo_manager.py`: Pruebas unitarias automatizadas.

## 3. Complejidad Algorítmica
- **Tiempo $O(N \times M)$:** Recorrido directo de cada celda de la matriz.
- **Memoria $O(N \times M)$:** Creación de matrices secundarias de tamaño equivalente.