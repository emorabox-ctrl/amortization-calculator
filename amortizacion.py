def calcular_cuota(monto, tasa_anual, plazo_meses):
    """
    Calcula la cuota mensual fija de un préstamo.
    
    monto: cantidad prestada (ej. 100000)
    tasa_anual: tasa de interés anual en porcentaje (ej. 12 para 12%)
    plazo_meses: número de cuotas mensuales (ej. 36)
    """
    tasa_mensual = (tasa_anual / 100) / 12
    
    if tasa_mensual == 0:
        return monto / plazo_meses
    
    cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** plazo_meses) / ((1 + tasa_mensual) ** plazo_meses - 1)
    
    return cuota


def generar_tabla_amortizacion(monto, tasa_anual, plazo_meses, abonos_extra=None):
    """
    Genera la tabla de amortización completa, mes por mes.
    
    abonos_extra: diccionario opcional {mes: monto_extra}, ej. {6: 5000}
                  significa un abono extra de 5000 en el mes 6.
    Devuelve una lista de diccionarios con el detalle de cada cuota.
    """
    if abonos_extra is None:
        abonos_extra = {}
    
    tasa_mensual = (tasa_anual / 100) / 12
    cuota = calcular_cuota(monto, tasa_anual, plazo_meses)
    
    saldo = monto
    tabla = []
    mes = 1
    
    while saldo > 0.01 and mes <= plazo_meses:
        if tasa_mensual == 0:
            interes = 0
        else:
            interes = saldo * tasa_mensual
        
        capital = cuota - interes
        abono = abonos_extra.get(mes, 0)
        
        # Si el saldo restante es menor que la cuota + abono, ajustamos para no pasarnos
        if capital + abono > saldo:
            capital = saldo - abono if saldo - abono > 0 else saldo
            abono = saldo - capital if capital == saldo else abono
        
        saldo = saldo - capital - abono
        if saldo < 0:
            saldo = 0
        
        tabla.append({
            "mes": mes,
            "cuota": cuota,
            "interes": interes,
            "capital": capital,
            "abono_extra": abono,
            "saldo": saldo
        })
        
        mes += 1
    
    return tabla