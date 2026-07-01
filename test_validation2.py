import math

# Funciones de validación
def validate_numeric(user_input, expected, tolerance=0.01):
    if not user_input or user_input.strip() == "":
        return False, None
    try:
        clean_input = user_input.replace(",", ".").strip()
        val = float(clean_input)
        if math.isclose(val, expected, abs_tol=tolerance):
            return True, val
        else:
            return False, val
    except ValueError:
        return False, None

def validate_string(user_input, expected):
    if not user_input or user_input.strip() == "":
        return False
    norm_user = user_input.lower().replace(" ", "").replace(",", ".")
    norm_expected = expected.lower().replace(" ", "").replace(",", ".")
    return norm_user == norm_expected

def calcular_nota(puntaje, puntaje_max, exigencia=0.6):
    if puntaje_max <= 0:
        return 1.0
    puntaje_corte = exigencia * puntaje_max
    if puntaje < puntaje_corte:
        nota = 1.0 + 3.0 * (puntaje / puntaje_corte)
    else:
        nota = 4.0 + 3.0 * ((puntaje - puntaje_corte) / (puntaje_max - puntaje_corte))
    return round(nota, 1)

# Datos de la Variación 1 (Original) de la Guía 2
datos = {
    "p1": {
        "x0": 2.0,
        "y0": 8.0,
        "m_t": 2.0,
        "m_n": -0.5,
        "eq_t": "Y = 2X + 4",
        "eq_n": "Y = -0.5X + 9"
    },
    "p2": {
        "m_c": 0.75,
        "m_d": 4.0,
        "eq_d_m": 4.0,
        "eq_d_n": -16.0,
        "inter_x": 4.62,
        "inter_y": 2.46
    },
    "p3": {
        "d1_a": 375.0, "d1_b": -150.0, "d1_c": 8.0,
        "d2_a": 750.0, "d2_b": -150.0,
        "d3": 750.0
    },
    "p4": {
        "punto_t_horiz": "(1,-6)"
    },
    "p5": {
        "x0": -2.0,
        "y0": -9.0,
        "lim_m": 2.0,
        "tabla": [
            {"x": -1.8, "fx": -8.56, "dx": 0.2, "dy": 0.44, "m": 2.2},
            {"x": -1.9, "fx": -8.79, "dx": 0.1, "dy": 0.21, "m": 2.1},
            {"x": -1.99, "fx": -8.9799, "dx": 0.01, "dy": 0.0201, "m": 2.01},
            {"x": -1.999, "fx": -8.998, "dx": 0.001, "dy": 0.002, "m": 2.001},
            {"x": -1.9999, "fx": -8.9998, "dx": 0.0001, "dy": 0.0002, "m": 2.0}
        ]
    }
}

# Simular respuestas correctas ingresadas por un usuario para la Guía 2
respuestas_usuario = {
    # Pregunta 1
    "p1_t_slope": "2",
    "p1_n_slope": "-0.50",
    "p1_eq_t": "Y = 2X + 4",
    "p1_eq_n": "Y = -0.5X + 9",
    
    # Pregunta 2
    "p2_slope_c": "0,75", # usando coma
    "p2_eq_d_m": "4.0",
    "p2_eq_d_n": "-16",
    "p2_inter_x": "4.62",
    "p2_inter_y": "2.46",
    
    # Pregunta 3
    "p3_d1_a": "375",
    "p3_d1_b": "-150",
    "p3_d1_c": "8",
    "p3_d2_a": "750",
    "p3_d2_b": "-150",
    "p3_d3": "750",
    
    # Pregunta 4
    "p4_pt": "(1,-6)",
    
    # Pregunta 5
    "p5_row1_fx": "-8.56", "p5_row1_dx": "0.2", "p5_row1_dy": "0.44", "p5_row1_m": "2.2",
    "p5_row2_fx": "-8.79", "p5_row2_dx": "0.1", "p5_row2_dy": "0.21", "p5_row2_m": "2.1",
    "p5_row3_fx": "-8.9799", "p5_row3_dx": "0.01", "p5_row3_dy": "0.0201", "p5_row3_m": "2.01",
    "p5_row4_fx": "-8.998", "p5_row4_dx": "0.001", "p5_row4_dy": "0.002", "p5_row4_m": "2.001",
    "p5_row5_fx": "-8.9998", "p5_row5_dx": "0.0001", "p5_row5_dy": "0.0002", "p5_row5_m": "2.0",
    "p5_limit": "2"
}

