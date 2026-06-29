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

# Datos de la Variación 1 (Original)
datos = {
    "p1": {
        "a": -4.0, "b": -12.0, "c": 576.0, "d": 350.0,
        "valores_criticos": ["-8", "6"],
        "valores_criticos_str": "6 y -8",
        "min_x": -8.0, "min_y": -2978.0,
        "max_x": 6.0, "max_y": 2510.0,
        "inf_x": -1.0, "inf_y": -234.0
    },
    "p2": {
        "p1_der_cero_opt1": "(1,8)", "p1_der_cero_opt2": "(-1,12)",
        "p2_der_cero": "(0,10)"
    },
    "p3": {
        "exp_m": "6x+4+9/(3x+1)",
        "exp_f": "3x^2+4x+3ln(3x+1)+C",
        "v_5": 34.563,
        "a_2": 5.449
    },
    "p4": {
        "derivada": "1080x^2-3672x+2430",
        "pendiente_min": 0.0,
        "intervalo_dec": "]0.9,2.5[",
        "max_rel": 962.28,
        "concava_arriba": "]1.7,inf[",
        "punto_min_pen_x": 1.7, "punto_min_pen_y": 593.64
    },
    "p5": {
        "A": 240.0, "B": 214.0, "K": 0.65,
        "max_val": 240.0,
        "inf_x": 8.256, "inf_y": 120.0,
        "max_slope": 39.0
    }
}

# Simular respuestas correctas ingresadas por un usuario (con pequeños formatos variables)
respuestas_usuario = {
    # Pregunta 1
    "p1_a": "-4",
    "p1_b": " -12 ",
    "p1_c": "576,0", # usando coma decimal
    "p1_d": "350",
    "p1_crit_sel": "6 y -8",
    "p1_min_x": "-8",
    "p1_min_y": "-2978",
    "p1_max_x": "6",
    "p1_max_y": "2510",
    "p1_inf_x": "-1",
    "p1_inf_y": "-234",
    "p1_int1": "-8",
    "p1_int2": "6",
    
    # Pregunta 2
    "p2_a": "(1,8)",
    "p2_b": "(0,10)",
    
    # Pregunta 3
    "p3_a": "6x + 4 + 9 / (3x + 1)",
    "p3_b": "3x^2+4x+3ln(3x+1)+C",
    "p3_c": "34.563",
    "p3_d": "5,449", # coma decimal
    
    # Pregunta 4
    "p4_a": "1080x^2 - 3672x + 2430",
    "p4_b": "0",
    "p4_c": "]0.9,2.5[",
    "p4_d": "962.28",
    "p4_e": "]1.7,inf[",
    "p4_fx": "1.7",
    "p4_fy": "593.64",
    
    # Pregunta 5
    "p5_a": "240",
    "p5_b": "214",
    "p5_k": "0.65",
    "p5_d": "240",
    "p5_infx": "8.256",
    "p5_infy": "120",
    "p5_slope": "39"
}

