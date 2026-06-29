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
        margin-top: 10px;
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
    st.markdown('<div class="question-title">1. ESTUDIO DE UNA FUNCIÓN DESCONOCIDA (20 Puntos)</div>', unsafe_allow_html=True)
    st.write(f"La gráfica de una función $f$ desconocida de grado 3 (cúbica) pasa por los siguientes puntos:")
    st.latex(datos["p1"]["puntos_enunciado"])
    st.write("Conteste:")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        respuestas["p1_a"] = st.text_input("Coef. a ($x^3$):", key="p1_a", placeholder="Ej: -4")
    with col2:
        respuestas["p1_b"] = st.text_input("Coef. b ($x^2$):", key="p1_b", placeholder="Ej: -12")
    with col3:
        respuestas["p1_c"] = st.text_input("Coef. c ($x$):", key="p1_c", placeholder="Ej: 576")
    with col4:
        respuestas["p1_d"] = st.text_input("Coef. d (const.):", key="p1_d", placeholder="Ej: 350")
        
    st.markdown('<div class="subquestion-title">b) ¿Cuáles son los valores críticos de $f$? (4 Puntos)</div>', unsafe_allow_html=True)
    col_crit1, col_crit2 = st.columns(2)
    with col_crit1:
        respuestas["p1_crit1"] = st.text_input("Primer valor crítico:", key="p1_crit1", placeholder="Ej: 6")
    with col_crit2:
        respuestas["p1_crit2"] = st.text_input("Segundo valor crítico:", key="p1_crit2", placeholder="Ej: -8")
        
    st.markdown('<div class="subquestion-title">c) ¿Cuál es el punto mínimo relativo? (2 Puntos)</div>', unsafe_allow_html=True)
    col_min_x, col_min_y = st.columns(2)
    with col_min_x:
        respuestas["p1_min_x"] = st.text_input("Mínimo relativo (Coordenada X):", key="p1_min_x", placeholder="Ej: -8")
    with col_min_y:
        respuestas["p1_min_y"] = st.text_input("Mínimo relativo (Coordenada Y):", key="p1_min_y", placeholder="Ej: -2978")

    st.markdown('<div class="subquestion-title">d) ¿Cuál es el punto máximo relativo? (2 Puntos)</div>', unsafe_allow_html=True)
    col_max_x, col_max_y = st.columns(2)
    with col_max_x:
        respuestas["p1_max_x"] = st.text_input("Máximo relativo (Coordenada X):", key="p1_max_x", placeholder="Ej: 6")
    with col_max_y:
        respuestas["p1_max_y"] = st.text_input("Máximo relativo (Coordenada Y):", key="p1_max_y", placeholder="Ej: 2510")

    st.markdown('<div class="subquestion-title">e) ¿Cuál es el punto de inflexión de $f$? (4 Puntos)</div>', unsafe_allow_html=True)
    col_inf_x, col_inf_y = st.columns(2)
    with col_inf_x:
        respuestas["p1_inf_x"] = st.text_input("Inflexión (Coordenada X):", key="p1_inf_x", placeholder="Ej: -1")
    with col_inf_y:
        respuestas["p1_inf_y"] = st.text_input("Inflexión (Coordenada Y):", key="p1_inf_y", placeholder="Ej: -234")

    st.markdown('<div class="subquestion-title">f) ¿En cuál intervalo $f$ es creciente? (4 Puntos)</div>', unsafe_allow_html=True)
    respuestas["p1_intervalo"] = st.text_input("Intervalo (ej: ]-8,6[ o (-8,6)):", key="p1_intervalo", placeholder="Ej: ]-8,6[")
    
    # AYUDANTE DE PREGUNTA 1
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
        <div class="helper-box">
            <h4>🧠 Razonamiento Pedagógico</h4>
            <p>Este ejercicio consiste en <strong>interpolación polinómica</strong>. Tienes una función cúbica general de la forma <code>f(x) = ax³ + bx² + cx + d</code> y conoces cuatro puntos por los que pasa. Al evaluar la función en cada punto, obtienes un sistema de 4 ecuaciones lineales con 4 incógnitas (a, b, c, d) que debes resolver. Una vez determinados los coeficientes, utilizas la primera derivada (<code>f'(x) = 0</code>) para encontrar los valores críticos y los máximos y mínimos, y la segunda derivada (<code>f''(x) = 0</code>) para el punto de inflexión.</p>
            
            <h4>🛠️ Cómo resolverlo en GeoGebra</h4>
            <ol>
                <li>Ingresa los cuatro puntos dados en la barra de entrada, por ejemplo: <br><code>A = (-4, -1890)</code>, <code>B = (-2, -818)</code>, <code>C = (0, 350)</code> y <code>D = (5, 2430)</code>.</li>
                <li>Usa la función de ajuste polinómico escribiendo: <br><code>f(x) = Polinomio({A, B, C, D})</code>. GeoGebra calculará la ecuación exacta.</li>
                <li>Para los extremos locales (puntos críticos), escribe: <br><code>Extremo(f)</code>. Esto marcará los máximos y mínimos relativos en la gráfica.</li>
                <li>Para el punto de inflexión, escribe: <br><code>PuntoInflexion(f)</code>.</li>
                <li>Para ver visualmente dónde es creciente, observa los intervalos de la gráfica que suben de izquierda a derecha (entre el mínimo y el máximo).</li>
            </ol>
            
            <h4>🌍 Aplicación en la Vida Real</h4>
            <p>Este concepto se utiliza en el diseño de <strong>montañas rusas o trazados de carreteras</strong>. Los ingenieros conocen puntos clave de paso obligatorios por donde debe ir la vía y usan polinomios de tercer grado para conectar dichos puntos con transiciones suaves, seguras y sin saltos bruscos en las fuerzas gravitacionales.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREGUNTA 2 ====================
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">2. PUNTOS DE DERIVADA CERO (8 Puntos)</div>', unsafe_allow_html=True)
    st.write("Considere la función:")
    st.latex(datos["p2"]["función_latex"])
    
    st.markdown('<div class="subquestion-title">a) ¿En cuál punto de la gráfica la función $f$ tiene la primera derivada igual a 0? (4 Puntos)</div>', unsafe_allow_html=True)
    opt_der1_1 = datos["p2"]["p1_der_cero_opt1"]
    opt_der1_2 = datos["p2"]["p1_der_cero_opt2"]
    opciones_p2_a = ["Seleccionar...", opt_der1_1, opt_der1_2, "(0,10)", "(1,12)", "(-1,8)"]
    respuestas["p2_a"] = st.selectbox("Seleccione el punto:", opciones_p2_a, key="p2_a")
    
    st.markdown('<div class="subquestion-title">b) ¿En cuál punto de la gráfica la función $f$ tiene la segunda derivada igual a 0? (4 Puntos)</div>', unsafe_allow_html=True)
    opciones_p2_b = ["Seleccionar...", datos["p2"]["p2_der_cero"], "(1,8)", "(-1,12)", "(0,0)", "(2,15)"]
    respuestas["p2_b"] = st.selectbox("Seleccione el punto:", opciones_p2_b, key="p2_b")
    
    # AYUDANTE DE PREGUNTA 2
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
        <div class="helper-box">
            <h4>🧠 Razonamiento Pedagógico</h4>
            <p>La <strong>primera derivada</strong> mide la pendiente de la recta tangente. Si es igual a 0, significa que la curva tiene rectas tangentes completamente horizontales. Esto sucede únicamente en los <strong>picos (máximos)</strong> o <strong>valles (mínimos)</strong> de la función. La <strong>segunda derivada</strong> mide la concavidad (curvatura). Si es igual a 0, representa el <strong>punto de inflexión</strong>, que es donde la función cambia su curvatura (de doblarse hacia abajo a doblarse hacia arriba, o viceversa).</p>
            
            <h4>🛠️ Cómo resolverlo en GeoGebra</h4>
            <ol>
                <li>Ingresa la función en la barra de entrada: <br><code>f(x) = x³ - 3x + 10</code> (usa la fórmula correspondiente a tu variación).</li>
                <li>Para hallar dónde la primera derivada es cero (extremos relativos), escribe: <br><code>Extremo(f)</code>. GeoGebra te indicará las coordenadas de los máximos y mínimos.</li>
                <li>Para hallar dónde la segunda derivada es cero, escribe: <br><code>PuntoInflexion(f)</code>. Obtendrás las coordenadas del punto de inflexión.</li>
                <li><em>Alternativa simbólica (Vista CAS):</em> Puedes resolver directamente escribiendo <code>Resolver(f'(x) = 0)</code> para la primera parte, y <code>Resolver(f''(x) = 0)</code> para la segunda.</li>
            </ol>
            
            <h4>🌍 Aplicación en la Vida Real</h4>
            <p>En <strong>economía y optimización de negocios</strong>, el punto de primera derivada cero te permite encontrar la producción exacta para <strong>maximizar los ingresos</strong> o <strong>minimizar los costos</strong>. El punto de segunda derivada cero (punto de inflexión) representa la ley de rendimientos decrecientes: el punto exacto donde la efectividad de una campaña publicitaria comienza a saturarse.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREGUNTA 3 ====================
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">3. FUNCIÓN DESCONOCIDA (20 Puntos)</div>', unsafe_allow_html=True)
    st.write("La posición de una partícula está representada por una función $f$ desconocida.")
    st.write("La tabla adjunta muestra la pendiente $M(x)$ de la recta tangente a $f$ para algunos valores de $x$:")
    
    df_p3 = pd.DataFrame(datos["p3"]["tabla"])
    st.table(df_p3.set_index("x").T)
    
    st.write("Sabiendo que $M(x) = f'(x)$, conteste:")
    
    st.markdown('<div class="subquestion-title">a) ¿Cuál es la expresión algebraica que modela la pendiente $M(x)$? (5 Puntos)</div>', unsafe_allow_html=True)
    respuestas["p3_a"] = st.text_input("Expresión de M(x) (sin espacios, ej: 6x+4+9/(3x+1)):", key="p3_a")
    
    st.markdown('<div class="subquestion-title">b) ¿Cuál de las siguientes expresiones algebraicas podría representar a la función $f$ desconocida? (5 Puntos)</div>', unsafe_allow_html=True)
    opt_f_correcta = datos["p3"]["exp_f"]
    opciones_p3_b = [
        "Seleccionar...",
        opt_f_correcta,
        opt_f_correcta.replace("3x^2", "6x^2").replace("3ln", "9ln").replace("2.5x^2", "5x^2").replace("4x^2", "8x^2"),
        opt_f_correcta.replace("4x", "2x").replace("+C", ""),
        "3x^2 + 4x + ln(3x+1) + C"
    ]
    opciones_p3_b = list(dict.fromkeys(opciones_p3_b))
    respuestas["p3_b"] = st.selectbox("Seleccione la función f(x):", opciones_p3_b, key="p3_b")
    
    st.markdown("**INDICACIÓN: INGRESE LOS VALORES EN FORMATO DECIMAL (Redondeo a 3 decimales)**")
    st.write("Sabiendo que la velocidad de la partícula es $V(x) = f'(x)$ y la aceleración $A(x) = V'(x)$:")
    
    col_v, col_a = st.columns(2)
    with col_v:
        respuestas["p3_c"] = st.text_input("c) ¿Cuál es la velocidad en t = 5 segundos? (5 Puntos)", key="p3_c", placeholder="Ej: 34.563")
    with col_a:
        respuestas["p3_d"] = st.text_input("d) ¿Cuál es la aceleración en t = 2 segundos? (5 Puntos)", key="p3_d", placeholder="Ej: 5.449")
        
    # AYUDANTE DE PREGUNTA 3
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
        <div class="helper-box">
            <h4>🧠 Razonamiento Pedagógico</h4>
            <p>Se te da una tabla con valores de la derivada <code>f'(x) = M(x)</code>. Debes descubrir la regla general (el patrón) en los números: verás una parte lineal y una parte con fracciones. Ambas siguen una <strong>progresión aritmética</strong> simple (primer término + diferencia * (x - 1)). Para encontrar <code>f(x)</code>, debes <strong>integrar</strong> la función de la pendiente. Para velocidad y aceleración: la velocidad es la derivada del espacio (o sea, <code>V(t) = f'(t) = M(t)</code>) y la aceleración es la derivada de la velocidad (<code>A(t) = M'(t)</code>).</p>
            
            <h4>🛠️ Cómo resolverlo en GeoGebra</h4>
            <ol>
                <li>Define la función de la pendiente en la entrada usando la fórmula deducida:<br><code>M(x) = 6x + 4 + 9 / (3x + 1)</code> (o la correspondiente a tu variación).</li>
                <li>Para hallar <code>f(x)</code> (la integral), escribe en la entrada: <br><code>Integral(M)</code>. GeoGebra calculará la primitiva simbólicamente agregando una constante.</li>
                <li>Para obtener la velocidad en t = 5, solo tienes que evaluar la pendiente en 5. Escribe:<br><code>M(5)</code>. Cambia la vista a decimal para ver el resultado con 3 decimales.</li>
                <li>Para obtener la aceleración en t = 2, calcula la derivada de la velocidad escribiendo: <br><code>A(x) = Derivada(M)</code> y luego evalúa la aceleración con: <br><code>A(2)</code>.</li>
            </ol>
            
            <h4>🌍 Aplicación en la Vida Real</h4>
            <p>Este análisis es el pilar de la <strong>navegación inercial</strong>. Los teléfonos móviles o los sistemas de guiado de los cohetes espaciales usan sensores (acelerómetros) que miden la aceleración de forma continua. Integrando esa aceleración una vez obtienen la velocidad, e integrándola por segunda vez calculan la posición exacta del vehículo.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREGUNTA 4 ====================
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">4. ESTUDIO DE UNA FUNCIÓN CONOCIDA (30 Puntos)</div>', unsafe_allow_html=True)
    st.write("Considere la siguiente función cúbica:")
    st.latex(datos["p4"]["función_latex"])
    st.write("Conteste:")
    
    st.markdown('<div class="subquestion-title">a) ¿Cuál es la derivada de la función $f(x)$? (7 Puntos)</div>', unsafe_allow_html=True)
    st.caption("Ingrese su resultado sin espacios entre caracteres, ej: 1080x^2-3672x+2430")
    respuestas["p4_a"] = st.text_input("La derivada es:", key="p4_a")
    
    st.markdown('<div class="subquestion-title">b) ¿Determine el valor de la pendiente a la recta tangente a $f$ en su punto mínimo relativo? (5 Puntos)</div>', unsafe_allow_html=True)
    respuestas["p4_b"] = st.text_input("El valor de la pendiente es:", key="p4_b", placeholder="Ej: 0")
    
    st.markdown('<div class="subquestion-title">c) Encuentre el intervalo donde $f$ decrece. (5 Puntos)</div>', unsafe_allow_html=True)
    opt_dec = datos["p4"]["intervalo_dec"]
    opciones_p4_c = ["Seleccionar...", opt_dec, "]0.5,1.5[", "]-inf,0.9[ U ]2.5,inf[", "]1.7,inf[", "]-8,6["]
    opciones_p4_c = list(dict.fromkeys(opciones_p4_c))
    respuestas["p4_c"] = st.selectbox("El intervalo es:", opciones_p4_c, key="p4_c")
    
    st.markdown('<div class="subquestion-title">d) ¿Cuál es el valor máximo relativo de la función $f$? (5 Puntos)</div>', unsafe_allow_html=True)
    respuestas["p4_d"] = st.text_input("El máximo relativo es:", key="p4_d")
    
    st.markdown('<div class="subquestion-title">e) ¿En cuál intervalo la función $f$ es cóncava hacia arriba? (4 Puntos)</div>', unsafe_allow_html=True)
    opt_conc = datos["p4"]["concava_arriba"]
    opciones_p4_e = ["Seleccionar...", opt_conc, "]1.7,inf[", "]-inf,1.7[", "]0.9,2.5[", "]1.0,inf["]
    opciones_p4_e = list(dict.fromkeys(opciones_p4_e))
    respuestas["p4_e"] = st.selectbox("El intervalo de concavidad es:", opciones_p4_e, key="p4_e")
    
    st.markdown('<div class="subquestion-title">f) ¿En cuál punto de la curva $f$ la pendiente de la recta tangente es mínima? (4 Puntos)</div>', unsafe_allow_html=True)
    col_p4_fx, col_p4_fy = st.columns(2)
    with col_p4_fx:
        respuestas["p4_fx"] = st.text_input("Coordenada X del punto:", key="p4_fx", placeholder="Ej: 1.7")
    with col_p4_fy:
        respuestas["p4_fy"] = st.text_input("Coordenada Y del punto:", key="p4_fy", placeholder="Ej: 593.64")
        
    # AYUDANTE DE PREGUNTA 4
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
        <div class="helper-box">
            <h4>🧠 Razonamiento Pedagógico</h4>
            <p>Se realiza un <strong>análisis completo</strong> de una función cúbica dada:</p>
            <ul>
                <li>La <strong>primera derivada</strong> describe la pendiente: dónde la función crece (<code>f'(x) > 0</code>) y decrece (<code>f'(x) < 0</code>).</li>
                <li>Los puntos máximos y mínimos ocurren cuando la derivada es cero. La pendiente en esos puntos siempre es 0.</li>
                <li>La <strong>segunda derivada</strong> indica la concavidad: cóncava hacia arriba (<code>f''(x) > 0</code>).</li>
                <li>El punto donde la pendiente es mínima coincide con el <strong>punto de inflexión</strong> (donde <code>f''(x) = 0</code>), que es donde la curva cambia de dirección y se vuelve horizontal o empieza a inclinarse en sentido opuesto de la forma más pronunciada.</li>
            </ul>
            
            <h4>🛠️ Cómo resolverlo en GeoGebra</h4>
            <ol>
                <li>Ingresa la función cúbica: <br><code>f(x) = 360x³ - 1836x² + 2430x</code> (o la correspondiente).</li>
                <li>Escribe <code>f'(x)</code> en la entrada para calcular la derivada de forma analítica instantánea.</li>
                <li>Para hallar el intervalo donde decrece, puedes visualizar la gráfica (el tramo que va de bajada entre los extremos) o resolver algebraicamente escribiendo: <br><code>Resolver(f'(x) < 0)</code>.</li>
                <li>Para encontrar el máximo relativo, escribe: <br><code>Extremo(f)</code> y lee las coordenadas del punto pico superior.</li>
                <li>Para la concavidad y el punto de pendiente mínima, escribe: <br><code>PuntoInflexion(f)</code>. La coordenada X define el inicio del intervalo cóncavo hacia arriba (<code>x > X_inflexion</code>) y las coordenadas (X, Y) corresponden al punto de pendiente mínima.</li>
            </ol>
            
            <h4>🌍 Aplicación en la Vida Real</h4>
            <p>Este tipo de análisis se emplea en la <strong>planificación financiera de proyectos</strong>. La derivada indica el ritmo de flujo de caja (pérdida o ganancia de dinero). El punto de pendiente mínima representa el momento crítico de mayor tasa de gasto (punto de máxima presión de liquidez), necesario para dimensionar las reservas monetarias de la empresa.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREGUNTA 5 ====================
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">5. CURVA LOGÍSTICA (25 Puntos)</div>', unsafe_allow_html=True)
    st.write("Dada la tabla adjunta de puntos $(x, y)$:")
    
    df_p5 = pd.DataFrame(datos["p5"]["tabla"])
    st.table(df_p5.T)
    
    st.write("Si manipulamos los deslizadores en Geogebra para que el modelo logístico $C(x) = \\frac{A e^{Kx}}{B + e^{Kx}}$ se ajuste a los 10 puntos:")
    
    col_la, col_lb, col_lk = st.columns(3)
    with col_la:
        respuestas["p5_a"] = st.text_input("a) El valor de A es: (3 Puntos)", key="p5_a", placeholder="Ej: 240")
    with col_lb:
        respuestas["p5_b"] = st.text_input("b) El valor de B es: (3 Puntos)", key="p5_b", placeholder="Ej: 214")
    with col_lk:
        respuestas["p5_k"] = st.text_input("c) El valor de K es: (3 Puntos)", key="p5_k", placeholder="Ej: 0.65")
        
    st.markdown('<div class="subquestion-title">d) ¿Cuál es el valor máximo de $C(x)$? (5 Puntos)</div>', unsafe_allow_html=True)
    opciones_p5_d = ["Seleccionar...", str(int(datos["p5"]["max_val"])), "270", "300", "200", "250"]
    opciones_p5_d = list(dict.fromkeys(opciones_p5_d))
    respuestas["p5_d"] = st.selectbox("El máximo valor es:", opciones_p5_d, key="p5_d")
    
    st.markdown('<div class="subquestion-title">e) Encuentre el punto de inflexión de la curva. (6 Puntos)</div>', unsafe_allow_html=True)
    col_p5_infx, col_p5_infy = st.columns(2)
    with col_p5_infx:
        respuestas["p5_infx"] = st.text_input("Inflexión Coordenada X (Redondeo a 3 decimales):", key="p5_infx", placeholder="Ej: 8.256")
    with col_p5_infy:
        respuestas["p5_infy"] = st.text_input("Inflexión Coordenada Y (Redondeo a 1 decimal):", key="p5_infy", placeholder="Ej: 120.0")
        
    st.markdown('<div class="subquestion-title">f) ¿Cuál es la máxima pendiente de la curva? (5 Puntos)</div>', unsafe_allow_html=True)
    respuestas["p5_slope"] = st.text_input("La máxima pendiente es:", key="p5_slope", placeholder="Ej: 39")
    
    # AYUDANTE DE PREGUNTA 5
    with st.expander("💡 Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
        <div class="helper-box">
            <h4>🧠 Razonamiento Pedagógico</h4>
            <p>La <strong>función logística</strong> modela fenómenos que crecen de manera acelerada (exponencial) al principio, pero que luego se ralentizan debido a restricciones ambientales o físicas, estabilizándose alrededor de un techo o límite.</p>
            <ul>
                <li>El parámetro <strong>A</strong> es la asíntota superior o límite máximo (capacidad de carga).</li>
                <li>El parámetro <strong>K</strong> es la tasa de crecimiento.</li>
                <li>El parámetro <strong>B</strong> define la traslación horizontal de la curva.</li>
                <li>El <strong>punto de inflexión</strong> marca el momento donde el crecimiento deja de acelerar y empieza a desacelerar. Ocurre exactamente en la mitad de la capacidad de carga (<code>y = A / 2</code>) y en la coordenada <code>x = ln(B) / K</code>.</li>
                <li>La <strong>máxima pendiente</strong> (tasa de cambio máxima) ocurre justamente en el punto de inflexión y equivale a la fórmula: <code>pendiente_max = A * K / 4</code>.</li>
            </ul>
            
            <h4>🛠️ Cómo resolverlo en GeoGebra</h4>
            <ol>
                <li>Abre la vista de <strong>Hoja de Cálculo</strong> en GeoGebra.</li>
                <li>Ingresa las dos columnas de datos x e y. Selecciona las celdas, haz clic derecho y selecciona <strong>Crear > Lista de Puntos</strong>. Esto creará una lista llamada <code>l1</code>.</li>
                <li>En la barra de entrada, ejecuta el ajuste logístico automático escribiendo: <br><code>AjusteLogístico(l1)</code> o <code>AjusteCrecimiento(l1)</code>. Esto trazará la curva óptima en pantalla.</li>
                <li>Lee los parámetros resultantes de la ecuación e identifícalos con A, B y K.</li>
                <li>Para hallar el punto de inflexión, escribe: <br><code>PuntoInflexion(f)</code>.</li>
                <li>Para la pendiente máxima, puedes evaluar analíticamente con <code>A * K / 4</code> o calcular la derivada de la curva en el valor de x de la inflexión.</li>
            </ol>
            
            <h4>🌍 Aplicación en la Vida Real</h4>
            <p>Las curvas logísticas son vitales para modelar la <strong>propagación de epidemias</strong> (número total de contagiados que se estabiliza al alcanzar la inmunidad de rebaño) o la <strong>adopción de productos tecnológicos</strong> en el mercado (como los smartphones), que se satura cuando la mayor parte de la población ya los posee.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
    
    # b) Valores críticos (4 pts: 2 pts c/u)
    crit1_ok, crit1_val = validate_numeric(respuestas["p1_crit1"], float(datos["p1"]["valores_criticos"][0]))
    crit2_ok, crit2_val = validate_numeric(respuestas["p1_crit2"], float(datos["p1"]["valores_criticos"][1]))
    if not (crit1_ok and crit2_ok):
        # Intentar al revés
        crit1_ok_rev, _ = validate_numeric(respuestas["p1_crit1"], float(datos["p1"]["valores_criticos"][1]))
        crit2_ok_rev, _ = validate_numeric(respuestas["p1_crit2"], float(datos["p1"]["valores_criticos"][0]))
        if crit1_ok_rev and crit2_ok_rev:
            crit1_ok, crit2_ok = True, True
    
    p1_crit1_pts = 2.0 if crit1_ok else 0.0
    p1_crit2_pts = 2.0 if crit2_ok else 0.0
    puntos_obtenidos += (p1_crit1_pts + p1_crit2_pts)
    detalles.append({"Pregunta": "1.b) Valor Crítico 1", "Estado": "✅" if crit1_ok else "❌", "Esperado": f"Uno de {datos['p1']['valores_criticos']}", "Ingresado": respuestas["p1_crit1"], "Puntos": p1_crit1_pts})
    detalles.append({"Pregunta": "1.b) Valor Crítico 2", "Estado": "✅" if crit2_ok else "❌", "Esperado": f"Uno de {datos['p1']['valores_criticos']}", "Ingresado": respuestas["p1_crit2"], "Puntos": p1_crit2_pts})

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

    # f) Intervalo creciente (4 pts)
    p1_int_ok = validate_string(respuestas["p1_intervalo"], datos["p1"]["intervalo_creciente"])
    p1_int_pts = 4.0 if p1_int_ok else 0.0
    puntos_obtenidos += p1_int_pts
    detalles.append({"Pregunta": "1.f) Intervalo Creciente", "Estado": "✅" if p1_int_ok else "❌", "Esperado": datos["p1"]["intervalo_creciente"], "Ingresado": respuestas["p1_intervalo"], "Puntos": p1_int_pts})

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
