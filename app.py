import streamlit as st
import math
import pandas as pd

# Configuración de página
st.set_page_config(
    page_title="Prueba Interactiva de Matemáticas",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para un diseño premium y adaptable (Modo Claro/Oscuro)
st.markdown("""
<style>
    .reportview-container {
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    .stAlert {
        border-radius: 12px;
    }
    .metric-card {
        background-color: var(--background-color, #ffffff);
        color: var(--text-color, #0f172a);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid rgba(128,128,128,0.15);
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-color, #64748b);
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .question-box {
        background-color: var(--background-color, #ffffff);
        color: var(--text-color, #0f172a);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 25px;
        border-left: 5px solid #0284c7;
        border-right: 1px solid rgba(128,128,128,0.1);
        border-top: 1px solid rgba(128,128,128,0.1);
        border-bottom: 1px solid rgba(128,128,128,0.1);
    }
    .question-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color, #0f172a);
        margin-bottom: 15px;
    }
    .subquestion-title {
        font-weight: 500;
        color: var(--text-color, #334155);
        margin-top: 15px;
        margin-bottom: 8px;
    }
    .chilean-nota {
        font-size: 3rem;
        font-weight: 800;
        padding: 10px 20px;
        border-radius: 10px;
        display: inline-block;
    }
    .nota-aprobado {
        color: #0d9488;
        background-color: rgba(13, 148, 136, 0.15);
        border: 2px solid #0d9488;
    }
    .nota-reprobado {
        color: #e11d48;
        background-color: rgba(225, 29, 72, 0.15);
        border: 2px solid #e11d48;
    }
    .helper-box {
        background-color: rgba(2, 132, 199, 0.05);
        border: 1px solid rgba(2, 132, 199, 0.2);
        color: var(--text-color, #0f172a);
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    /* Estilo para alinear verticalmente textos fijos con inputs */
    .inline-text {
        font-size: 1rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        height: 100%;
        margin-top: 0px;
        padding-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- FUNCIONES DE VALIDACIÓN -----------------

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

# ----------------- BASE DE DATOS DE VARIACIONES -----------------
VARIACIONES = {
    "Variación 1 (Original)": {
        "p1": {
            "puntos_enunciado": "A = (-4, -1890), B = (-2, -818), C = (0, 350) \\text{ y } D = (5, 2430)",
            "a": -4.0, "b": -12.0, "c": 576.0, "d": 350.0,
            "valores_criticos": ["-8", "6"],
            "valores_criticos_str": "6 y -8",
            "min_x": -8.0, "min_y": -2978.0,
            "max_x": 6.0, "max_y": 2510.0,
            "inf_x": -1.0, "inf_y": -234.0,
            "intervalo_creciente": "]-8,6["
        },
        "p2": {
            "función_latex": "f(x) = x^3 - 3x + 10",
            "p1_der_cero_opt1": "(1,8)", "p1_der_cero_opt2": "(-1,12)",
            "p2_der_cero": "(0,10)"
        },
        "p3": {
            "tabla": [
                {"x": 1, "m": "10 + \\frac{9}{4}"},
                {"x": 2, "m": "16 + \\frac{9}{7}"},
                {"x": 3, "m": "22 + \\frac{9}{10}"},
                {"x": 4, "m": "28 + \\frac{9}{13}"},
                {"x": 5, "m": "34 + \\frac{9}{16}"}
            ],
            "exp_m": "6x+4+9/(3x+1)",
            "exp_f": "3x^2+4x+3ln(3x+1)+C",
            "v_5": 34.563,
            "a_2": 5.449
        },
        "p4": {
            "función_latex": "f(x) = 360x^3 - 1836x^2 + 2430x",
            "derivada": "1080x^2-3672x+2430",
            "pendiente_min": 0.0,
            "intervalo_dec": "]0.9,2.5[",
            "max_rel": 962.28,
            "concava_arriba": "]1.7,inf[",
            "punto_min_pen_x": 1.7, "punto_min_pen_y": 593.64
        },
        "p5": {
            "tabla": [
                {"x": 2, "y": 4},
                {"x": 3, "y": 8},
                {"x": 4, "y": 14},
                {"x": 5, "y": 26},
                {"x": 6, "y": 45},
                {"x": 7, "y": 73},
                {"x": 8, "y": 110},
                {"x": 9, "y": 148},
                {"x": 12, "y": 221},
                {"x": 17, "y": 239}
            ],
            "A": 240.0, "B": 214.0, "K": 0.65,
            "max_val": 240.0,
            "inf_x": 8.256, "inf_y": 120.0,
            "max_slope": 39.0
        }
    },
    "Variación 2": {
        "p1": {
            "puntos_enunciado": "A = (-3, -232), B = (-2, -96), C = (0, 200) \\text{ y } D = (3, 524)",
            "a": -2.0, "b": -6.0, "c": 144.0, "d": 200.0,
            "valores_criticos": ["-6", "4"],
            "valores_criticos_str": "4 y -6",
            "min_x": -6.0, "min_y": -448.0,
            "max_x": 4.0, "max_y": 552.0,
            "inf_x": -1.0, "inf_y": 52.0,
            "intervalo_creciente": "]-6,4["
        },
        "p2": {
            "función_latex": "f(x) = x^3 - 12x + 15",
            "p1_der_cero_opt1": "(2,-1)", "p1_der_cero_opt2": "(-2,31)",
            "p2_der_cero": "(0,15)"
        },
        "p3": {
            "tabla": [
                {"x": 1, "m": "8 + \\frac{8}{3}"},
                {"x": 2, "m": "13 + \\frac{8}{5}"},
                {"x": 3, "m": "18 + \\frac{8}{7}"},
                {"x": 4, "m": "23 + \\frac{8}{9}"},
                {"x": 5, "m": "28 + \\frac{8}{11}"}
            ],
            "exp_m": "5x+3+8/(2x+1)",
            "exp_f": "2.5x^2+3x+4ln(2x+1)+C",
            "v_5": 28.727,
            "a_2": 4.360
        },
        "p4": {
            "función_latex": "f(x) = 80x^3 - 240x^2 + 180x",
            "derivada": "240x^2-480x+180",
            "pendiente_min": 0.0,
            "intervalo_dec": "]0.5,1.5[",
            "max_rel": 40.0,
            "concava_arriba": "]1,inf[",
            "punto_min_pen_x": 1.0, "punto_min_pen_y": 20.0
        },
        "p5": {
            "tabla": [
                {"x": 2, "y": 5},
                {"x": 3, "y": 9},
                {"x": 4, "y": 14},
                {"x": 5, "y": 23},
                {"x": 6, "y": 36},
                {"x": 7, "y": 54},
                {"x": 8, "y": 79},
                {"x": 9, "y": 110},
                {"x": 12, "y": 219},
                {"x": 17, "y": 291}
            ],
            "A": 300.0, "B": 150.0, "K": 0.50,
            "max_val": 300.0,
            "inf_x": 10.021, "inf_y": 150.0,
            "max_slope": 37.50
        }
    },
    "Variación 3": {
        "p1": {
            "puntos_enunciado": "A = (-4, -1112), B = (-2, -542), C = (0, 100) \\text{ y } D = (4, 1024)",
            "a": -3.0, "b": -9.0, "c": 315.0, "d": 100.0,
            "valores_criticos": ["-7", "5"],
            "valores_criticos_str": "5 y -7",
            "min_x": -7.0, "min_y": -1517.0,
            "max_x": 5.0, "max_y": 1075.0,
            "inf_x": -1.0, "inf_y": -221.0,
            "intervalo_creciente": "]-7,5["
        },
        "p2": {
            "función_latex": "f(x) = x^3 - 27x + 20",
            "p1_der_cero_opt1": "(3,-34)", "p1_der_cero_opt2": "(-3,74)",
            "p2_der_cero": "(0,20)"
        },
        "p3": {
            "tabla": [
                {"x": 1, "m": "12 + \\frac{10}{5}"},
                {"x": 2, "m": "20 + \\frac{10}{9}"},
                {"x": 3, "m": "28 + \\frac{10}{13}"},
                {"x": 4, "m": "36 + \\frac{10}{17}"},
                {"x": 5, "m": "44 + \\frac{10}{21}"}
            ],
            "exp_m": "8x+4+10/(4x+1)",
            "exp_f": "4x^2+4x+2.5ln(4x+1)+C",
            "v_5": 44.476,
            "a_2": 7.506
        },
        "p4": {
            "función_latex": "f(x) = 100x^3 - 420x^2 + 480x",
            "derivada": "300x^2-840x+480",
            "pendiente_min": 0.0,
            "intervalo_dec": "]0.8,2.0[",
            "max_rel": 166.40,
            "concava_arriba": "]1.4,inf[",
            "punto_min_pen_x": 1.4, "punto_min_pen_y": 123.2
        },
        "p5": {
            "tabla": [
                {"x": 2, "y": 8},
                {"x": 3, "y": 15},
                {"x": 4, "y": 28},
                {"x": 5, "y": 50},
                {"x": 6, "y": 80},
                {"x": 7, "y": 115},
                {"x": 8, "y": 146},
                {"x": 9, "y": 170},
                {"x": 12, "y": 196},
                {"x": 17, "y": 200}
            ],
            "A": 200.0, "B": 100.0, "K": 0.70,
            "max_val": 200.0,
            "inf_x": 6.579, "inf_y": 100.0,
            "max_slope": 35.00
        }
    }
}

# ----------------- INTERFAZ PRINCIPAL DE STREAMLIT -----------------

st.title("📐 Prueba Interactiva de Matemáticas (Cálculo y Álgebra)")
st.caption("Esta plataforma te permite responder a la evaluación interactiva de matemáticas, evaluar tus respuestas y calcular tu calificación de acuerdo a la escala de notas chilena.")

# Panel lateral
with st.sidebar:
    st.header("⚙️ Configuración")
    variacion_sel = st.selectbox(
        "Seleccione la variación de la prueba:",
        options=list(VARIACIONES.keys())
    )
    
    st.subheader("🇨🇱 Parámetros de Calificación")
    exigencia = st.slider(
        "Exigencia de la prueba (%):",
        min_value=50,
        max_value=70,
        value=60,
        step=5
    ) / 100.0
    
    st.info(
        "La escala chilena va de **1.0 a 7.0**. "
        "La nota de aprobación (**4.0**) se obtiene al alcanzar el porcentaje de exigencia configurado."
    )
    
    st.markdown("---")
    st.caption("Desarrollado para Luspa - 2026")

datos = VARIACIONES[variacion_sel]

# Inicializar un diccionario para almacenar las respuestas
respuestas = {}

st.write(f"### Estás rindiendo la **{variacion_sel}** (Puntaje Máximo: 103 Puntos)")

# ==================== PREGUNTA 1 ====================
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">ESTUDIO DE UNA FUNCIÓN DESCONOCIDA (20 puntos)</div>', unsafe_allow_html=True)
    st.write(f"La gráfica de una función f desconocida de grado 3 (cúbica) pasa por los siguientes puntos :")
    st.latex(datos["p1"]["puntos_enunciado"])
    st.write("Conteste:")
    
    # a) Modelo en una sola línea horizontal
    st.markdown('<div class="subquestion-title">a) ¿Cuál es el modelo de la función f ? (4 puntos)</div>', unsafe_allow_html=True)
    col_a1, col_a2, col_a3, col_a4, col_a5, col_a6, col_a7, col_a8, col_a9 = st.columns([2.2, 1.2, 0.8, 1.2, 0.8, 1.2, 0.8, 1.2, 3], vertical_alignment="center")
    with col_a1:
        st.markdown('<div class="inline-text">La función f es = </div>', unsafe_allow_html=True)
    with col_a2:
        respuestas["p1_a"] = st.text_input("", key="p1_a", label_visibility="collapsed")
    with col_a3:
        st.markdown('<div class="inline-text"> x³ + </div>', unsafe_allow_html=True)
    with col_a4:
        respuestas["p1_b"] = st.text_input("", key="p1_b", label_visibility="collapsed")
    with col_a5:
        st.markdown('<div class="inline-text"> x² + </div>', unsafe_allow_html=True)
    with col_a6:
        respuestas["p1_c"] = st.text_input("", key="p1_c", label_visibility="collapsed")
    with col_a7:
        st.markdown('<div class="inline-text"> x + </div>', unsafe_allow_html=True)
    with col_a8:
        respuestas["p1_d"] = st.text_input("", key="p1_d", label_visibility="collapsed")
    with col_a9:
        st.write("")
        
    # b) Valores críticos en una línea horizontal
    st.markdown('<div class="subquestion-title">b) ¿Cuáles son los valores críticos de f ? (4 puntos)</div>', unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([3, 2, 7], vertical_alignment="center")
    with col_b1:
        st.markdown('<div class="inline-text">Los valores críticos son : </div>', unsafe_allow_html=True)
    with col_b2:
        correct_crit_str = datos["p1"]["valores_criticos_str"]
        opciones_b = ["Seleccionar...", correct_crit_str, "4 y -6", "5 y -7", "6 y 8", "-6 y 8"]
        opciones_b = list(dict.fromkeys(opciones_b))
        respuestas["p1_crit_sel"] = st.selectbox("", opciones_b, key="p1_crit_sel", label_visibility="collapsed")
    with col_b3:
        st.write("")

    # c) Mínimo relativo
    st.markdown('<div class="subquestion-title">c) ¿Cuál es el punto mínimo relativo? (2 puntos)</div>', unsafe_allow_html=True)
    col_c1, col_c2, col_c3, col_c4, col_c5, col_c6 = st.columns([3, 0.3, 1.5, 0.3, 1.5, 5.4], vertical_alignment="center")
    with col_c1:
        st.markdown('<div class="inline-text">El punto mínimo relativo es : </div>', unsafe_allow_html=True)
    with col_c2:
        st.markdown('<div class="inline-text"> ( </div>', unsafe_allow_html=True)
    with col_c3:
        respuestas["p1_min_x"] = st.text_input("", key="p1_min_x", label_visibility="collapsed")
    with col_c4:
        st.markdown('<div class="inline-text"> , </div>', unsafe_allow_html=True)
    with col_c5:
        respuestas["p1_min_y"] = st.text_input("", key="p1_min_y", label_visibility="collapsed")
    with col_c6:
        st.markdown('<div class="inline-text"> ) </div>', unsafe_allow_html=True)

    # d) Máximo relativo
    st.markdown('<div class="subquestion-title">d) ¿Cuál es el punto máximo relativo? (2 puntos)</div>', unsafe_allow_html=True)
    col_d1, col_d2, col_d3, col_d4, col_d5, col_d6 = st.columns([3, 0.3, 1.5, 0.3, 1.5, 5.4], vertical_alignment="center")
    with col_d1:
        st.markdown('<div class="inline-text">El punto máximo relativo es : </div>', unsafe_allow_html=True)
    with col_d2:
        st.markdown('<div class="inline-text"> ( </div>', unsafe_allow_html=True)
    with col_d3:
        respuestas["p1_max_x"] = st.text_input("", key="p1_max_x", label_visibility="collapsed")
    with col_d4:
        st.markdown('<div class="inline-text"> , </div>', unsafe_allow_html=True)
    with col_d5:
        respuestas["p1_max_y"] = st.text_input("", key="p1_max_y", label_visibility="collapsed")
    with col_d6:
        st.markdown('<div class="inline-text"> ) </div>', unsafe_allow_html=True)

    # e) Punto de inflexión
    st.markdown('<div class="subquestion-title">e) ¿Cuál es el punto de inflexión de f ? (4 puntos)</div>', unsafe_allow_html=True)
    col_e1, col_e2, col_e3, col_e4, col_e5, col_e6 = st.columns([3, 0.3, 1.5, 0.3, 1.5, 5.4], vertical_alignment="center")
    with col_e1:
        st.markdown('<div class="inline-text">El punto de inflexión es : </div>', unsafe_allow_html=True)
    with col_e2:
        st.markdown('<div class="inline-text"> ( </div>', unsafe_allow_html=True)
    with col_e3:
        respuestas["p1_inf_x"] = st.text_input("", key="p1_inf_x", label_visibility="collapsed")
    with col_e4:
        st.markdown('<div class="inline-text"> , </div>', unsafe_allow_html=True)
    with col_e5:
        respuestas["p1_inf_y"] = st.text_input("", key="p1_inf_y", label_visibility="collapsed")
    with col_e6:
        st.markdown('<div class="inline-text"> ) </div>', unsafe_allow_html=True)

    # f) Intervalo creciente/decreciente
    st.markdown('<div class="subquestion-title">f) ¿En cuál intervalo f es creciente? (4 puntos)</div>', unsafe_allow_html=True)
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([4, 1.5, 0.3, 1.5, 4.7], vertical_alignment="center")
    with col_f1:
        st.markdown('<div class="inline-text"> f es decreciente en el intervalo ] </div>', unsafe_allow_html=True)
    with col_f2:
        respuestas["p1_int1"] = st.text_input("", key="p1_int1", label_visibility="collapsed")
    with col_f3:
        st.markdown('<div class="inline-text"> , </div>', unsafe_allow_html=True)
    with col_f4:
        respuestas["p1_int2"] = st.text_input("", key="p1_int2", label_visibility="collapsed")
    with col_f5:
        st.markdown('<div class="inline-text"> [ </div>', unsafe_allow_html=True)
    
    # AYUDANTE DE PREGUNTA 1
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
Este ejercicio consiste en **interpolación polinómica**. Tienes una función cúbica general de la forma `f(x) = ax³ + bx² + cx + d` y conoces cuatro puntos por los que pasa. Al evaluar la función en cada uno de ellos, obtienes un sistema de 4 ecuaciones lineales con 4 incógnitas (a, b, c, d) que debes resolver.

* **La Derivada (Primera Derivada)**: Mide el ritmo de cambio instantáneo de una función. Gráficamente, representa la **pendiente de la recta tangente** en cualquier punto de la curva.
  * **Cómo afecta**: Si la derivada es positiva, la función sube (es creciente). Si es negativa, la función baja (es decreciente). Si es exactamente cero, la recta tangente es completamente horizontal, indicando la ubicación de los **valores críticos** (donde la curva tiene picos máximos o valles mínimos).
* **La Segunda Derivada**: Es la derivada de la primera derivada. Mide el ritmo al que cambia la pendiente de la curva (es decir, la aceleración de la función).
  * **Cómo afecta**: Determina la **concavidad** de la curva. Si es positiva, la curva se dobla hacia arriba (cóncava hacia arriba). Si es negativa, se dobla hacia abajo (cóncava hacia abajo). Si es exactamente cero y cambia de signo, define el **punto de inflexión** (donde cambia la dirección del doblado de la curva).

### Cómo resolverlo en GeoGebra
1. Ingresa los cuatro puntos dados en la barra de entrada:
   * `A = (-4, -1890)`
   * `B = (-2, -818)`
   * `C = (0, 350)`
   * `D = (5, 2430)`
2. Usa la función de ajuste polinómico escribiendo: `f(x) = Polinomio({A, B, C, D})`. GeoGebra calculará la ecuación exacta.
3. Para los extremos locales (puntos críticos donde la primera derivada es cero), escribe: `Extremo(f)`. Esto marcará los máximos y mínimos relativos en la gráfica.
4. Para el punto de inflexión (donde la segunda derivada es cero), escribe: `PuntoInflexion(f)`.

### Aplicación en la Vida Real
Este concepto se utiliza en el diseño de **montañas rusas o trazados de carreteras**. Los ingenieros conocen puntos clave de paso obligatorios por donde debe ir la vía y usan polinomios de tercer grado para conectar dichos puntos con transiciones suaves, seguras y sin cambios bruscos en las fuerzas gravitacionales experimentadas por los pasajeros.
""")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREGUNTA 2 ====================
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">PUNTOS DE DERIVADA CERO (8 Puntos)</div>', unsafe_allow_html=True)
    
    # a) Primera derivada cero
    st.markdown(f'<div class="subquestion-title">a) ¿En cuál punto de la gráfica de f(x) = {datos["p2"]["función_latex"].split("=")[1]} la función f tiene la primera derivada igual a 0?</div>', unsafe_allow_html=True)
    col_p2a1, col_p2a2, col_p2a3 = st.columns([1.5, 2, 8.5], vertical_alignment="center")
    with col_p2a1:
        st.markdown('<div class="inline-text">En el punto : </div>', unsafe_allow_html=True)
    with col_p2a2:
        opt_der1_1 = datos["p2"]["p1_der_cero_opt1"]
        opt_der1_2 = datos["p2"]["p1_der_cero_opt2"]
        opciones_p2_a = ["Seleccionar...", opt_der1_1, opt_der1_2, "(0,10)", "(1,12)", "(-1,8)"]
        opciones_p2_a = list(dict.fromkeys(opciones_p2_a))
        respuestas["p2_a"] = st.selectbox("", opciones_p2_a, key="p2_a", label_visibility="collapsed")
    with col_p2a3:
        st.write("")
    
    # b) Segunda derivada cero
    st.markdown(f'<div class="subquestion-title">b) ¿En cuál punto de la gráfica de f(x) = {datos["p2"]["función_latex"].split("=")[1]} la función f tiene la segunda derivada igual a 0?</div>', unsafe_allow_html=True)
    col_p2b1, col_p2b2, col_p2b3 = st.columns([1.5, 2, 8.5], vertical_alignment="center")
    with col_p2b1:
        st.markdown('<div class="inline-text">En el punto : </div>', unsafe_allow_html=True)
    with col_p2b2:
        opciones_p2_b = ["Seleccionar...", datos["p2"]["p2_der_cero"], "(1,8)", "(-1,12)", "(0,0)", "(2,15)"]
        opciones_p2_b = list(dict.fromkeys(opciones_p2_b))
        respuestas["p2_b"] = st.selectbox("", opciones_p2_b, key="p2_b", label_visibility="collapsed")
    with col_p2b3:
        st.write("")
    
    # AYUDANTE DE PREGUNTA 2
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
En este ejercicio analizamos cómo las derivadas caracterizan geométricamente a una curva:

* **La Derivada (Primera Derivada)**: Mide el ritmo de cambio instantáneo. Gráficamente, representa la **pendiente de la recta tangente** a la gráfica en cada punto.
  * **Cómo afecta**: Si la derivada es cero, significa que la recta tangente es completamente horizontal. Esto ocurre únicamente en los puntos extremos de la gráfica: los picos superiores (**máximos relativos**) y los valles inferiores (**mínimos relativos**).
* **La Segunda Derivada**: Mide la curvatura o aceleración de la función (el ritmo de cambio de la primera derivada).
  * **Cómo afecta**: Si es cero, indica que la curva no se dobla en ninguna dirección en ese instante. Representa el **punto de inflexión**, el lugar exacto de la gráfica donde la función cambia su curvatura (de cóncava a convexa o viceversa).

### Cómo resolverlo en GeoGebra
1. Escribe la función en la barra de entrada: `f(x) = x³ - 3x + 10` (o usa la correspondiente a tu variación).
2. Para encontrar dónde la primera derivada es cero (los puntos críticos extremos), escribe: `Extremo(f)`. GeoGebra te marcará en la gráfica los puntos correspondientes.
3. Para encontrar dónde la segunda derivada es cero (punto de inflexión), escribe: `PuntoInflexion(f)`.
4. *Alternativa Simbólica (CAS)*: Puedes abrir la vista CAS y escribir `Resolver(f'(x) = 0)` para la primera derivada, y `Resolver(f''(x) = 0)` para la segunda.

### Aplicación en la Vida Real
En **economía y optimización de negocios**, el punto donde la primera derivada es cero permite encontrar la producción exacta para **maximizar los beneficios** o **minimizar los costos operativos**. El punto donde la segunda derivada es cero (punto de inflexión) representa la ley de rendimientos decrecientes: el límite donde invertir más en marketing comienza a ser menos efectivo debido a la saturación.
""")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREGUNTA 3 ====================
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">FUNCIÓN DESCONOCIDA (20 PUNTOS)</div>', unsafe_allow_html=True)
    st.write("La posición de una partícula está representada por una función f desconocida.")
    st.write("La tabla adjunta muestra la pendiente M(x) de la recta tangente a f para algunos valores de x:")
    
    col_tab1, col_tab2 = st.columns([3, 9])
    with col_tab1:
        tabla_md = "| $x$ | $M(x)$ |\n| :---: | :---: |\n"
        for fila in datos["p3"]["tabla"]:
            tabla_md += f"| {fila['x']} | ${fila['m']}$ |\n"
        st.markdown(tabla_md)
    with col_tab2:
        st.write("")
    
    st.write("Sabiendo que M(x) = f'(x), conteste:")
    
    # a) Dropdown
    st.markdown('<div class="subquestion-title">a) ¿Cuál es la expresión algebraica que modela la pendiente M(x)? (5 puntos)</div>', unsafe_allow_html=True)
    col_p3a1, col_p3a2 = st.columns([4, 8], vertical_alignment="center")
    with col_p3a1:
        opt_correct_m = datos["p3"]["exp_m"]
        opciones_p3_a = ["Seleccionar...", opt_correct_m, "5x+3+8/(2x+1)", "8x+4+10/(4x+1)", "6x+4+9/(2x+1)"]
        opciones_p3_a = list(dict.fromkeys(opciones_p3_a))
        respuestas["p3_a"] = st.selectbox("", opciones_p3_a, key="p3_a", label_visibility="collapsed")
    with col_p3a2:
        st.write("")
    
    # b) Dropdown
    st.markdown('<div class="subquestion-title">b) ¿Cuál de las siguientes expresiones algebraicas podría representar a la función f desconocida? (5 puntos)</div>', unsafe_allow_html=True)
    col_p3b1, col_p3b2 = st.columns([4, 8], vertical_alignment="center")
    with col_p3b1:
        opt_f_correcta = datos["p3"]["exp_f"]
        opciones_p3_b = [
            "Seleccionar...",
            opt_f_correcta,
            "3x^2+4x+3ln(3x+1)+C",
            "2.5x^2+3x+4ln(2x+1)+C",
            "4x^2+4x+2.5ln(4x+1)+C"
        ]
        opciones_p3_b = list(dict.fromkeys(opciones_p3_b))
        respuestas["p3_b"] = st.selectbox("", opciones_p3_b, key="p3_b", label_visibility="collapsed")
    with col_p3b2:
        st.write("")
    
    st.markdown("<br><b>INDICACIÓN: INGRESE LOS VALORES EN FORMATO DECIMAL (Redondeo a 3 decimales)</b>", unsafe_allow_html=True)
    st.write("Sabiendo que la velocidad de la partícula es V(x) = f'(x) y la aceleración A(x) = V'(x):")
    
    # c) Velocidad en una línea horizontal
    col_p3c1, col_p3c2, col_p3c3, col_p3c4 = st.columns([3.5, 1.5, 0.6, 6.4], vertical_alignment="center")
    with col_p3c1:
        st.markdown('<div class="inline-text">c) ¿Cuál es la velocidad de la partícula en el instante 5 segundos? (5 puntos)</div>', unsafe_allow_html=True)
    with col_p3c2:
        respuestas["p3_c"] = st.text_input("", key="p3_c", label_visibility="collapsed")
    with col_p3c3:
        st.markdown('<div class="inline-text"> m/s </div>', unsafe_allow_html=True)
    with col_p3c4:
        st.write("")
        
    # d) Aceleración en una línea horizontal
    col_p3d1, col_p3d2, col_p3d3, col_p3d4 = st.columns([3.5, 1.5, 0.6, 6.4], vertical_alignment="center")
    with col_p3d1:
        st.markdown('<div class="inline-text">d) ¿Cuál es la aceleración de la partícula cuando han transcurrido 2 segundos? (5 puntos)</div>', unsafe_allow_html=True)
    with col_p3d2:
        respuestas["p3_d"] = st.text_input("", key="p3_d", label_visibility="collapsed")
    with col_p3d3:
        st.markdown('<div class="inline-text"> m/s² </div>', unsafe_allow_html=True)
    with col_p3d4:
        st.write("")
        
    # AYUDANTE DE PREGUNTA 3
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
En este problema analizamos la relación entre progresiones y cálculo aplicado al movimiento de una partícula:

* **El patrón de la pendiente**: Los valores de `M(x)` muestran una parte lineal y una fraccionaria que siguen una progresión aritmética (primer término + diferencia * (x - 1)). La pendiente es la derivada de la posición: `M(x) = f'(x)`.
* **La Derivada (Velocidad)**: La velocidad instantánea `V(t)` de un objeto es la **primera derivada de su posición** con respecto al tiempo, representando la tasa de cambio de la distancia recorrida.
  * **Cómo afecta**: Si la velocidad es positiva, la partícula avanza; si es negativa, retrocede. Para calcular la velocidad a los 5 segundos, evaluamos directamente la primera derivada en dicho punto (`V(5) = f'(5)`).
* **La Segunda Derivada (Aceleración)**: La aceleración `A(t)` es la tasa de cambio de la velocidad con respecto al tiempo, lo que equivale a la **segunda derivada de la posición** (`A(t) = V'(t) = f''(t)`).
  * **Cómo afecta**: Si la aceleración es positiva, la partícula está acelerando (aumentando su velocidad); si es negativa, está frenando (desacelerando). Para hallarla, derivamos la función de la pendiente `M(x)` y la evaluamos en t = 2.
* **Integración**: Para recuperar la función de posición `f(x)` a partir de su derivada `M(x)`, aplicamos la operación inversa de la derivada, que es la **integral indefinida** (sumando la constante de integración `C`).

### Cómo resolverlo en GeoGebra
1. Define la función de la pendiente en la barra de entrada: `M(x) = 6x + 4 + 9 / (3x + 1)` (o la correspondiente a tu variación).
2. Para encontrar la función de posición `f(x)`, calcula la integral indefinida escribiendo: `Integral(M)`.
3. Para obtener la velocidad a los 5 segundos, evalúa la derivada de forma directa escribiendo: `M(5)`.
4. Para obtener la aceleración a los 2 segundos, calcula la derivada de la pendiente escribiendo: `A(x) = Derivada(M)`, y luego evalúala en 2 escribiendo: `A(2)`.

### Aplicación en la Vida Real
Es la base del funcionamiento de los **sistemas de navegación inercial** en naves espaciales, aviones y teléfonos inteligentes. Los sensores miden de forma continua la aceleración (segunda derivada), la cual se integra una vez para obtener la velocidad (primera derivada) y se integra por segunda vez para calcular la posición exacta del dispositivo en tiempo real.
""")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREGUNTA 4 ====================
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">ESTUDIO DE UNA FUNCIÓN CONOCIDA (30 Puntos)</div>', unsafe_allow_html=True)
    st.write("Considere la siguiente función cúbica:")
    st.latex(datos["p4"]["función_latex"])
    st.write("Conteste las siguientes preguntas:")
    
    # a) Derivada
    st.markdown('<div class="subquestion-title">a) ¿Cuál es la derivada de la función f(x)? (7 puntos)</div>', unsafe_allow_html=True)
    st.caption("Ingrese su resultado como en el siguiente ejemplo: 15x^3-7x^2+4x+5 , sin espacio entre caracteres.")
    col_p4a1, col_p4a2, col_p4a3 = st.columns([1.5, 3, 7.5], vertical_alignment="center")
    with col_p4a1:
        st.markdown('<div class="inline-text">La derivada es : </div>', unsafe_allow_html=True)
    with col_p4a2:
        respuestas["p4_a"] = st.text_input("", key="p4_a", label_visibility="collapsed")
    with col_p4a3:
        st.write("")
    
    # b) Pendiente en mínimo
    st.markdown('<div class="subquestion-title">b) ¿Determine el valor de la pendiente a la recta tangente a f en su punto mínimo relativo? (5 puntos)</div>', unsafe_allow_html=True)
    col_p4b1, col_p4b2, col_p4b3 = st.columns([2.2, 1.5, 8.3], vertical_alignment="center")
    with col_p4b1:
        st.markdown('<div class="inline-text">El valor de la pendiente es : </div>', unsafe_allow_html=True)
    with col_p4b2:
        respuestas["p4_b"] = st.text_input("", key="p4_b", label_visibility="collapsed")
    with col_p4b3:
        st.write("")
    
    # c) Intervalo donde f decrece
    st.markdown('<div class="subquestion-title">c) Encuentre el intervalo donde f decrece. (5 puntos)</div>', unsafe_allow_html=True)
    col_p4c1, col_p4c2, col_p4c3 = st.columns([1.5, 2.5, 8], vertical_alignment="center")
    with col_p4c1:
        st.markdown('<div class="inline-text">El intervalo es: </div>', unsafe_allow_html=True)
    with col_p4c2:
        opt_dec = datos["p4"]["intervalo_dec"]
        opciones_p4_c = ["Seleccionar...", opt_dec, "]0.5,1.5[", "]-inf,0.9[ U ]2.5,inf[", "]1.7,inf[", "]-8,6["]
        opciones_p4_c = list(dict.fromkeys(opciones_p4_c))
        respuestas["p4_c"] = st.selectbox("", opciones_p4_c, key="p4_c", label_visibility="collapsed")
    with col_p4c3:
        st.write("")
        
    # d) Máximo relativo
    st.markdown('<div class="subquestion-title">d) ¿Cuál es el valor máximo relativo de la función f ? (5 puntos)</div>', unsafe_allow_html=True)
    col_p4d1, col_p4d2, col_p4d3 = st.columns([2, 1.5, 8.5], vertical_alignment="center")
    with col_p4d1:
        st.markdown('<div class="inline-text">El máximo relativo es: </div>', unsafe_allow_html=True)
    with col_p4d2:
        respuestas["p4_d"] = st.text_input("", key="p4_d", label_visibility="collapsed")
    with col_p4d3:
        st.write("")
        
    # e) Cóncava arriba
    st.markdown('<div class="subquestion-title">e) ¿En cuál intervalo la función f es cóncava hacia arriba? (4 puntos)</div>', unsafe_allow_html=True)
    col_p4e1, col_p4e2, col_p4e3 = st.columns([1.5, 2.5, 8], vertical_alignment="center")
    with col_p4e1:
        st.markdown('<div class="inline-text">El intervalo es: </div>', unsafe_allow_html=True)
    with col_p4e2:
        opt_conc = datos["p4"]["concava_arriba"]
        opciones_p4_e = ["Seleccionar...", opt_conc, "]1.7,inf[", "]-inf,1.7[", "]0.9,2.5[", "]1.0,inf["]
        opciones_p4_e = list(dict.fromkeys(opciones_p4_e))
        respuestas["p4_e"] = st.selectbox("", opciones_p4_e, key="p4_e", label_visibility="collapsed")
    with col_p4e3:
        st.write("")
        
    # f) Pendiente tangente mínima
    st.markdown('<div class="subquestion-title">f) ¿En cuál punto de la curva f la pendiente de la recta tangente es mínima? (4 puntos)</div>', unsafe_allow_html=True)
    col_p4f1, col_p4f2, col_p4f3, col_p4f4, col_p4f5, col_p4f6 = st.columns([3, 0.3, 1.5, 0.3, 1.5, 5.4], vertical_alignment="center")
    with col_p4f1:
        st.markdown('<div class="inline-text">La pendiente es mínima en el punto : </div>', unsafe_allow_html=True)
    with col_p4f2:
        st.markdown('<div class="inline-text"> ( </div>', unsafe_allow_html=True)
    with col_p4f3:
        respuestas["p4_fx"] = st.text_input("", key="p4_fx", label_visibility="collapsed")
    with col_p4f4:
        st.markdown('<div class="inline-text"> , </div>', unsafe_allow_html=True)
    with col_p4f5:
        respuestas["p4_fy"] = st.text_input("", key="p4_fy", label_visibility="collapsed")
    with col_p4f6:
        st.markdown('<div class="inline-text"> ) </div>', unsafe_allow_html=True)
        
    # AYUDANTE DE PREGUNTA 4
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
En este análisis de una función cúbica conocida aplicamos el estudio de curvas mediante derivadas:

