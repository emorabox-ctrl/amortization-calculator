from amortizacion import generar_tabla_amortizacion, generar_tabla_tasa_variable, comparar_escenarios, exportar_a_excel

def pedir_numero(mensaje, tipo=float):
    while True:
        entrada = input(mensaje)
        try:
            valor = tipo(entrada)
            if valor <= 0:
                print("El valor debe ser mayor a 0. Intenta de nuevo.\n")
                continue
            return valor
        except ValueError:
            print("Eso no es un número válido. Intenta de nuevo.\n")

def pedir_datos():
    monto = pedir_numero("Monto del préstamo: ", float)
    tasa_anual = pedir_numero("Tasa de interés anual (%): ", float)
    plazo_meses = pedir_numero("Plazo en meses: ", int)
    return monto, tasa_anual, plazo_meses

def pedir_abonos_extra():
    abonos = {}
    respuesta = input("\n¿Quieres simular abonos extra a capital? (s/n): ").strip().lower()
    
    if respuesta != "s":
        return abonos
    
    print("Ingresa los abonos uno por uno. Cuando termines, deja el mes en blanco y presiona Enter.\n")
    
    while True:
        mes_texto = input("Mes del abono (o Enter para terminar): ").strip()
        if mes_texto == "":
            break
        try:
            mes = int(mes_texto)
        except ValueError:
            print("Eso no es un número válido de mes. Intenta de nuevo.\n")
            continue
        
        monto_abono = pedir_numero(f"Monto del abono extra en el mes {mes}: ", float)
        abonos[mes] = monto_abono
    
    return abonos

def pedir_tramos_variable():
    print("\nDefine los tramos de tasa variable. El primer tramo debe empezar en el mes 1.")
    print("Cuando termines, deja el mes en blanco y presiona Enter.\n")
    
    tramos = {}
    while True:
        mes_texto = input("Mes desde el cual aplica esta tasa (o Enter para terminar): ").strip()
        if mes_texto == "":
            break
        try:
            mes = int(mes_texto)
        except ValueError:
            print("Eso no es un número válido de mes. Intenta de nuevo.\n")
            continue
        
        tasa = pedir_numero(f"Tasa anual (%) a partir del mes {mes}: ", float)
        tramos[mes] = tasa
    
    if 1 not in tramos:
        print("\nAdvertencia: no definiste una tasa para el mes 1. Se usará la primera tasa que diste para todo el inicio.")
    
    return tramos

def mostrar_tabla(tabla):
    tiene_tasa = "tasa_anual" in tabla[0]
    
    if tiene_tasa:
        print("\n{:<5} {:<8} {:<12} {:<12} {:<12} {:<14} {:<12}".format(
            "Mes", "Tasa%", "Cuota", "Interés", "Capital", "Abono Extra", "Saldo"
        ))
        print("-" * 78)
        for fila in tabla:
            print("{:<5} {:<8} {:<12.2f} {:<12.2f} {:<12.2f} {:<14.2f} {:<12.2f}".format(
                fila["mes"], fila["tasa_anual"], fila["cuota"], fila["interes"],
                fila["capital"], fila["abono_extra"], fila["saldo"]
            ))
    else:
        print("\n{:<5} {:<12} {:<12} {:<12} {:<14} {:<12}".format(
            "Mes", "Cuota", "Interés", "Capital", "Abono Extra", "Saldo"
        ))
        print("-" * 70)
        for fila in tabla:
            print("{:<5} {:<12.2f} {:<12.2f} {:<12.2f} {:<14.2f} {:<12.2f}".format(
                fila["mes"], fila["cuota"], fila["interes"], fila["capital"],
                fila["abono_extra"], fila["saldo"]
            ))
    
    print(f"\nTotal de meses pagados: {len(tabla)}")

def preguntar_exportar(tabla):
    respuesta = input("\n¿Quieres exportar esta tabla a Excel? (s/n): ").strip().lower()
    if respuesta == "s":
        nombre = input("Nombre del archivo (Enter para usar 'tabla_amortizacion.xlsx'): ").strip()
        if nombre == "":
            nombre = "tabla_amortizacion.xlsx"
        if not nombre.endswith(".xlsx"):
            nombre += ".xlsx"
        archivo_generado = exportar_a_excel(tabla, nombre)
        print(f"Archivo guardado como: {archivo_generado}")

def mostrar_comparacion(resultado):
    print("\n===== Comparación: Tasa Fija vs Tasa Variable =====")
    print(f"Total pagado (tasa fija):      {resultado['total_pagado_fija']:.2f}")
    print(f"Total pagado (tasa variable):  {resultado['total_pagado_variable']:.2f}")
    print(f"Total interés (tasa fija):     {resultado['total_interes_fija']:.2f}")
    print(f"Total interés (tasa variable): {resultado['total_interes_variable']:.2f}")
    
    diferencia = resultado["diferencia"]
    if diferencia > 0:
        print(f"\nLa tasa variable resulta MÁS CARA por {diferencia:.2f}")
    elif diferencia < 0:
        print(f"\nLa tasa variable resulta MÁS BARATA por {abs(diferencia):.2f}")
    else:
        print("\nAmbos escenarios cuestan exactamente lo mismo.")

def flujo_amortizacion_normal():
    monto, tasa_anual, plazo_meses = pedir_datos()
    abonos_extra = pedir_abonos_extra()
    tabla = generar_tabla_amortizacion(monto, tasa_anual, plazo_meses, abonos_extra)
    mostrar_tabla(tabla)
    preguntar_exportar(tabla)

def flujo_comparacion():
    monto = pedir_numero("Monto del préstamo: ", float)
    plazo_meses = pedir_numero("Plazo en meses: ", int)
    tasa_fija = pedir_numero("Tasa fija anual (%) para el escenario fijo: ", float)
    tramos_variable = pedir_tramos_variable()
    
    resultado = comparar_escenarios(monto, tasa_fija, tramos_variable, plazo_meses)
    mostrar_comparacion(resultado)

def main():
    print("=== Calculadora de Amortización de Créditos ===\n")
    print("1. Calcular tabla de amortización (tasa fija)")
    print("2. Comparar tasa fija vs tasa variable")
    
    opcion = input("\nElige una opción (1 o 2): ").strip()
    
    if opcion == "1":
        flujo_amortizacion_normal()
    elif opcion == "2":
        flujo_comparacion()
    else:
        print("Opción no válida. Ejecuta el programa de nuevo y elige 1 o 2.")

if __name__ == "__main__":
    main()