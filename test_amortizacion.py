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

def test_calcular_cuota_tasa_cero():
    resultado = calcular_cuota(120000, 0, 12)
    assert round(resultado, 2) == 10000.00

def test_tabla_amortizacion_tasa_cero():
    tabla = generar_tabla_amortizacion(120000, 0, 12)
    
    # Cada cuota debe ser 10000 exacto (120000 / 12)
    for fila in tabla:
        assert round(fila["cuota"], 2) == 10000.00
        assert round(fila["interes"], 2) == 0.00
        assert round(fila["capital"], 2) == 10000.00
    
    # El saldo final debe ser 0 exacto (no solo cercano)
    assert tabla[-1]["saldo"] == 0

def test_tabla_con_abono_extra_reduce_plazo():
    tabla_sin_abono = generar_tabla_amortizacion(100000, 12, 36)
    tabla_con_abono = generar_tabla_amortizacion(100000, 12, 36, {6: 20000})
    
    # Con el abono, el préstamo debe pagarse en menos meses
    assert len(tabla_con_abono) < len(tabla_sin_abono)
    
    # El abono debe reflejarse exactamente en el mes 6
    assert tabla_con_abono[5]["abono_extra"] == 20000
    
    # El saldo final debe llegar a 0 (con tolerancia por redondeo)
    assert abs(tabla_con_abono[-1]["saldo"]) < 1