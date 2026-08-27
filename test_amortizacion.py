from amortizacion import calcular_cuota, generar_tabla_amortizacion, generar_tabla_tasa_variable, comparar_escenarios

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

def test_tabla_tasa_variable_cambia_cuota_correctamente():
    tabla = generar_tabla_tasa_variable(100000, {1: 10, 13: 14}, 24)
    
    # Los primeros 12 meses deben tener tasa 10%
    for fila in tabla[:12]:
        assert fila["tasa_anual"] == 10
    
    # A partir del mes 13, la tasa debe ser 14%
    for fila in tabla[12:]:
        assert fila["tasa_anual"] == 14
    
    # La cuota debe cambiar en el mes 13 (índice 12)
    assert tabla[11]["cuota"] != tabla[12]["cuota"]
    
    # El saldo final debe llegar a 0
    assert abs(tabla[-1]["saldo"]) < 1

def test_comparar_escenarios_estructura_correcta():
    resultado = comparar_escenarios(100000, 12, {1: 10, 13: 14}, 24)
    
    # Verifica que existan todas las claves esperadas
    claves_esperadas = {"total_interes_fija", "total_interes_variable", 
                         "total_pagado_fija", "total_pagado_variable", "diferencia"}
    assert set(resultado.keys()) == claves_esperadas
    
    # La diferencia debe ser consistente con los totales pagados
    diferencia_calculada = resultado["total_pagado_variable"] - resultado["total_pagado_fija"]
    assert round(resultado["diferencia"], 2) == round(diferencia_calculada, 2)