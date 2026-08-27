from amortizacion import calcular_cuota, generar_tabla_amortizacion

def test_calcular_cuota_basico():
    resultado = calcular_cuota(100000, 12, 36)
    assert round(resultado, 2) == 3321.43

def test_tabla_amortizacion_saldo_final_cercano_a_cero():
    tabla = generar_tabla_amortizacion(100000, 12, 36)
    ultimo_saldo = tabla[-1]["saldo"]
    assert abs(ultimo_saldo) < 1  # tolerancia por redondeo

def test_tabla_tiene_el_numero_correcto_de_meses():
    tabla = generar_tabla_amortizacion(50000, 10, 24)
    assert len(tabla) == 24