def evaluar_prueba():
    puntos = 0.0
    
    # Pregunta 1 (20 pts)
    puntos += 1.0 if validate_numeric(respuestas_usuario["p1_a"], datos["p1"]["a"])[0] else 0.0
    puntos += 1.0 if validate_numeric(respuestas_usuario["p1_b"], datos["p1"]["b"])[0] else 0.0
    puntos += 1.0 if validate_numeric(respuestas_usuario["p1_c"], datos["p1"]["c"])[0] else 0.0
    puntos += 1.0 if validate_numeric(respuestas_usuario["p1_d"], datos["p1"]["d"])[0] else 0.0
    
    # b) Valores críticos (4 pts)
    puntos += 4.0 if respuestas_usuario["p1_crit_sel"] == datos["p1"]["valores_criticos_str"] else 0.0
    
    # c) Mínimo relativo (2 pts)
    puntos += 1.0 if validate_numeric(respuestas_usuario["p1_min_x"], datos["p1"]["min_x"])[0] else 0.0
    puntos += 1.0 if validate_numeric(respuestas_usuario["p1_min_y"], datos["p1"]["min_y"])[0] else 0.0
    
    # d) Máximo relativo (2 pts)
    puntos += 1.0 if validate_numeric(respuestas_usuario["p1_max_x"], datos["p1"]["max_x"])[0] else 0.0
    puntos += 1.0 if validate_numeric(respuestas_usuario["p1_max_y"], datos["p1"]["max_y"])[0] else 0.0
    
    # e) Inflexión (4 pts)
    puntos += 2.0 if validate_numeric(respuestas_usuario["p1_inf_x"], datos["p1"]["inf_x"])[0] else 0.0
    puntos += 2.0 if validate_numeric(respuestas_usuario["p1_inf_y"], datos["p1"]["inf_y"])[0] else 0.0
    
    # f) Intervalo decremento (4 pts)
    int1_ok, _ = validate_numeric(respuestas_usuario["p1_int1"], float(datos["p1"]["valores_criticos"][0]))
    int2_ok, _ = validate_numeric(respuestas_usuario["p1_int2"], float(datos["p1"]["valores_criticos"][1]))
    if not (int1_ok and int2_ok):
        int1_ok_rev, _ = validate_numeric(respuestas_usuario["p1_int1"], float(datos["p1"]["valores_criticos"][1]))
        int2_ok_rev, _ = validate_numeric(respuestas_usuario["p1_int2"], float(datos["p1"]["valores_criticos"][0]))
        if int1_ok_rev and int2_ok_rev:
            int1_ok, int2_ok = True, True
    puntos += 2.0 if int1_ok else 0.0
    puntos += 2.0 if int2_ok else 0.0
    
    # Pregunta 2 (8 pts)
    p2_a_ok = (respuestas_usuario["p2_a"] == datos["p2"]["p1_der_cero_opt1"]) or (respuestas_usuario["p2_a"] == datos["p2"]["p1_der_cero_opt2"])
    puntos += 4.0 if p2_a_ok else 0.0
    puntos += 4.0 if respuestas_usuario["p2_b"] == datos["p2"]["p2_der_cero"] else 0.0
    
    # Pregunta 3 (20 pts)
    puntos += 5.0 if validate_string(respuestas_usuario["p3_a"], datos["p3"]["exp_m"]) else 0.0
    puntos += 5.0 if respuestas_usuario["p3_b"] == datos["p3"]["exp_f"] else 0.0
    puntos += 5.0 if validate_numeric(respuestas_usuario["p3_c"], datos["p3"]["v_5"], tolerance=0.005)[0] else 0.0
    puntos += 5.0 if validate_numeric(respuestas_usuario["p3_d"], datos["p3"]["a_2"], tolerance=0.005)[0] else 0.0
    
    # Pregunta 4 (30 pts)
    puntos += 7.0 if validate_string(respuestas_usuario["p4_a"], datos["p4"]["derivada"]) else 0.0
    puntos += 5.0 if validate_numeric(respuestas_usuario["p4_b"], datos["p4"]["pendiente_min"])[0] else 0.0
    puntos += 5.0 if respuestas_usuario["p4_c"] == datos["p4"]["intervalo_dec"] else 0.0
    puntos += 5.0 if validate_numeric(respuestas_usuario["p4_d"], datos["p4"]["max_rel"], tolerance=0.1)[0] else 0.0
    puntos += 4.0 if respuestas_usuario["p4_e"] == datos["p4"]["concava_arriba"] else 0.0
    puntos += 2.0 if validate_numeric(respuestas_usuario["p4_fx"], datos["p4"]["punto_min_pen_x"])[0] else 0.0
    puntos += 2.0 if validate_numeric(respuestas_usuario["p4_fy"], datos["p4"]["punto_min_pen_y"], tolerance=0.1)[0] else 0.0
    
    # Pregunta 5 (25 pts)
    puntos += 3.0 if validate_numeric(respuestas_usuario["p5_a"], datos["p5"]["A"], tolerance=2.0)[0] else 0.0
    puntos += 3.0 if validate_numeric(respuestas_usuario["p5_b"], datos["p5"]["B"], tolerance=2.0)[0] else 0.0
    puntos += 3.0 if validate_numeric(respuestas_usuario["p5_k"], datos["p5"]["K"], tolerance=0.03)[0] else 0.0
    puntos += 5.0 if respuestas_usuario["p5_d"] == str(int(datos["p5"]["max_val"])) else 0.0
    puntos += 3.0 if validate_numeric(respuestas_usuario["p5_infx"], datos["p5"]["inf_x"], tolerance=0.05)[0] else 0.0
    puntos += 3.0 if validate_numeric(respuestas_usuario["p5_infy"], datos["p5"]["inf_y"], tolerance=1.0)[0] else 0.0
    puntos += 5.0 if validate_numeric(respuestas_usuario["p5_slope"], datos["p5"]["max_slope"], tolerance=0.5)[0] else 0.0
    
    nota = calcular_nota(puntos, 103.0)
    print(f"Puntaje total obtenido: {puntos} / 103.0")
    print(f"Nota obtenida: {nota}")
    return puntos, nota

if __name__ == "__main__":
    evaluar_prueba()