def evaluar_prueba():
    puntos = 0.0
    
    # Pregunta 1 (20 pts)
    puntos += 3.0 if validate_numeric(respuestas_usuario["p1_t_slope"], datos["p1"]["m_t"])[0] else 0.0
    puntos += 3.0 if validate_numeric(respuestas_usuario["p1_n_slope"], datos["p1"]["m_n"])[0] else 0.0
    puntos += 7.0 if validate_string(respuestas_usuario["p1_eq_t"], datos["p1"]["eq_t"]) else 0.0
    puntos += 7.0 if validate_string(respuestas_usuario["p1_eq_n"], datos["p1"]["eq_n"]) else 0.0
    
    # Pregunta 2 (15 pts)
    puntos += 3.0 if validate_numeric(respuestas_usuario["p2_slope_c"], datos["p2"]["m_c"], tolerance=0.05)[0] else 0.0
    
    p2_b_m = validate_numeric(respuestas_usuario["p2_eq_d_m"], datos["p2"]["eq_d_m"], tolerance=0.05)[0]
    p2_b_n = validate_numeric(respuestas_usuario["p2_eq_d_n"], datos["p2"]["eq_d_n"], tolerance=0.05)[0]
    puntos += 6.0 if (p2_b_m and p2_b_n) else 0.0
    
    p2_c_x = validate_numeric(respuestas_usuario["p2_inter_x"], datos["p2"]["inter_x"], tolerance=0.05)[0]
    p2_c_y = validate_numeric(respuestas_usuario["p2_inter_y"], datos["p2"]["inter_y"], tolerance=0.05)[0]
    puntos += 6.0 if (p2_c_x and p2_c_y) else 0.0
    
    # Pregunta 3 (7 pts)
    p3_a_1 = validate_numeric(respuestas_usuario["p3_d1_a"], datos["p3"]["d1_a"])[0]
    p3_a_2 = validate_numeric(respuestas_usuario["p3_d1_b"], datos["p3"]["d1_b"])[0]
    p3_a_3 = validate_numeric(respuestas_usuario["p3_d1_c"], datos["p3"]["d1_c"])[0]
    puntos += 3.0 if (p3_a_1 and p3_a_2 and p3_a_3) else 0.0
    
    p3_b_1 = validate_numeric(respuestas_usuario["p3_d2_a"], datos["p3"]["d2_a"])[0]
    p3_b_2 = validate_numeric(respuestas_usuario["p3_d2_b"], datos["p3"]["d2_b"])[0]
    puntos += 2.0 if (p3_b_1 and p3_b_2) else 0.0
    
    puntos += 2.0 if validate_numeric(respuestas_usuario["p3_d3"], datos["p3"]["d3"])[0] else 0.0
    
    # Pregunta 4 (6 pts)
    puntos += 6.0 if validate_string(respuestas_usuario["p4_pt"], datos["p4"]["punto_t_horiz"]) else 0.0
    
    # Pregunta 5 (25 pts)
    c_puntos_tabla = 0.0
    for idx, fila in enumerate(datos["p5"]["tabla"], 1):
        key_fx = f"p5_row{idx}_fx"
        key_dx = f"p5_row{idx}_dx"
        key_dy = f"p5_row{idx}_dy"
        key_m = f"p5_row{idx}_m"
        
        c_puntos_tabla += 1.0 if validate_numeric(respuestas_usuario[key_fx], fila["fx"], tolerance=0.0005)[0] else 0.0
        c_puntos_tabla += 1.0 if validate_numeric(respuestas_usuario[key_dx], fila["dx"], tolerance=0.0005)[0] else 0.0
        c_puntos_tabla += 1.0 if validate_numeric(respuestas_usuario[key_dy], fila["dy"], tolerance=0.0005)[0] else 0.0
        c_puntos_tabla += 1.0 if validate_numeric(respuestas_usuario[key_m], fila["m"], tolerance=0.005)[0] else 0.0
        
    puntos += c_puntos_tabla
    puntos += 5.0 if validate_numeric(respuestas_usuario["p5_limit"], datos["p5"]["lim_m"], tolerance=0.01)[0] else 0.0
    
    nota = calcular_nota(puntos, 73.0)
    print(f"Puntaje total obtenido: {puntos} / 73.0")
    print(f"Nota obtenida: {nota}")
    return puntos, nota

if __name__ == "__main__":
    evaluar_prueba()
