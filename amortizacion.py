from openpyxl import Workbook

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

def generar_tabla_tasa_variable(monto, tramos, plazo_meses, abonos_extra=None):
    """
    Genera la tabla de amortización cuando la tasa de interés cambia en el tiempo.
    
    tramos: diccionario {mes_desde: tasa_anual}, ej. {1: 10, 13: 14, 25: 8}
            significa que desde el mes 1 la tasa es 10%, desde el mes 13 cambia a 14%, etc.
    Cada vez que cambia la tasa, se recalcula la cuota usando el saldo pendiente
    como nuevo monto y los meses restantes como nuevo plazo.
    """
    if abonos_extra is None:
        abonos_extra = {}
    
    saldo = monto
    tabla = []
    mes = 1
    tasa_actual = tramos[1]  # la tasa del mes 1 siempre debe existir
    meses_restantes = plazo_meses
    cuota = calcular_cuota(saldo, tasa_actual, meses_restantes)
    
    while saldo > 0.01 and mes <= plazo_meses:
        # ¿Cambia la tasa en este mes?
        if mes in tramos:
            tasa_actual = tramos[mes]
            meses_restantes = plazo_meses - mes + 1
            cuota = calcular_cuota(saldo, tasa_actual, meses_restantes)
        
        tasa_mensual = (tasa_actual / 100) / 12
        
        if tasa_mensual == 0:
            interes = 0
        else:
            interes = saldo * tasa_mensual
        
        capital = cuota - interes
        abono = abonos_extra.get(mes, 0)
        
        if capital + abono > saldo:
            capital = saldo - abono if saldo - abono > 0 else saldo
            abono = saldo - capital if capital == saldo else abono
        
        saldo = saldo - capital - abono
        if saldo < 0:
            saldo = 0
        
        tabla.append({
            "mes": mes,
            "tasa_anual": tasa_actual,
            "cuota": cuota,
            "interes": interes,
            "capital": capital,
            "abono_extra": abono,
            "saldo": saldo
        })
        
        mes += 1
    
    return tabla

def comparar_escenarios(monto, tasa_fija, tramos_variable, plazo_meses):
    """
    Compara el total pagado en un escenario de tasa fija vs uno de tasa variable.
    
    Devuelve un diccionario con el resumen de ambos escenarios.
    """
    tabla_fija = generar_tabla_amortizacion(monto, tasa_fija, plazo_meses)
    tabla_variable = generar_tabla_tasa_variable(monto, tramos_variable, plazo_meses)
    
    total_interes_fija = sum(fila["interes"] for fila in tabla_fija)
    total_interes_variable = sum(fila["interes"] for fila in tabla_variable)
    
    total_pagado_fija = sum(fila["cuota"] for fila in tabla_fija)
    total_pagado_variable = sum(fila["cuota"] for fila in tabla_variable)
    
    return {
        "total_interes_fija": total_interes_fija,
        "total_interes_variable": total_interes_variable,
        "total_pagado_fija": total_pagado_fija,
        "total_pagado_variable": total_pagado_variable,
        "diferencia": total_pagado_variable - total_pagado_fija
    }


def exportar_a_excel(tabla, nombre_archivo="tabla_amortizacion.xlsx"):
    """
    Exporta una tabla de amortización a un archivo Excel.
    
    tabla: lista de diccionarios generada por generar_tabla_amortizacion,
           generar_tabla_tasa_variable, etc.
    nombre_archivo: nombre del archivo .xlsx a crear
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Amortizacion"
    
    tiene_tasa = "tasa_anual" in tabla[0]
    
    if tiene_tasa:
        encabezados = ["Mes", "Tasa %", "Cuota", "Interés", "Capital", "Abono Extra", "Saldo"]
    else:
        encabezados = ["Mes", "Cuota", "Interés", "Capital", "Abono Extra", "Saldo"]
    
    ws.append(encabezados)
    
    for fila in tabla:
        if tiene_tasa:
            ws.append([
                fila["mes"], fila["tasa_anual"], round(fila["cuota"], 2),
                round(fila["interes"], 2), round(fila["capital"], 2),
                round(fila["abono_extra"], 2), round(fila["saldo"], 2)
            ])
        else:
            ws.append([
                fila["mes"], round(fila["cuota"], 2), round(fila["interes"], 2),
                round(fila["capital"], 2), round(fila["abono_extra"], 2), round(fila["saldo"], 2)
            ])
    
    wb.save(nombre_archivo)
    return nombre_archivo