* **La Derivada (Primera Derivada)**: Representa la **pendiente de la recta tangente** en cada punto y mide la velocidad instantánea con la que cambia la función.
  * **Cómo afecta**: Divide el dominio en tramos. Donde la derivada es negativa (`f'(x) < 0`), la función está cayendo (decrece). Donde es positiva (`f'(x) > 0`), la función sube (crece). En los puntos donde cambia de signo, la derivada es cero (`f'(x) = 0`), lo cual corresponde al máximo y mínimo relativo.
* **La Segunda Derivada**: Mide el doblado de la curva (concavidad), es decir, la tasa de cambio de la pendiente.
  * **Cómo afecta**: Si es positiva (`f''(x) > 0`), la curva es cóncava hacia arriba (tiene forma de "U"). Si es negativa, es cóncava hacia abajo. El punto donde la segunda derivada es exactamente cero (`f''(x) = 0`) es el **punto de inflexión**. En una función cúbica, este punto representa también el lugar donde la pendiente de la recta tangente alcanza su **valor mínimo** absoluto.

### Cómo resolverlo en GeoGebra
1. Ingresa la función en la barra de entrada: `f(x) = 360x³ - 1836x² + 2430x` (o la correspondiente).
2. Para calcular la derivada analítica escribe: `Derivada(f)` o simplemente `f'(x)`.
3. Para hallar el intervalo de decrecimiento escribe: `Resolver(f'(x) < 0)`. Obtendrás el intervalo exacto.
4. Para encontrar el valor del máximo relativo escribe: `Extremo(f)` y evalúa las coordenadas del pico.
5. Para la concavidad y el punto de pendiente mínima, escribe: `PuntoInflexion(f)`. La coordenada X de este punto te dará la frontera de la concavidad, y sus coordenadas (X, Y) indican el punto donde la pendiente es mínima.

