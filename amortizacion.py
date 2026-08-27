def calcular_cuota(monto, tasa_anual, plazo_meses):
    """
    Calcula la cuota mensual fija de un préstamo.
    
    monto: cantidad prestada (ej. 100000)
    tasa_anual: tasa de interés anual en porcentaje (ej. 12 para 12%)
    plazo_meses: número de cuotas mensuales (ej. 36)
    """
    tasa_mensual = (tasa_anual / 100) / 12
    
    cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** plazo_meses) / ((1 + tasa_mensual) ** plazo_meses - 1)
    
    return cuota
def generar_tabla_amortizacion(monto, tasa_anual, plazo_meses):
    """
    Genera la tabla de amortización completa, mes por mes.
    Devuelve una lista de diccionarios con el detalle de cada cuota.
    """
    tasa_mensual = (tasa_anual / 100) / 12
    cuota = calcular_cuota(monto, tasa_anual, plazo_meses)
    
    saldo = monto
    tabla = []
    
    for mes in range(1, plazo_meses + 1):
        interes = saldo * tasa_mensual
        capital = cuota - interes
        saldo = saldo - capital
        
        tabla.append({
            "mes": mes,
            "cuota": cuota,
            "interes": interes,
            "capital": capital,
            "saldo": saldo
        })
    
    return tabla