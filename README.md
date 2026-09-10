# AeroCargo-Matrix: Auditoría y Balance Matricial de Distribución de Carga

**Asignatura:** Desarrollo de Algoritmos para la Simulación de Sistemas [DAS172]  
**Evaluación:** EVA106 - Examen Teórico Unidad II: Funciones y Arreglos  
**Institución:** Universidad Don Bosco - Facultad de Aeronáutica  

---

## 1. Importancia Operativa y Física del Balance en Aviación

En la aviación comercial y de carga, la gestión de peso y balance es crucial para la seguridad operativa y la integridad de la estructura por dos razones fundamentales:

### Resistencia Estructural e Integridad del Piso
Cada compartimento de la bodega de carga cuenta con un límite estricto de densidad de carga ($kg/m^2$) definido en las especificaciones del fabricante. Sobrepasar la capacidad máxima en una celda individual genera concentraciones de esfuerzo que pueden exceder el límite elástico de las vigas y rieles del piso de carga, comprometiendo la integridad estructural del fuselaje inferior y afectando la canalización de líneas de control hidráulicas y eléctricas subyacentes.

### Estabilidad Aerodinámica y Control de Vuelo
- **Desbalance Lateral (Eje Transversal):** Una asimetría sustancial de peso entre el lado izquierdo (babor) y derecho (estribor) desplaza el Centro de Gravedad ($CG$) fuera de la línea media del avión. Esto genera un momento de alabeo (*roll moment*) no deseado que requiere una deflexión continua de los alerones y spoilers para mantener las alas niveladas. Además, la resistencia inducida asimétrica resultante genera un momento de guiñada (*yaw moment*) que exige compensación con el timón de dirección (*rudder trim*), incrementando la resistencia al avance (*drag*) y el consumo de combustible.
- **Distribución Longitudinal (Eje Anteroposterior):** Mantener la carga equilibrada a lo largo de las filas longitudinales previene que el $CG$ se desplace más allá del límite delantero o trasero (*forward/aft CG limits*), garantizando la autoridad de control del elevador durante las fases de rotación, despegue y aterrizaje.

---

## 2. Arquitectura Modular y Diagrama de Flujo

El sistema está diseñado bajo el principio de **funciones puras e inmutabilidad**, asegurando que los datos de entrada no sufran alteraciones durante las operaciones matriciales.

```text
[Datos de Entrada: Cargas y Capacidades]
                   │
                   ▼
       +-----------------------+
       |   validar_matrices    | ──> [True / False]
       +-----------------------+
                   │ (Si es True)
                   ├───> +----------------------------------+
                   │     | calcular_ocupacion_y_sobrecarga  | ──> [Matriz % y Sobrecargas]
                   │     +----------------------------------+
                   │
                   ├───> +----------------------------------+
                   │     |         evaluar_balance          | ──> [Pesos Filas y Desbalance kg]
                   │     +----------------------------------+
                   │
                   └───> +----------------------------------+
                         |    extraer_submatriz_critica     | ──> [Submatriz Ventana k x p]
                         +----------------------------------+