### Aplicación en la Vida Real
Se utiliza en la **planificación de flujos de caja y liquidez de empresas**. La derivada mide el ritmo de ingresos y egresos de efectivo. El punto de pendiente mínima representa el momento de mayor presión de liquidez (tasa máxima de salida de dinero), fundamental para asegurar que la compañía cuente con las reservas de capital necesarias para afrontar ese instante crítico.
""")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREGUNTA 5 ====================
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">CURVA LOGÍSTICA (25 puntos)</div>', unsafe_allow_html=True)
    st.write("En esta pregunta realice los siguientes pasos:")
    st.write("1).- Dada la tabla adjunta, copie los datos de y (en celeste) en la tabla del geogebra.")
    
    df_p5 = pd.DataFrame(datos["p5"]["tabla"])
    st.table(df_p5.T)
    
    st.write("2).- Manipule los deslizadores para que la curva pase por el centro de los 10 puntos.")
    st.write("Conteste las siguientes preguntas.")
    
    # a, b, c) Deslizadores
    col_p5a1, col_p5a2, col_p5a3 = st.columns([1.5, 1.5, 9], vertical_alignment="center")
    with col_p5a1:
        st.markdown('<div class="inline-text">a) El valor de A es : </div>', unsafe_allow_html=True)
    with col_p5a2:
        respuestas["p5_a"] = st.text_input("", key="p5_a", label_visibility="collapsed")
    with col_p5a3:
        st.markdown('<div class="inline-text"> (3 puntos) </div>', unsafe_allow_html=True)

    col_p5b1, col_p5b2, col_p5b3 = st.columns([1.5, 1.5, 9], vertical_alignment="center")
    with col_p5b1:
        st.markdown('<div class="inline-text">b) El valor de B es : </div>', unsafe_allow_html=True)
    with col_p5b2:
        respuestas["p5_b"] = st.text_input("", key="p5_b", label_visibility="collapsed")
    with col_p5b3:
        st.markdown('<div class="inline-text"> (3 puntos) </div>', unsafe_allow_html=True)

    col_p5c1, col_p5c2, col_p5c3 = st.columns([1.5, 1.5, 9], vertical_alignment="center")
    with col_p5c1:
        st.markdown('<div class="inline-text">c) El valor de K es : </div>', unsafe_allow_html=True)
    with col_p5c2:
        respuestas["p5_k"] = st.text_input("", key="p5_k", label_visibility="collapsed")
    with col_p5c3:
        st.markdown('<div class="inline-text"> (3 puntos) </div>', unsafe_allow_html=True)
        
    # d) C(x) max
    st.markdown('<div class="subquestion-title">d) ¿Cuál es el valor máximo de C(x)? (5 puntos)</div>', unsafe_allow_html=True)
    col_p5d1, col_p5d2, col_p5d3 = st.columns([1.8, 2, 8.2], vertical_alignment="center")
    with col_p5d1:
        st.markdown('<div class="inline-text">El máximo valor es: </div>', unsafe_allow_html=True)
    with col_p5d2:
        opciones_p5_d = ["Seleccionar...", str(int(datos["p5"]["max_val"])), "270", "300", "200", "250"]
        opciones_p5_d = list(dict.fromkeys(opciones_p5_d))
        respuestas["p5_d"] = st.selectbox("", opciones_p5_d, key="p5_d", label_visibility="collapsed")
    with col_p5d3:
        st.write("")
    
    # e) Inflexión curva logística
    st.markdown('<div class="subquestion-title">e) Encuentre el punto de inflexión de la curva. (6 puntos)</div>', unsafe_allow_html=True)
    col_p5e1, col_p5e2, col_p5e3, col_p5e4, col_p5e5, col_p5e6 = st.columns([2, 0.3, 1.5, 0.3, 1.5, 6.4], vertical_alignment="center")
    with col_p5e1:
        st.markdown('<div class="inline-text">El punto de inflexión es: </div>', unsafe_allow_html=True)
    with col_p5e2:
        st.markdown('<div class="inline-text"> ( </div>', unsafe_allow_html=True)
    with col_p5e3:
        respuestas["p5_infx"] = st.text_input("", key="p5_infx", label_visibility="collapsed")
    with col_p5e4:
        st.markdown('<div class="inline-text"> , </div>', unsafe_allow_html=True)
    with col_p5e5:
        respuestas["p5_infy"] = st.text_input("", key="p5_infy", label_visibility="collapsed")
    with col_p5e6:
        st.markdown('<div class="inline-text"> ) </div>', unsafe_allow_html=True)
        
    # f) Pendiente máxima curva logística
    st.markdown('<div class="subquestion-title">f) ¿Cuál es la máxima pendiente de la curva? (5 puntos)</div>', unsafe_allow_html=True)
    col_p5f1, col_p5f2, col_p5f3 = st.columns([2, 1.5, 8.5], vertical_alignment="center")
    with col_p5f1:
        st.markdown('<div class="inline-text">La máxima pendiente es : </div>', unsafe_allow_html=True)
    with col_p5f2:
        respuestas["p5_slope"] = st.text_input("", key="p5_slope", label_visibility="collapsed")
    with col_p5f3:
        st.write("")
    
    # AYUDANTE DE PREGUNTA 5
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
Este problema estudia una **curva de crecimiento logístico**, la cual modela crecimientos acelerados que se topan con límites físicos o ambientales:

* **Parámetro A**: Es el límite superior o **asíntota horizontal** (capacidad de carga máxima) a la que tiende la función cuando el tiempo crece hacia el infinito.
* **Parámetro K**: Controla la velocidad o tasa intrínseca de crecimiento.
* **La Derivada (Velocidad de Crecimiento)**: Representa el ritmo al cual se incrementa la cantidad en cada instante de tiempo.
  * **Cómo afecta**: Al inicio, la velocidad aumenta rápidamente (crecimiento exponencial). Sin embargo, al acercarse al límite `A`, la velocidad disminuye hasta llegar a cero (saturación).
* **Punto de Inflexión (Máxima Derivada)**: Es el punto exacto donde la aceleración es cero (la **segunda derivada es cero**).
  * **Cómo afecta**: Representa el instante de **máxima velocidad de crecimiento** (donde la pendiente de la curva es la más empinada posible). A partir de este punto, el crecimiento continúa, pero cada vez más despacio. En cualquier modelo logístico simétrico, este punto ocurre siempre a la mitad del límite máximo (es decir, en `y = A / 2`) y en `x = ln(B) / K`.

### Cómo resolverlo en GeoGebra
1. Abre la vista de **Hoja de Cálculo** en GeoGebra.
2. Ingresa las dos columnas de datos x e y. Selecciona las celdas, haz clic derecho y selecciona **Crear > Lista de Puntos** para generar la lista (normalmente llamada `l1`).
3. Traza la curva logística que mejor se ajuste a los datos escribiendo: `AjusteLogístico(l1)`. GeoGebra calculará la ecuación de inmediato.
4. Extrae los coeficientes resultantes de la ecuación para identificar A, B y K.
5. Para encontrar las coordenadas del punto de inflexión, escribe: `PuntoInflexion(f)`.
6. Para hallar la máxima pendiente, calcula el valor de la derivada en la coordenada X del punto de inflexión, o utiliza la relación teórica: `pendiente_max = A * K / 4`.

### Aplicación en la Vida Real
Se utiliza en la **propagación de epidemias** (donde el número total de contagiados empieza exponencialmente, alcanza su velocidad máxima en el punto de inflexión y finalmente se estabiliza debido a la inmunidad de rebaño) o en la **penetración de nuevas tecnologías en el mercado** (como la adopción de internet), que se detiene cuando la población total ya cuenta con el servicio.
""")
        
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== BOTÓN DE ENVÍO Y CALIFICACIÓN ====================
st.markdown("---")
btn_calificar = st.button("📝 Enviar Respuestas y Obtener Nota", type="primary", use_container_width=True)

