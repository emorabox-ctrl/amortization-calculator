# Calculadora de Amortización de Créditos

Programa en Python que calcula la tabla de amortización de un préstamo, 
mostrando cuota, interés, capital y saldo pendiente mes a mes. Incluye 
soporte para pagos extraordinarios, comparación entre tasa fija y variable, 
y exportación de resultados a Excel.

## Motivación

Como analista de crédito, trabajo diariamente con cálculos de amortización. 
Este proyecto es mi primer paso en desarrollo de software, aplicando ese 
conocimiento del dominio para construir una herramienta útil desde cero.

## Funcionalidades

- Cálculo de cuota mensual fija (sistema de amortización francés)
- Tabla de amortización completa: cuota, interés, capital y saldo por mes
- Manejo del caso especial de tasa de interés 0%
- Simulación de abonos extraordinarios a capital, que reducen el plazo del préstamo
- Comparación entre un escenario de tasa fija y uno de tasa variable (con tramos definidos por el usuario), incluyendo recálculo automático de la cuota cuando cambia la tasa
- Exportación de la tabla de amortización a un archivo Excel (.xlsx)
- Menú interactivo para elegir entre calcular una amortización simple o comparar escenarios
- Validación de entradas del usuario (rechaza texto inválido y valores negativos)
- Suite de 9 tests automatizados con pytest

## Cómo ejecutarlo

Requisitos: Python 3.x instalado, junto con la librería `openpyxl`:

```bash
python -m pip install openpyxl
```

Luego corre el programa:

```bash
python main.py
```

El programa muestra un menú con dos opciones:

**1. Calcular tabla de amortización (tasa fija)**
Pide monto, tasa anual y plazo, con la opción de simular abonos extraordinarios 
a capital (indicando mes y monto de cada uno). Al final, permite exportar 
la tabla resultante a un archivo Excel.

**2. Comparar tasa fija vs tasa variable**
Pide monto, plazo, una tasa fija de referencia, y los tramos de tasa variable 
(mes en que cambia y nueva tasa). Muestra el total pagado e interés total 
de cada escenario, y cuál resulta más económico.

## Cómo correr los tests

```bash
python -m pytest
```

## Estructura del proyecto

- `main.py`: interacción con el usuario (menú, entrada de datos, presentación de resultados)
- `amortizacion.py`: lógica de cálculo (cuota, tabla de amortización, abonos extra, tasa variable, comparación de escenarios, exportación a Excel)
- `test_amortizacion.py`: tests automatizados con pytest

## Próximas mejoras

- Interfaz web simple con Streamlit