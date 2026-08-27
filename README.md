# Calculadora de Amortización de Créditos

Programa en Python que calcula la tabla de amortización de un préstamo, 
mostrando cuota, interés, capital y saldo pendiente mes a mes. Incluye 
soporte para simular pagos extraordinarios (abonos a capital).

## Motivación

Como analista de crédito, trabajo diariamente con cálculos de amortización. 
Este proyecto es mi primer paso en desarrollo de software, aplicando ese 
conocimiento del dominio para construir una herramienta útil desde cero.

## Funcionalidades

- Cálculo de cuota mensual fija (sistema de amortización francés)
- Tabla de amortización completa: cuota, interés, capital y saldo por mes
- Manejo del caso especial de tasa de interés 0%
- Simulación de abonos extraordinarios a capital, que reducen el plazo del préstamo
- Validación de entradas del usuario (rechaza texto inválido y valores negativos)
- Suite de tests automatizados con pytest

## Cómo ejecutarlo

Requisitos: Python 3.x instalado.

```bash
python main.py
```

El programa te pedirá:
- Monto del préstamo
- Tasa de interés anual (%)
- Plazo en meses
- Si quieres simular abonos extraordinarios (opcional), indicando el mes y monto de cada uno

Y mostrará la tabla completa de amortización, incluyendo el total de meses 
pagados (que puede ser menor al plazo original si se simularon abonos).

## Cómo correr los tests

```bash
python -m pytest
```

## Estructura del proyecto

- `main.py`: interacción con el usuario (entrada de datos, presentación de resultados)
- `amortizacion.py`: lógica de cálculo (cuota, tabla de amortización, abonos extra)
- `test_amortizacion.py`: tests automatizados