if btn_calificar:
    # ----------------- PROCESAMIENTO Y EVALUACIÓN -----------------
    puntos_obtenidos = 0.0
    detalles = []
    
    # Pregunta 1
    # a) Coeficientes (4 pts: 1 pt c/u)
    p1_a_ok, p1_a_val = validate_numeric(respuestas["p1_a"], datos["p1"]["a"])
    p1_b_ok, p1_b_val = validate_numeric(respuestas["p1_b"], datos["p1"]["b"])
    p1_c_ok, p1_c_val = validate_numeric(respuestas["p1_c"], datos["p1"]["c"])
    p1_d_ok, p1_d_val = validate_numeric(respuestas["p1_d"], datos["p1"]["d"])
    
    p1_a_pts = 1.0 if p1_a_ok else 0.0
    p1_b_pts = 1.0 if p1_b_ok else 0.0
    p1_c_pts = 1.0 if p1_c_ok else 0.0
    p1_d_pts = 1.0 if p1_d_ok else 0.0
    
    detalles.append({"Pregunta": "1.a) Coeficiente a", "Estado": "✅" if p1_a_ok else "❌", "Esperado": datos["p1"]["a"], "Ingresado": respuestas["p1_a"], "Puntos": p1_a_pts})
    detalles.append({"Pregunta": "1.a) Coeficiente b", "Estado": "✅" if p1_b_ok else "❌", "Esperado": datos["p1"]["b"], "Ingresado": respuestas["p1_b"], "Puntos": p1_b_pts})
    detalles.append({"Pregunta": "1.a) Coeficiente c", "Estado": "✅" if p1_c_ok else "❌", "Esperado": datos["p1"]["c"], "Ingresado": respuestas["p1_c"], "Puntos": p1_c_pts})
    detalles.append({"Pregunta": "1.a) Coeficiente d", "Estado": "✅" if p1_d_ok else "❌", "Esperado": datos["p1"]["d"], "Ingresado": respuestas["p1_d"], "Puntos": p1_d_pts})
    puntos_obtenidos += (p1_a_pts + p1_b_pts + p1_c_pts + p1_d_pts)
    
    # b) Valores críticos (4 pts)
    p1_crit_ok = respuestas["p1_crit_sel"] == datos["p1"]["valores_criticos_str"]
    p1_crit_pts = 4.0 if p1_crit_ok else 0.0
    puntos_obtenidos += p1_crit_pts
    detalles.append({"Pregunta": "1.b) Valores críticos de f", "Estado": "✅" if p1_crit_ok else "❌", "Esperado": datos["p1"]["valores_criticos_str"], "Ingresado": respuestas["p1_crit_sel"], "Puntos": p1_crit_pts})

    # c) Mínimo relativo (2 pts: 1 pt c/u)
    min_x_ok, _ = validate_numeric(respuestas["p1_min_x"], datos["p1"]["min_x"])
    min_y_ok, _ = validate_numeric(respuestas["p1_min_y"], datos["p1"]["min_y"])
    p1_min_pts = (1.0 if min_x_ok else 0.0) + (1.0 if min_y_ok else 0.0)
    puntos_obtenidos += p1_min_pts
    detalles.append({"Pregunta": "1.c) Mínimo relativo X", "Estado": "✅" if min_x_ok else "❌", "Esperado": datos["p1"]["min_x"], "Ingresado": respuestas["p1_min_x"], "Puntos": 1.0 if min_x_ok else 0.0})
    detalles.append({"Pregunta": "1.c) Mínimo relativo Y", "Estado": "✅" if min_y_ok else "❌", "Esperado": datos["p1"]["min_y"], "Ingresado": respuestas["p1_min_y"], "Puntos": 1.0 if min_y_ok else 0.0})

    # d) Máximo relativo (2 pts: 1 pt c/u)
    max_x_ok, _ = validate_numeric(respuestas["p1_max_x"], datos["p1"]["max_x"])
    max_y_ok, _ = validate_numeric(respuestas["p1_max_y"], datos["p1"]["max_y"])
    p1_max_pts = (1.0 if max_x_ok else 0.0) + (1.0 if max_y_ok else 0.0)
    puntos_obtenidos += p1_max_pts
    detalles.append({"Pregunta": "1.d) Máximo relativo X", "Estado": "✅" if max_x_ok else "❌", "Esperado": datos["p1"]["max_x"], "Ingresado": respuestas["p1_max_x"], "Puntos": 1.0 if max_x_ok else 0.0})
    detalles.append({"Pregunta": "1.d) Máximo relativo Y", "Estado": "✅" if max_y_ok else "❌", "Esperado": datos["p1"]["max_y"], "Ingresado": respuestas["p1_max_y"], "Puntos": 1.0 if max_y_ok else 0.0})

    # e) Punto de inflexión (4 pts: 2 pts c/u)
    inf_x_ok, _ = validate_numeric(respuestas["p1_inf_x"], datos["p1"]["inf_x"])
    inf_y_ok, _ = validate_numeric(respuestas["p1_inf_y"], datos["p1"]["inf_y"])
    p1_inf_pts = (2.0 if inf_x_ok else 0.0) + (2.0 if inf_y_ok else 0.0)
    puntos_obtenidos += p1_inf_pts
    detalles.append({"Pregunta": "1.e) Inflexión X", "Estado": "✅" if inf_x_ok else "❌", "Esperado": datos["p1"]["inf_x"], "Ingresado": respuestas["p1_inf_x"], "Puntos": 2.0 if inf_x_ok else 0.0})
    detalles.append({"Pregunta": "1.e) Inflexión Y", "Estado": "✅" if inf_y_ok else "❌", "Esperado": datos["p1"]["inf_y"], "Ingresado": respuestas["p1_inf_y"], "Puntos": 2.0 if inf_y_ok else 0.0})

    # f) Intervalo decreciente (4 pts: 2 pts c/u) - Nota: Valida los extremos del intervalo del decremento
    int1_ok, _ = validate_numeric(respuestas["p1_int1"], float(datos["p1"]["valores_criticos"][0]))
    int2_ok, _ = validate_numeric(respuestas["p1_int2"], float(datos["p1"]["valores_criticos"][1]))
    if not (int1_ok and int2_ok):
        # Intentar al revés
        int1_ok_rev, _ = validate_numeric(respuestas["p1_int1"], float(datos["p1"]["valores_criticos"][1]))
        int2_ok_rev, _ = validate_numeric(respuestas["p1_int2"], float(datos["p1"]["valores_criticos"][0]))
        if int1_ok_rev and int2_ok_rev:
            int1_ok, int2_ok = True, True
            
    p1_int_pts = (2.0 if int1_ok else 0.0) + (2.0 if int2_ok else 0.0)
    puntos_obtenidos += p1_int_pts
    detalles.append({"Pregunta": "1.f) Intervalo de decremento izquierdo", "Estado": "✅" if int1_ok else "❌", "Esperado": f"Uno de {datos['p1']['valores_criticos']}", "Ingresado": respuestas["p1_int1"], "Puntos": 2.0 if int1_ok else 0.0})
    detalles.append({"Pregunta": "1.f) Intervalo de decremento derecho", "Estado": "✅" if int2_ok else "❌", "Esperado": f"Uno de {datos['p1']['valores_criticos']}", "Ingresado": respuestas["p1_int2"], "Puntos": 2.0 if int2_ok else 0.0})

    # Pregunta 2
    # a) Primera derivada cero (4 pts)
    p2_a_ok = (respuestas["p2_a"] == datos["p2"]["p1_der_cero_opt1"]) or (respuestas["p2_a"] == datos["p2"]["p1_der_cero_opt2"])
    p2_a_pts = 4.0 if p2_a_ok else 0.0
    puntos_obtenidos += p2_a_pts
    detalles.append({"Pregunta": "2.a) Pto. Primera Derivada Cero", "Estado": "✅" if p2_a_ok else "❌", "Esperado": f"{datos['p2']['p1_der_cero_opt1']} o {datos['p2']['p1_der_cero_opt2']}", "Ingresado": respuestas["p2_a"], "Puntos": p2_a_pts})
    
    # b) Segunda derivada cero (4 pts)
    p2_b_ok = respuestas["p2_b"] == datos["p2"]["p2_der_cero"]
    p2_b_pts = 4.0 if p2_b_ok else 0.0
    puntos_obtenidos += p2_b_pts
    detalles.append({"Pregunta": "2.b) Pto. Segunda Derivada Cero", "Estado": "✅" if p2_b_ok else "❌", "Esperado": datos["p2"]["p2_der_cero"], "Ingresado": respuestas["p2_b"], "Puntos": p2_b_pts})

    # Pregunta 3
    # a) Expresión M(x) (5 pts)
    p3_a_ok = validate_string(respuestas["p3_a"], datos["p3"]["exp_m"])
    p3_a_pts = 5.0 if p3_a_ok else 0.0
    puntos_obtenidos += p3_a_pts
    detalles.append({"Pregunta": "3.a) Expresión de M(x)", "Estado": "✅" if p3_a_ok else "❌", "Esperado": datos["p3"]["exp_m"], "Ingresado": respuestas["p3_a"], "Puntos": p3_a_pts})

    # b) Expresión f(x) (5 pts)
    p3_b_ok = respuestas["p3_b"] == datos["p3"]["exp_f"]
    p3_b_pts = 5.0 if p3_b_ok else 0.0
    puntos_obtenidos += p3_b_pts
    detalles.append({"Pregunta": "3.b) Expresión f(x)", "Estado": "✅" if p3_b_ok else "❌", "Esperado": datos["p3"]["exp_f"], "Ingresado": respuestas["p3_b"], "Puntos": p3_b_pts})

    # c) Velocidad en t=5 (5 pts)
    p3_c_ok, _ = validate_numeric(respuestas["p3_c"], datos["p3"]["v_5"], tolerance=0.005)
    p3_c_pts = 5.0 if p3_c_ok else 0.0
    puntos_obtenidos += p3_c_pts
    detalles.append({"Pregunta": "3.c) Velocidad en t=5", "Estado": "✅" if p3_c_ok else "❌", "Esperado": datos["p3"]["v_5"], "Ingresado": respuestas["p3_c"], "Puntos": p3_c_pts})

    # d) Aceleración en t=2 (5 pts)
    p3_d_ok, _ = validate_numeric(respuestas["p3_d"], datos["p3"]["a_2"], tolerance=0.005)
    p3_d_pts = 5.0 if p3_d_ok else 0.0
    puntos_obtenidos += p3_d_pts
    detalles.append({"Pregunta": "3.d) Aceleración en t=2", "Estado": "✅" if p3_d_ok else "❌", "Esperado": datos["p3"]["a_2"], "Ingresado": respuestas["p3_d"], "Puntos": p3_d_pts})

    # Pregunta 4
    # a) Derivada (7 pts)
    p4_a_ok = validate_string(respuestas["p4_a"], datos["p4"]["derivada"])
    p4_a_pts = 7.0 if p4_a_ok else 0.0
    puntos_obtenidos += p4_a_pts
    detalles.append({"Pregunta": "4.a) Derivada f'(x)", "Estado": "✅" if p4_a_ok else "❌", "Esperado": datos["p4"]["derivada"], "Ingresado": respuestas["p4_a"], "Puntos": p4_a_pts})

    # b) Pendiente en mínimo (5 pts)
    p4_b_ok, _ = validate_numeric(respuestas["p4_b"], datos["p4"]["pendiente_min"])
    p4_b_pts = 5.0 if p4_b_ok else 0.0
    puntos_obtenidos += p4_b_pts
    detalles.append({"Pregunta": "4.b) Pendiente en mínimo", "Estado": "✅" if p4_b_ok else "❌", "Esperado": datos["p4"]["pendiente_min"], "Ingresado": respuestas["p4_b"], "Puntos": p4_b_pts})

    # c) Intervalo decreciente (5 pts)
    p4_c_ok = respuestas["p4_c"] == datos["p4"]["intervalo_dec"]
    p4_c_pts = 5.0 if p4_c_ok else 0.0
    puntos_obtenidos += p4_c_pts
    detalles.append({"Pregunta": "4.c) Intervalo Decreciente", "Estado": "✅" if p4_c_ok else "❌", "Esperado": datos["p4"]["intervalo_dec"], "Ingresado": respuestas["p4_c"], "Puntos": p4_c_pts})

    # d) Máximo relativo (5 pts)
    p4_d_ok, _ = validate_numeric(respuestas["p4_d"], datos["p4"]["max_rel"], tolerance=0.1)
    p4_d_pts = 5.0 if p4_d_ok else 0.0
    puntos_obtenidos += p4_d_pts
    detalles.append({"Pregunta": "4.d) Máximo relativo", "Estado": "✅" if p4_d_ok else "❌", "Esperado": datos["p4"]["max_rel"], "Ingresado": respuestas["p4_d"], "Puntos": p4_d_pts})

    # e) Intervalo concavidad (4 pts)
    p4_e_ok = respuestas["p4_e"] == datos["p4"]["concava_arriba"]
    p4_e_pts = 4.0 if p4_e_ok else 0.0
    puntos_obtenidos += p4_e_pts
    detalles.append({"Pregunta": "4.e) Intervalo cóncava arriba", "Estado": "✅" if p4_e_ok else "❌", "Esperado": datos["p4"]["concava_arriba"], "Ingresado": respuestas["p4_e"], "Puntos": p4_e_pts})

    # f) Punto de pendiente mínima (4 pts: 2 pts c/u)
    p4_fx_ok, _ = validate_numeric(respuestas["p4_fx"], datos["p4"]["punto_min_pen_x"])
    p4_fy_ok, _ = validate_numeric(respuestas["p4_fy"], datos["p4"]["punto_min_pen_y"], tolerance=0.1)
    p4_f_pts = (2.0 if p4_fx_ok else 0.0) + (2.0 if p4_fy_ok else 0.0)
    puntos_obtenidos += p4_f_pts
    detalles.append({"Pregunta": "4.f) Punto Pendiente Mínima X", "Estado": "✅" if p4_fx_ok else "❌", "Esperado": datos["p4"]["punto_min_pen_x"], "Ingresado": respuestas["p4_fx"], "Puntos": 2.0 if p4_fx_ok else 0.0})
    detalles.append({"Pregunta": "4.f) Punto Pendiente Mínima Y", "Estado": "✅" if p4_fy_ok else "❌", "Esperado": datos["p4"]["punto_min_pen_y"], "Ingresado": respuestas["p4_fy"], "Puntos": 2.0 if p4_fy_ok else 0.0})

    # Pregunta 5
    # a) Valor A (3 pts)
    p5_a_ok, _ = validate_numeric(respuestas["p5_a"], datos["p5"]["A"], tolerance=2.0)
    p5_a_pts = 3.0 if p5_a_ok else 0.0
    puntos_obtenidos += p5_a_pts
    detalles.append({"Pregunta": "5.a) Deslizador A", "Estado": "✅" if p5_a_ok else "❌", "Esperado": datos["p5"]["A"], "Ingresado": respuestas["p5_a"], "Puntos": p5_a_pts})

    # b) Valor B (3 pts)
    p5_b_ok, _ = validate_numeric(respuestas["p5_b"], datos["p5"]["B"], tolerance=2.0)
    p5_b_pts = 3.0 if p5_b_ok else 0.0
    puntos_obtenidos += p5_b_pts
    detalles.append({"Pregunta": "5.b) Deslizador B", "Estado": "✅" if p5_b_ok else "❌", "Esperado": datos["p5"]["B"], "Ingresado": respuestas["p5_b"], "Puntos": p5_b_pts})

    # c) Valor K (3 pts)
    p5_k_ok, _ = validate_numeric(respuestas["p5_k"], datos["p5"]["K"], tolerance=0.03)
    p5_k_pts = 3.0 if p5_k_ok else 0.0
    puntos_obtenidos += p5_k_pts
    detalles.append({"Pregunta": "5.c) Deslizador K", "Estado": "✅" if p5_k_ok else "❌", "Esperado": datos["p5"]["K"], "Ingresado": respuestas["p5_k"], "Puntos": p5_k_pts})

    # d) Valor máximo C(x) (5 pts)
    p5_d_ok = respuestas["p5_d"] == str(int(datos["p5"]["max_val"]))
    p5_d_pts = 5.0 if p5_d_ok else 0.0
    puntos_obtenidos += p5_d_pts
    detalles.append({"Pregunta": "5.d) Máximo valor C(x)", "Estado": "✅" if p5_d_ok else "❌", "Esperado": str(int(datos["p5"]["max_val"])), "Ingresado": respuestas["p5_d"], "Puntos": p5_d_pts})

    # e) Punto de inflexión (6 pts: 3 pts c/u)
    p5_infx_ok, _ = validate_numeric(respuestas["p5_infx"], datos["p5"]["inf_x"], tolerance=0.05)
    p5_infy_ok, _ = validate_numeric(respuestas["p5_infy"], datos["p5"]["inf_y"], tolerance=1.0)
    p5_inf_pts = (3.0 if p5_infx_ok else 0.0) + (3.0 if p5_infy_ok else 0.0)
    puntos_obtenidos += p5_inf_pts
    detalles.append({"Pregunta": "5.e) Inflexión X", "Estado": "✅" if p5_infx_ok else "❌", "Esperado": datos["p5"]["inf_x"], "Ingresado": respuestas["p5_infx"], "Puntos": 3.0 if p5_infx_ok else 0.0})
    detalles.append({"Pregunta": "5.e) Inflexión Y", "Estado": "✅" if p5_infy_ok else "❌", "Esperado": datos["p5"]["inf_y"], "Ingresado": respuestas["p5_infy"], "Puntos": 3.0 if p5_infy_ok else 0.0})

    # f) Máxima pendiente (5 pts)
    p5_slope_ok, _ = validate_numeric(respuestas["p5_slope"], datos["p5"]["max_slope"], tolerance=0.5)
    p5_slope_pts = 5.0 if p5_slope_ok else 0.0
    puntos_obtenidos += p5_slope_pts
    detalles.append({"Pregunta": "5.f) Máxima pendiente", "Estado": "✅" if p5_slope_ok else "❌", "Esperado": datos["p5"]["max_slope"], "Ingresado": respuestas["p5_slope"], "Puntos": p5_slope_pts})

    # Calcular Calificación Final
    max_puntos = 103.0
    nota_final = calcular_nota(puntos_obtenidos, max_puntos, exigencia)
    
    # ----------------- RENDERIZAR RESULTADOS -----------------
    st.markdown("## 📊 Calificación e Informe de Resultados")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Puntaje Obtenido</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{puntos_obtenidos:.1f} / {max_puntos}</div>', unsafe_allow_html=True)
        pct = (puntos_obtenidos / max_puntos) * 100
        st.markdown(f"**Porcentaje de Logro:** {pct:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_res2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Nota Final</div>', unsafe_allow_html=True)
        nota_style = "nota-aprobado" if nota_final >= 4.0 else "nota-reprobado"
        st.markdown(f'<div class="chilean-nota {nota_style}">{nota_final:.1f}</div>', unsafe_allow_html=True)
        
        status_msg = "🏆 ¡Aprobado!" if nota_final >= 4.0 else "🔴 Reprobado"
        st.markdown(f"### {status_msg}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_res3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Exigencia Aplicada</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{exigencia*100:.0f}%</div>', unsafe_allow_html=True)
        puntaje_min_aprobacion = exigencia * max_puntos
        st.markdown(f"**Puntaje Mínimo para 4.0:** {puntaje_min_aprobacion:.1f} Pts")
        st.markdown('</div>', unsafe_allow_html=True)

    if nota_final >= 4.0:
        st.balloons()
        st.success("¡Felicidades! Has aprobado la evaluación con éxito.")
    else:
        st.error("No has alcanzado la nota mínima de aprobación (4.0). ¡Sigue practicando!")

    # Mostrar la tabla de detalles
    st.markdown("### 📋 Desglose Detallado por Pregunta")
    df_detalles = pd.DataFrame(detalles)
    st.dataframe(
        df_detalles,
        column_config={
            "Pregunta": st.column_config.TextColumn("Pregunta/Concepto", width="large"),
            "Estado": st.column_config.TextColumn("Estado", width="small"),
            "Esperado": st.column_config.TextColumn("Valor Correcto (Esperado)"),
            "Ingresado": st.column_config.TextColumn("Tu Respuesta"),
            "Puntos": st.column_config.NumberColumn("Puntos Obtenidos", format="%.1f")
        },
        use_container_width=True,
        hide_index=True
    )
