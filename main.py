from amortizacion import generar_tabla_amortizacion

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

def mostrar_tabla(tabla):
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

def main():
    monto, tasa_anual, plazo_meses = pedir_datos()
    abonos_extra = pedir_abonos_extra()
    tabla = generar_tabla_amortizacion(monto, tasa_anual, plazo_meses, abonos_extra)
    mostrar_tabla(tabla)

if __name__ == "__main__":
    main()