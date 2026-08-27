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

def mostrar_tabla(tabla):
    print("\n{:<5} {:<12} {:<12} {:<12} {:<12}".format("Mes", "Cuota", "Interés", "Capital", "Saldo"))
    print("-" * 55)
    for fila in tabla:
        print("{:<5} {:<12.2f} {:<12.2f} {:<12.2f} {:<12.2f}".format(
            fila["mes"], fila["cuota"], fila["interes"], fila["capital"], fila["saldo"]
        ))

def main():
    monto, tasa_anual, plazo_meses = pedir_datos()
    tabla = generar_tabla_amortizacion(monto, tasa_anual, plazo_meses)
    mostrar_tabla(tabla)

if __name__ == "__main__":
    main()