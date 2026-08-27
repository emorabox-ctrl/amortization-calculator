# Calculadora de Amortización de Créditos

Programa en Python que calcula la tabla de amortización de un préstamo, 
mostrando cuota, interés, capital y saldo pendiente mes a mes.

## Motivación

Como analista de crédito, trabajo diariamente con cálculos de amortización. 
Este proyecto es mi primer paso en desarrollo de software, aplicando ese 
conocimiento del dominio para construir una herramienta útil desde cero.

## Cómo funciona

El programa usa el método de cuota fija (sistema francés) para calcular:
- La cuota mensual fija de un préstamo
- El desglose de cada pago en interés y capital
- El saldo pendiente después de cada cuota

## Cómo ejecutarlo

Requisitos: Python 3.x instalado.

```bash
python main.py
```

El programa te pedirá:
- Monto del préstamo
- Tasa de interés anual (%)
- Plazo en meses

Y mostrará la tabla completa de amortización.

## Estructura del proyecto

- `main.py`: interacción con el usuario (entrada de datos, presentación de resultados)
- `amortizacion.py`: lógica de cálculo (cuota, tabla de amortización)

## Próximas mejoras

- Comparación entre tasa fija y variable
- Soporte para pagos extraordinarios
- Exportar tabla a Excel/PDF