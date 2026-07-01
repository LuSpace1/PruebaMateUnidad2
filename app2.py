import streamlit as st
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Prueba de Cálculo Diferencial - Unidad 2",
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
        background-color: var(--secondary-background-color, #f8fafc);
        color: var(--text-color, #0f172a);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid rgba(128,128,128,0.2);
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 5px;
        color: var(--text-color, #0f172a);
    }
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-color, #64748b);
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .question-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color, #0f172a);
        margin-bottom: 15px;
        border-bottom: 2px solid rgba(2, 132, 199, 0.3);
        padding-bottom: 8px;
    }
    .subquestion-title {
        font-weight: 600;
        color: var(--text-color, #1e293b);
        opacity: 0.95;
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
        background-color: rgba(2, 132, 199, 0.08);
        border: 1px solid rgba(2, 132, 199, 0.3);
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
        color: var(--text-color, #0f172a);
        display: flex;
        align-items: center;
        height: 100%;
        margin-top: 0px;
        padding-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

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

# Inicializar variables de estado en session_state
if "prueba_enviada" not in st.session_state:
    st.session_state["prueba_enviada"] = False
if "respuestas_usuario" not in st.session_state:
    st.session_state["respuestas_usuario"] = {}
if "feedback_respuestas" not in st.session_state:
    st.session_state["feedback_respuestas"] = {}
if "puntos_obtenidos" not in st.session_state:
    st.session_state["puntos_obtenidos"] = 0.0
if "nota_final" not in st.session_state:
    st.session_state["nota_final"] = 1.0
if "detalles" not in st.session_state:
    st.session_state["detalles"] = []

def obtener_flag_subpregunta(key):
    if key in ["p1_t_slope"]:
        return "validada_p1_a"
    elif key in ["p1_n_slope"]:
        return "validada_p1_b"
    elif key in ["p1_eq_t"]:
        return "validada_p1_c"
    elif key in ["p1_eq_n"]:
        return "validada_p1_d"
    elif key in ["p2_slope_c"]:
        return "validada_p2_a"
    elif key in ["p2_eq_d_m", "p2_eq_d_n"]:
        return "validada_p2_b"
    elif key in ["p2_inter_x", "p2_inter_y"]:
        return "validada_p2_c"
    elif key in ["p3_d1_a", "p3_d1_b", "p3_d1_c"]:
        return "validada_p3_a"
    elif key in ["p3_d2_a", "p3_d2_b"]:
        return "validada_p3_b"
    elif key in ["p3_d3"]:
        return "validada_p3_c"
    elif key in ["p4_pt"]:
        return "validada_p4"
    elif key.startswith("p5_row"):
        return "validada_p5_a"
    elif key in ["p5_limit"]:
        return "validada_p5_b"
    return f"validada_{key}"

# Inicializar banderas para validación individual de subpreguntas
subpreguntas_flags = [
    "validada_p1_a", "validada_p1_b", "validada_p1_c", "validada_p1_d",
    "validada_p2_a", "validada_p2_b", "validada_p2_c",
    "validada_p3_a", "validada_p3_b", "validada_p3_c",
    "validada_p4",
    "validada_p5_a", "validada_p5_b"
]

for flag in subpreguntas_flags:
    if flag not in st.session_state:
        st.session_state[flag] = False

def dibujar_feedback(key):
    flag_val = obtener_flag_subpregunta(key)
    if st.session_state.get("prueba_enviada", False) or st.session_state.get(flag_val, False):
        f_data = st.session_state.get("feedback_respuestas", {}).get(key, None)
        if f_data:
            ok = f_data["ok"]
            ingresado = f_data["ingresado"]
            esperado = f_data["esperado"]
            if ok:
                st.markdown(f'<div style="color: #0d9488; font-weight: 600; font-size: 0.8rem; margin-top: 1px; margin-bottom: 2px;">✅ ¡Correcto!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="color: #e11d48; font-weight: 600; font-size: 0.8rem; margin-top: 1px; margin-bottom: 2px;">❌ Incorrecto<br><span style="font-size: 0.72rem; font-weight: normal; opacity: 0.9;">Ingresado: "{ingresado}"<br>Esperado: "{esperado}"</span></div>', unsafe_allow_html=True)

# ----------------- BASE DE DATOS DE VARIACIONES -----------------
VARIACIONES = {
    "Variación 1 (Original)": {
        "p1": {
            "función_latex": "f(x) = 3x + \\frac{4}{x}",
            "x0": 2.0,
            "y0": 8.0,
            "m_t": 2.0,
            "m_n": -0.5,
            "eq_t": "Y = 2X + 4",
            "eq_n": "Y = -0.5X + 9",
            "opts_m_n": ["", "-2.00", "0.50", "-0.50", "2.00"],
            "opts_eq_t": ["", "Y = 2X + 4", "Y = -0.5X + 9", "Y = 2X + 8", "Y = 3X + 2"],
            "opts_eq_n": ["", "Y = -0.5X + 9", "Y = 2X + 4", "Y = -0.5X + 8", "Y = 3X + 2"]
        },
        "p2": {
            "puntos_x": [-2.0, 2.0, 4.0, 6.0, 10.0],
            "puntos_y": [0.0, 4.0, 2.0, 8.0, 6.0],
            "m_c": 0.75,
            "m_d": 4.0,
            "eq_d_m": 4.0,
            "eq_d_n": -16.0,
            "inter_x": 4.62,
            "inter_y": 2.46
        },
        "p3": {
            "función_latex": "f(x) = (5x - 1)^3 - 7x + 9",
            "d1_a": 375.0, "d1_b": -150.0, "d1_c": 8.0,
            "d2_a": 750.0, "d2_b": -150.0,
            "d3": 750.0
        },
        "p4": {
            "función_latex": "f(x) = 2x^4 - 8x",
            "punto_t_horiz": "(1,-6)",
            "opts_pt": ["", "(1,-6)", "(2,24)", "(0,0)", "(1,2)"]
        },
        "p5": {
            "función_latex": "f(x) = x^2 + 6x - 1",
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
    },
    "Variación 2": {
        "p1": {
            "función_latex": "f(x) = 2x + \\frac{9}{x}",
            "x0": 3.0,
            "y0": 9.0,
            "m_t": 1.0,
            "m_n": -1.0,
            "eq_t": "Y = X + 6",
            "eq_n": "Y = -X + 12",
            "opts_m_n": ["", "-1.00", "1.00", "-0.50", "2.00"],
            "opts_eq_t": ["", "Y = X + 6", "Y = -X + 12", "Y = X + 9", "Y = 2X + 3"],
            "opts_eq_n": ["", "Y = -X + 12", "Y = X + 6", "Y = -X + 9", "Y = 2X + 3"]
        },
        "p2": {
            "puntos_x": [-2.0, 1.0, 3.0, 5.0, 8.0],
            "puntos_y": [0.0, 4.0, 3.0, 7.0, 5.0],
            "m_c": 0.5,
            "m_d": 2.0,
            "eq_d_m": 2.0,
            "eq_d_n": -3.0,
            "inter_x": 3.0,
            "inter_y": 3.0
        },
        "p3": {
            "función_latex": "f(x) = (2x - 3)^3 - 4x + 10",
            "d1_a": 24.0, "d1_b": -72.0, "d1_c": 50.0,
            "d2_a": 48.0, "d2_b": -72.0,
            "d3": 48.0
        },
        "p4": {
            "función_latex": "f(x) = x^4 - 32x",
            "punto_t_horiz": "(2,-48)",
            "opts_pt": ["", "(2,-48)", "(1,-31)", "(0,0)", "(2,16)"]
        },
        "p5": {
            "función_latex": "f(x) = x^2 + 4x + 3",
            "x0": -1.0,
            "y0": 0.0,
            "lim_m": 2.0,
            "tabla": [
                {"x": -0.8, "fx": 0.44, "dx": 0.2, "dy": 0.44, "m": 2.2},
                {"x": -0.9, "fx": 0.21, "dx": 0.1, "dy": 0.21, "m": 2.1},
                {"x": -0.99, "fx": 0.0201, "dx": 0.01, "dy": 0.0201, "m": 2.01},
                {"x": -0.999, "fx": 0.002, "dx": 0.001, "dy": 0.002, "m": 2.001},
                {"x": -0.9999, "fx": 0.0002, "dx": 0.0001, "dy": 0.0002, "m": 2.0}
            ]
        }
    },
    "Variación 3": {
        "p1": {
            "función_latex": "f(x) = 4x + \\frac{9}{x}",
            "x0": 3.0,
            "y0": 15.0,
            "m_t": 3.0,
            "m_n": -0.33,
            "eq_t": "Y = 3X + 6",
            "eq_n": "Y = -0.33X + 16",
            "opts_m_n": ["", "-0.33", "3.00", "-3.00", "0.33"],
            "opts_eq_t": ["", "Y = 3X + 6", "Y = -0.33X + 16", "Y = 3X + 15", "Y = X + 12"],
            "opts_eq_n": ["", "Y = -0.33X + 16", "Y = 3X + 6", "Y = -0.33X + 15", "Y = X + 12"]
        },
        "p2": {
            "puntos_x": [-2.0, 2.0, 4.0, 6.0, 9.0],
            "puntos_y": [0.0, 5.0, 3.0, 9.0, 7.0],
            "m_c": 1.0,
            "m_d": 3.0,
            "eq_d_m": 3.0,
            "eq_d_n": -9.0,
            "inter_x": 4.0,
            "inter_y": 3.0
        },
        "p3": {
            "función_latex": "f(x) = (3x - 2)^3 - 5x + 6",
            "d1_a": 81.0, "d1_b": -108.0, "d1_c": 31.0,
            "d2_a": 162.0, "d2_b": -108.0,
            "d3": 162.0
        },
        "p4": {
            "función_latex": "f(x) = 3x^4 - 96x",
            "punto_t_horiz": "(2,-144)",
            "opts_pt": ["", "(2,-144)", "(1,-93)", "(0,0)", "(2,48)"]
        },
        "p5": {
            "función_latex": "f(x) = x^2 + 8x + 5",
            "x0": -3.0,
            "y0": -10.0,
            "lim_m": 2.0,
            "tabla": [
                {"x": -2.8, "fx": -9.56, "dx": 0.2, "dy": 0.44, "m": 2.2},
                {"x": -2.9, "fx": -9.79, "dx": 0.1, "dy": 0.21, "m": 2.1},
                {"x": -2.99, "fx": -9.9799, "dx": 0.01, "dy": 0.0201, "m": 2.01},
                {"x": -2.999, "fx": -9.9979, "dx": 0.001, "dy": 0.002, "m": 2.001},
                {"x": -2.9999, "fx": -9.9998, "dx": 0.0001, "dy": 0.0002, "m": 2.0}
            ]
        }
    }
}

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.title("Prueba de Cálculo")
    st.write("Unidad 2: Rectas Tangentes y Derivadas")
    
    variacion_sel = st.selectbox(
        "Seleccione su Variación de Prueba:",
        list(VARIACIONES.keys()),
        index=0,
        disabled=st.session_state["prueba_enviada"]
    )
    
    st.markdown("---")
    st.markdown("### Escala de Notas")
    st.write("Puntaje Máximo: 73 Puntos")
    st.write("Exigencia: 60%")
    st.write("Aprobación (Nota 4.0): 43.8 Puntos")

# Obtener datos de la variación seleccionada
datos = VARIACIONES[variacion_sel]
respuestas = {}

st.write(f"### Rendimiento de la **{variacion_sel}** (Puntaje Máximo: 73 Puntos)")

# ==================== PREGUNTA 1 ====================
with st.container(border=True):
    st.markdown('<div class="question-title">RECTA TANGENTE Y NORMAL (20 Puntos)</div>', unsafe_allow_html=True)
    st.write("Dada la función:")
    st.latex(datos["p1"]["función_latex"])
    st.write(f"Conteste las siguientes preguntas con respecto a su comportamiento en $x_0 = {int(datos['p1']['x0'])}$:")

    # a) Pendiente de la recta tangente
    st.markdown('<div class="subquestion-title">a) ¿Cuál es la pendiente de la recta tangente a f en x₀ = 2? (3 puntos)</div>', unsafe_allow_html=True)
    col_1a1, col_1a2, col_1a3, col_1a4 = st.columns([3, 2, 2.5, 4.5], vertical_alignment="center")
    with col_1a1:
        st.markdown('<div class="inline-text">La pendiente de la recta tangente es : </div>', unsafe_allow_html=True)
    with col_1a2:
        val_p1_t_slope = st.session_state["respuestas_usuario"].get("p1_t_slope", "")
        respuestas["p1_t_slope"] = st.text_input("", value=val_p1_t_slope, key="p1_t_slope", label_visibility="collapsed")
        dibujar_feedback("p1_t_slope")
    with col_1a3:
        if st.button("🔍 Validar a", key="btn_val_p1_a", use_container_width=True):
            st.session_state["respuestas_usuario"]["p1_t_slope"] = respuestas["p1_t_slope"]
            p1_t_slope_ok, _ = validate_numeric(respuestas["p1_t_slope"], datos["p1"]["m_t"])
            st.session_state["feedback_respuestas"]["p1_t_slope"] = {"ok": p1_t_slope_ok, "ingresado": respuestas["p1_t_slope"], "esperado": datos["p1"]["m_t"]}
            st.session_state["validada_p1_a"] = True
            st.rerun()
    with col_1a4:
        st.write("")

    # b) Pendiente de la recta normal
    st.markdown('<div class="subquestion-title">b) ¿Cuál es la pendiente de la recta normal a f en x₀ = 2? (3 puntos)</div>', unsafe_allow_html=True)
    col_1b1, col_1b2, col_1b3, col_1b4 = st.columns([3, 2, 2.5, 4.5], vertical_alignment="center")
    with col_1b1:
        st.markdown('<div class="inline-text">La pendiente de la recta normal es : </div>', unsafe_allow_html=True)
    with col_1b2:
        val_p1_n_slope = st.session_state["respuestas_usuario"].get("p1_n_slope", "")
        opts = datos["p1"]["opts_m_n"]
        idx = opts.index(val_p1_n_slope) if val_p1_n_slope in opts else 0
        respuestas["p1_n_slope"] = st.selectbox("", opts, index=idx, key="p1_n_slope", label_visibility="collapsed")
        dibujar_feedback("p1_n_slope")
    with col_1b3:
        if st.button("🔍 Validar b", key="btn_val_p1_b", use_container_width=True):
            st.session_state["respuestas_usuario"]["p1_n_slope"] = respuestas["p1_n_slope"]
            p1_n_slope_ok, _ = validate_numeric(respuestas["p1_n_slope"], datos["p1"]["m_n"])
            st.session_state["feedback_respuestas"]["p1_n_slope"] = {"ok": p1_n_slope_ok, "ingresado": respuestas["p1_n_slope"], "esperado": datos["p1"]["m_n"]}
            st.session_state["validada_p1_b"] = True
            st.rerun()
    with col_1b4:
        st.write("")

    # c) Ecuación de la recta tangente
    st.markdown('<div class="subquestion-title">c) ¿Cuál de las siguientes expresiones algebraicas representa la ecuación de la recta tangente a f en x₀ = 2? (7 puntos)</div>', unsafe_allow_html=True)
    col_1c1, col_1c2, col_1c3, col_1c4 = st.columns([3, 2.5, 2.5, 4], vertical_alignment="center")
    with col_1c1:
        st.markdown('<div class="inline-text">La ecuación de la recta tangente es : </div>', unsafe_allow_html=True)
    with col_1c2:
        val_p1_eq_t = st.session_state["respuestas_usuario"].get("p1_eq_t", "")
        opts_t = datos["p1"]["opts_eq_t"]
        idx_t = opts_t.index(val_p1_eq_t) if val_p1_eq_t in opts_t else 0
        respuestas["p1_eq_t"] = st.selectbox("", opts_t, index=idx_t, key="p1_eq_t", label_visibility="collapsed")
        dibujar_feedback("p1_eq_t")
    with col_1c3:
        if st.button("🔍 Validar c", key="btn_val_p1_c", use_container_width=True):
            st.session_state["respuestas_usuario"]["p1_eq_t"] = respuestas["p1_eq_t"]
            p1_eq_t_ok = validate_string(respuestas["p1_eq_t"], datos["p1"]["eq_t"])
            st.session_state["feedback_respuestas"]["p1_eq_t"] = {"ok": p1_eq_t_ok, "ingresado": respuestas["p1_eq_t"], "esperado": datos["p1"]["eq_t"]}
            st.session_state["validada_p1_c"] = True
            st.rerun()
    with col_1c4:
        st.write("")

    # d) Ecuación de la recta normal
    st.markdown('<div class="subquestion-title">d) ¿Cuál de las siguientes expresiones algebraicas representa la ecuación de la recta normal a f en x₀ = 2? (7 puntos)</div>', unsafe_allow_html=True)
    col_1d1, col_1d2, col_1d3, col_1d4 = st.columns([3, 2.5, 2.5, 4], vertical_alignment="center")
    with col_1d1:
        st.markdown('<div class="inline-text">La ecuación de la recta normal es : </div>', unsafe_allow_html=True)
    with col_1d2:
        val_p1_eq_n = st.session_state["respuestas_usuario"].get("p1_eq_n", "")
        opts_n = datos["p1"]["opts_eq_n"]
        idx_n = opts_n.index(val_p1_eq_n) if val_p1_eq_n in opts_n else 0
        respuestas["p1_eq_n"] = st.selectbox("", opts_n, index=idx_n, key="p1_eq_n", label_visibility="collapsed")
        dibujar_feedback("p1_eq_n")
    with col_1d3:
        if st.button("🔍 Validar d", key="btn_val_p1_d", use_container_width=True):
            st.session_state["respuestas_usuario"]["p1_eq_n"] = respuestas["p1_eq_n"]
            p1_eq_n_ok = validate_string(respuestas["p1_eq_n"], datos["p1"]["eq_n"])
            st.session_state["feedback_respuestas"]["p1_eq_n"] = {"ok": p1_eq_n_ok, "ingresado": respuestas["p1_eq_n"], "esperado": datos["p1"]["eq_n"]}
            st.session_state["validada_p1_d"] = True
            st.rerun()
    with col_1d4:
        st.write("")

    with st.expander("Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
En este problema estudiamos cómo obtener la recta tangente y normal a una función en un punto dado:
1. **Pendiente de la Recta Tangente ($m_t$)**: Representa la tasa de cambio instantánea. Se obtiene calculando la primera derivada de la función $f'(x)$ y evaluándola en el punto dado $x_0$, es decir, $m_t = f'(x_0)$.
2. **Pendiente de la Recta Normal ($m_n$)**: La recta normal es perpendicular a la tangente en el punto de tangencia. Su pendiente es el recíproco negativo de la pendiente de la tangente: $m_n = -1 / m_t$.
3. **Ecuaciones de las Rectas**: Utilizamos la fórmula punto-pendiente: $Y - y_0 = m(X - x_0)$, donde $y_0 = f(x_0)$. Despejamos $Y$ para obtener la ecuación explícita de la forma $Y = mX + n$.

### Aplicación Simple en la Vida Real
Este concepto se aplica en el **diseño de faros de vehículos y lentes de cámaras**. La superficie reflectora o el vidrio del lente es la curva matemática. La recta tangente representa la superficie local del lente en un punto específico, mientras que la recta normal (perpendicular) marca la dirección exacta en la que un rayo de luz incide y se refracta (siguiendo la Ley de Snell) para enfocar las imágenes correctamente.

### Guía Paso a Paso en GeoGebra Clásico (Por Literal)
* **Literal a) Pendiente de la recta tangente**
  1. Define la función en la barra de entrada de GeoGebra, por ejemplo: `f(x) = 3x + 4/x`.
  2. Escribe `f'(2)` para calcular de forma directa el valor de la derivada en el punto de interés.
* **Literal b) Pendiente de la recta normal**
  1. Con el valor $m_t$ del literal anterior, escribe en la entrada de GeoGebra `-1 / m_t` (o el valor obtenido).
* **Literal c) Ecuación de la recta tangente**
  1. Escribe el comando: `Tangente(2, f)`. GeoGebra mostrará la recta tangente y su ecuación simplificada.
* **Literal d) Ecuación de la recta normal**
  1. Crea el punto de tangencia escribiendo: `P = (2, f(2))`.
  2. Traza la recta normal escribiendo: `Normal(P, f)`. GeoGebra calculará de inmediato la ecuación explícita.
""")

# ==================== PREGUNTA 2 ====================
with st.container(border=True):
    st.markdown('<div class="question-title">RECTAS TANGENTES DESDE GRÁFICA (15 Puntos)</div>', unsafe_allow_html=True)
    st.write("En la siguiente gráfica se presenta el comportamiento de una función de orden 4 desconocida, indicando las tangentes trazadas en los puntos C y D:")
    
    # Dibujar la gráfica dinámicamente con matplotlib
    fig, ax = plt.subplots(figsize=(8, 4.5))
    pts_x = datos["p2"]["puntos_x"]
    pts_y = datos["p2"]["puntos_y"]
    letras = ["A", "B", "C", "D", "E"]
    
    # Ajuste polinómico de grado 4 para graficar la curva
    coeffs = np.polyfit(pts_x, pts_y, 4)
    poly = np.poly1d(coeffs)
    
    x_curve = np.linspace(-3, 11, 300)
    y_curve = poly(x_curve)
    
    # Graficar curva polinómica
    ax.plot(x_curve, y_curve, color="#e11d48", label="f(x)", linewidth=2.5)
    
    # Graficar puntos clave
    for px, py, letra in zip(pts_x, pts_y, letras):
        ax.plot(px, py, 'o', color="#1e293b", markersize=8)
        ax.text(px - 0.3, py + 0.6, letra, fontsize=11, fontweight='bold', color="black")
        
    # Graficar recta tangente azul (en C)
    m_c = datos["p2"]["m_c"]
    y_azul = m_c * (x_curve - pts_x[2]) + pts_y[2]
    ax.plot(x_curve, y_azul, color="#0284c7", linestyle="-", label="Tangente en C", linewidth=1.5)
    
    # Graficar recta tangente verde (en D)
    m_d = datos["p2"]["m_d"]
    y_verde = m_d * (x_curve - pts_x[3]) + pts_y[3]
    ax.plot(x_curve, y_verde, color="#22c55e", linestyle="-", label="Tangente en D", linewidth=1.5)
    
    # Límites y formato premium de la gráfica
    ax.set_xlim(-3, 11)
    ax.set_ylim(-2, 15)
    ax.grid(True, which='both', linestyle=':', alpha=0.5)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.legend(loc="upper left")
    
    # Mostrar la figura en Streamlit
    st.pyplot(fig)
    
    st.write("INDICACIÓN: Ingrese valores con 2 decimales.")
    
    # a) Pendiente de la recta tangente en C
    st.markdown('<div class="subquestion-title">a) La pendiente de la recta tangente a f en el punto C. (3 puntos)</div>', unsafe_allow_html=True)
    col_2a1, col_2a2, col_2a3, col_2a4 = st.columns([3, 2, 2.5, 4.5], vertical_alignment="center")
    with col_2a1:
        st.markdown('<div class="inline-text">La pendiente en C es : </div>', unsafe_allow_html=True)
    with col_2a2:
        val_p2_slope_c = st.session_state["respuestas_usuario"].get("p2_slope_c", "")
        respuestas["p2_slope_c"] = st.text_input("", value=val_p2_slope_c, key="p2_slope_c", label_visibility="collapsed")
        dibujar_feedback("p2_slope_c")
    with col_2a3:
        if st.button("🔍 Validar a", key="btn_val_p2_a", use_container_width=True):
            st.session_state["respuestas_usuario"]["p2_slope_c"] = respuestas["p2_slope_c"]
            p2_slope_c_ok, _ = validate_numeric(respuestas["p2_slope_c"], datos["p2"]["m_c"], tolerance=0.05)
            st.session_state["feedback_respuestas"]["p2_slope_c"] = {"ok": p2_slope_c_ok, "ingresado": respuestas["p2_slope_c"], "esperado": datos["p2"]["m_c"]}
            st.session_state["validada_p2_a"] = True
            st.rerun()
    with col_2a4:
        st.write("")

    # b) Ecuación de la recta tangente en D
    st.markdown('<div class="subquestion-title">b) La ecuación de la recta tangente a f en el punto D. (6 puntos)</div>', unsafe_allow_html=True)
    col_2b1, col_2b2, col_2b3, col_2b4, col_2b5, col_2b6, col_2b7 = st.columns([2, 1.5, 0.4, 1.5, 2.5, 2.9, 1.2], vertical_alignment="center")
    with col_2b1:
        st.markdown('<div class="inline-text">La ecuación es : Y = </div>', unsafe_allow_html=True)
    with col_2b2:
        val_p2_eq_d_m = st.session_state["respuestas_usuario"].get("p2_eq_d_m", "")
        respuestas["p2_eq_d_m"] = st.text_input("", value=val_p2_eq_d_m, key="p2_eq_d_m", label_visibility="collapsed")
        dibujar_feedback("p2_eq_d_m")
    with col_2b3:
        st.markdown('<div class="inline-text"> X + </div>', unsafe_allow_html=True)
    with col_2b4:
        val_p2_eq_d_n = st.session_state["respuestas_usuario"].get("p2_eq_d_n", "")
        respuestas["p2_eq_d_n"] = st.text_input("", value=val_p2_eq_d_n, key="p2_eq_d_n", label_visibility="collapsed")
        dibujar_feedback("p2_eq_d_n")
    with col_2b5:
        if st.button("🔍 Validar b", key="btn_val_p2_b", use_container_width=True):
            st.session_state["respuestas_usuario"]["p2_eq_d_m"] = respuestas["p2_eq_d_m"]
            st.session_state["respuestas_usuario"]["p2_eq_d_n"] = respuestas["p2_eq_d_n"]
            eq_d_m_ok, _ = validate_numeric(respuestas["p2_eq_d_m"], datos["p2"]["eq_d_m"], tolerance=0.05)
            eq_d_n_ok, _ = validate_numeric(respuestas["p2_eq_d_n"], datos["p2"]["eq_d_n"], tolerance=0.05)
            st.session_state["feedback_respuestas"]["p2_eq_d_m"] = {"ok": eq_d_m_ok, "ingresado": respuestas["p2_eq_d_m"], "esperado": datos["p2"]["eq_d_m"]}
            st.session_state["feedback_respuestas"]["p2_eq_d_n"] = {"ok": eq_d_n_ok, "ingresado": respuestas["p2_eq_d_n"], "esperado": datos["p2"]["eq_d_n"]}
            st.session_state["validada_p2_b"] = True
            st.rerun()
    with col_2b6:
        st.write("")

    # c) Punto de intersección de las rectas
    st.markdown('<div class="subquestion-title">c) El punto de intersección de las rectas de la gráfica. (6 puntos)</div>', unsafe_allow_html=True)
    col_2c1, col_2c2, col_2c3, col_2c4, col_2c5, col_2c6, col_2c7, col_2c8 = st.columns([2.5, 0.4, 1.5, 0.4, 1.5, 0.4, 2.5, 2.9], vertical_alignment="center")
    with col_2c1:
        st.markdown('<div class="inline-text">El punto es : </div>', unsafe_allow_html=True)
    with col_2c2:
        st.markdown('<div class="inline-text"> ( </div>', unsafe_allow_html=True)
    with col_2c3:
        val_p2_inter_x = st.session_state["respuestas_usuario"].get("p2_inter_x", "")
        respuestas["p2_inter_x"] = st.text_input("", value=val_p2_inter_x, key="p2_inter_x", label_visibility="collapsed")
        dibujar_feedback("p2_inter_x")
    with col_2c4:
        st.markdown('<div class="inline-text"> , </div>', unsafe_allow_html=True)
    with col_2c5:
        val_p2_inter_y = st.session_state["respuestas_usuario"].get("p2_inter_y", "")
        respuestas["p2_inter_y"] = st.text_input("", value=val_p2_inter_y, key="p2_inter_y", label_visibility="collapsed")
        dibujar_feedback("p2_inter_y")
    with col_2c6:
        st.markdown('<div class="inline-text"> ) </div>', unsafe_allow_html=True)
    with col_2c7:
        if st.button("🔍 Validar c", key="btn_val_p2_c", use_container_width=True):
            st.session_state["respuestas_usuario"]["p2_inter_x"] = respuestas["p2_inter_x"]
            st.session_state["respuestas_usuario"]["p2_inter_y"] = respuestas["p2_inter_y"]
            inter_x_ok, _ = validate_numeric(respuestas["p2_inter_x"], datos["p2"]["inter_x"], tolerance=0.05)
            inter_y_ok, _ = validate_numeric(respuestas["p2_inter_y"], datos["p2"]["inter_y"], tolerance=0.05)
            st.session_state["feedback_respuestas"]["p2_inter_x"] = {"ok": inter_x_ok, "ingresado": respuestas["p2_inter_x"], "esperado": datos["p2"]["inter_x"]}
            st.session_state["feedback_respuestas"]["p2_inter_y"] = {"ok": inter_y_ok, "ingresado": respuestas["p2_inter_y"], "esperado": datos["p2"]["inter_y"]}
            st.session_state["validada_p2_c"] = True
            st.rerun()
    with col_2c8:
        st.write("")

    with st.expander("Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
En esta sección aprendemos a extraer información analítica a partir de la representación geométrica de curvas y rectas tangentes:
1. **Pendiente de la Recta Tangente en C**: Podemos calcular la pendiente de la recta tangente $m_c$ de forma gráfica identificando dos puntos por los que pase la recta azul (por ejemplo, el punto $C$ y el punto donde la recta corta al eje Y o X) y aplicando la fórmula de la pendiente: $m = (y_2 - y_1) / (x_2 - x_1)$.
2. **Ecuación de la Recta Tangente en D**: La recta verde es tangente a la curva en $D$. Hallamos su pendiente $m_d$ usando dos puntos del dibujo por donde pase. Luego determinamos el intercepto con el eje Y ($n$) para estructurar la ecuación de la recta de la forma $Y = mX + n$.
3. **Punto de Intersección**: Las dos rectas tangentes se cruzan en un único punto. Para calcularlo, resolvemos el sistema lineal de dos ecuaciones igualando las expresiones de ambas rectas: $m_c X + n_c = m_d X + n_d$ para despejar la coordenada $X$, y luego evaluamos en cualquiera de las rectas para obtener la coordenada $Y$.

### Aplicación Simple en la Vida Real
Se utiliza en la **ingeniería vial y diseño de caminos**. Imagina que la curva roja es una loma o colina por la que se proyectan dos túneles o vías de tren rectas (las líneas tangentes azul y verde). Encontrar el punto de intersección de estas rectas tangentes es fundamental para que los ingenieros determinen el vértice de encuentro y calculen los ángulos de curvatura correctos para unir ambas pendientes mediante transiciones seguras.

### Guía Paso a Paso en GeoGebra Clásico (Por Literal)
* **Literal a) Pendiente de la recta tangente en C**
  1. Identifica las coordenadas del punto $C(4, 2)$ y otro punto por el que pasa la recta azul (como $(0, -1)$).
  2. Crea la recta en GeoGebra escribiendo: `rectaAzul = Recta((4, 2), (0, -1))`.
  3. Obtén la pendiente de la recta escribiendo: `Pendiente(rectaAzul)`.
* **Literal b) Ecuación de la recta tangente en D**
  1. Identifica las coordenadas del punto $D(6, 8)$ y otro por donde pase la recta verde (como $(4, 0)$).
  2. Escribe en la entrada: `rectaVerde = Recta((6, 8), (4, 0))`. GeoGebra mostrará de inmediato la ecuación de la recta en formato $Y = mX + n$.
* **Literal c) Punto de intersección de las rectas**
  1. En la entrada de GeoGebra, calcula la intersección exacta de ambas rectas utilizando el comando: `Intersección(rectaAzul, rectaVerde)`.
""")

# ==================== PREGUNTA 3 ====================
with st.container(border=True):
    st.markdown('<div class="question-title">DERIVADAS ENÉSIMAS (7 Puntos)</div>', unsafe_allow_html=True)
    st.write("Dada la función:")
    st.latex(datos["p3"]["función_latex"])
    st.write("Conteste las siguientes preguntas determinando los coeficientes de las derivadas indicadas:")

    # a) Primera derivada
    st.markdown('<div class="subquestion-title">a) ¿Cuál es la primera derivada de f? (3 puntos)</div>', unsafe_allow_html=True)
    col_3a1, col_3a2, col_3a3, col_3a4, col_3a5, col_3a6, col_3a7, col_3a8 = st.columns([1.5, 1.2, 0.4, 1.2, 0.4, 1.2, 2.5, 3.6], vertical_alignment="center")
    with col_3a1:
        st.markdown('<div class="inline-text">f\'(x) = </div>', unsafe_allow_html=True)
    with col_3a2:
        val_p3_d1_a = st.session_state["respuestas_usuario"].get("p3_d1_a", "")
        respuestas["p3_d1_a"] = st.text_input("", value=val_p3_d1_a, key="p3_d1_a", label_visibility="collapsed")
        dibujar_feedback("p3_d1_a")
    with col_3a3:
        st.markdown('<div class="inline-text"> x² + </div>', unsafe_allow_html=True)
    with col_3a4:
        val_p3_d1_b = st.session_state["respuestas_usuario"].get("p3_d1_b", "")
        respuestas["p3_d1_b"] = st.text_input("", value=val_p3_d1_b, key="p3_d1_b", label_visibility="collapsed")
        dibujar_feedback("p3_d1_b")
    with col_3a5:
        st.markdown('<div class="inline-text"> x + </div>', unsafe_allow_html=True)
    with col_3a6:
        val_p3_d1_c = st.session_state["respuestas_usuario"].get("p3_d1_c", "")
        respuestas["p3_d1_c"] = st.text_input("", value=val_p3_d1_c, key="p3_d1_c", label_visibility="collapsed")
        dibujar_feedback("p3_d1_c")
    with col_3a7:
        if st.button("🔍 Validar a", key="btn_val_p3_a", use_container_width=True):
            st.session_state["respuestas_usuario"]["p3_d1_a"] = respuestas["p3_d1_a"]
            st.session_state["respuestas_usuario"]["p3_d1_b"] = respuestas["p3_d1_b"]
            st.session_state["respuestas_usuario"]["p3_d1_c"] = respuestas["p3_d1_c"]
            d1_a_ok, _ = validate_numeric(respuestas["p3_d1_a"], datos["p3"]["d1_a"])
            d1_b_ok, _ = validate_numeric(respuestas["p3_d1_b"], datos["p3"]["d1_b"])
            d1_c_ok, _ = validate_numeric(respuestas["p3_d1_c"], datos["p3"]["d1_c"])
            st.session_state["feedback_respuestas"]["p3_d1_a"] = {"ok": d1_a_ok, "ingresado": respuestas["p3_d1_a"], "esperado": datos["p3"]["d1_a"]}
            st.session_state["feedback_respuestas"]["p3_d1_b"] = {"ok": d1_b_ok, "ingresado": respuestas["p3_d1_b"], "esperado": datos["p3"]["d1_b"]}
            st.session_state["feedback_respuestas"]["p3_d1_c"] = {"ok": d1_c_ok, "ingresado": respuestas["p3_d1_c"], "esperado": datos["p3"]["d1_c"]}
            st.session_state["validada_p3_a"] = True
            st.rerun()
    with col_3a8:
        st.write("")

    # b) Segunda derivada
    st.markdown('<div class="subquestion-title">b) ¿Cuál es la segunda derivada de f? (2 puntos)</div>', unsafe_allow_html=True)
    col_3b1, col_3b2, col_3b3, col_3b4, col_3b5, col_3b6 = st.columns([1.5, 1.2, 0.4, 1.2, 2.5, 5.2], vertical_alignment="center")
    with col_3b1:
        st.markdown('<div class="inline-text">f\'\'(x) = </div>', unsafe_allow_html=True)
    with col_3b2:
        val_p3_d2_a = st.session_state["respuestas_usuario"].get("p3_d2_a", "")
        respuestas["p3_d2_a"] = st.text_input("", value=val_p3_d2_a, key="p3_d2_a", label_visibility="collapsed")
        dibujar_feedback("p3_d2_a")
    with col_3b3:
        st.markdown('<div class="inline-text"> x + </div>', unsafe_allow_html=True)
    with col_3b4:
        val_p3_d2_b = st.session_state["respuestas_usuario"].get("p3_d2_b", "")
        respuestas["p3_d2_b"] = st.text_input("", value=val_p3_d2_b, key="p3_d2_b", label_visibility="collapsed")
        dibujar_feedback("p3_d2_b")
    with col_3b5:
        if st.button("🔍 Validar b", key="btn_val_p3_b", use_container_width=True):
            st.session_state["respuestas_usuario"]["p3_d2_a"] = respuestas["p3_d2_a"]
            st.session_state["respuestas_usuario"]["p3_d2_b"] = respuestas["p3_d2_b"]
            d2_a_ok, _ = validate_numeric(respuestas["p3_d2_a"], datos["p3"]["d2_a"])
            d2_b_ok, _ = validate_numeric(respuestas["p3_d2_b"], datos["p3"]["d2_b"])
            st.session_state["feedback_respuestas"]["p3_d2_a"] = {"ok": d2_a_ok, "ingresado": respuestas["p3_d2_a"], "esperado": datos["p3"]["d2_a"]}
            st.session_state["feedback_respuestas"]["p3_d2_b"] = {"ok": d2_b_ok, "ingresado": respuestas["p3_d2_b"], "esperado": datos["p3"]["d2_b"]}
            st.session_state["validada_p3_b"] = True
            st.rerun()
    with col_3b6:
        st.write("")

    # c) Tercera derivada
    st.markdown('<div class="subquestion-title">c) ¿Cuál es la tercera derivada de f? (2 puntos)</div>', unsafe_allow_html=True)
    col_3c1, col_3c2, col_3c3, col_3c4 = st.columns([1.5, 1.2, 2.5, 6.8], vertical_alignment="center")
    with col_3c1:
        st.markdown('<div class="inline-text">f\'\'\'(x) = </div>', unsafe_allow_html=True)
    with col_3c2:
        val_p3_d3 = st.session_state["respuestas_usuario"].get("p3_d3", "")
        respuestas["p3_d3"] = st.text_input("", value=val_p3_d3, key="p3_d3", label_visibility="collapsed")
        dibujar_feedback("p3_d3")
    with col_3c3:
        if st.button("🔍 Validar c", key="btn_val_p3_c", use_container_width=True):
            st.session_state["respuestas_usuario"]["p3_d3"] = respuestas["p3_d3"]
            d3_ok, _ = validate_numeric(respuestas["p3_d3"], datos["p3"]["d3"])
            st.session_state["feedback_respuestas"]["p3_d3"] = {"ok": d3_ok, "ingresado": respuestas["p3_d3"], "esperado": datos["p3"]["d3"]}
            st.session_state["validada_p3_c"] = True
            st.rerun()
    with col_3c4:
        st.write("")

    with st.expander("Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
En este ejercicio estudiamos las derivadas sucesivas de una función polinómica:
1. **Primera Derivada**: Se obtiene aplicando las reglas básicas de derivación. Para derivar una función compuesta como $(Ax - B)^3$, utilizamos la **regla de la cadena** (la derivada del bloque externo por la derivada del bloque interno) y restamos o sumamos las derivadas de los términos lineales correspondientes.
2. **Segunda Derivada**: Consiste en volver a derivar la función obtenida en la primera derivada.
3. **Tercera Derivada**: Consiste en volver a derivar la segunda derivada, lo que nos dará una constante en el caso de polinomios de grado 3.

### Aplicación Simple en la Vida Real
Se aplica directamente en la **física mecánica y control de movimiento de ascensores o montañas rusas**. Si la función original representa la posición del ascensor, la primera derivada es su **velocidad**, la segunda derivada es su **aceleración**, y la tercera derivada representa el **jerk o tirón** (la tasa de cambio de la aceleración). Controlar y limitar la tercera derivada (el jerk) a un valor constante adecuado es crucial para evitar sacudidas y garantizar un viaje suave y confortable para los pasajeros.

### Guía Paso a Paso en GeoGebra Clásico (Por Literal)
* **Literal a) Primera derivada de f**
  1. Define la función en la barra de entrada de GeoGebra, por ejemplo: `f(x) = (5x - 1)^3 - 7x + 9`.
  2. Escribe en la entrada: `f'(x)`. GeoGebra mostrará el desarrollo algebraico de la primera derivada. Identifica los coeficientes que acompañan a $x^2$, $x$ y el término constante.
* **Literal b) Segunda derivada de f**
  1. En la entrada de GeoGebra, calcula la segunda derivada escribiendo: `f''(x)`.
* **Literal c) Tercera derivada de f**
  1. En la entrada de GeoGebra, calcula la tercera derivada escribiendo: `f'''(x)`.
""")

# ==================== PREGUNTA 4 ====================
with st.container(border=True):
    st.markdown('<div class="question-title">RECTA TANGENTE HORIZONTAL (6 Puntos)</div>', unsafe_allow_html=True)
    st.write("Dada la función:")
    st.latex(datos["p4"]["función_latex"])
    st.write("Conteste la siguiente pregunta:")

    st.markdown('<div class="subquestion-title">¿En cuál punto de la gráfica la función f tiene una recta tangente horizontal?</div>', unsafe_allow_html=True)
    col_4a1, col_4a2, col_4a3, col_4a4 = st.columns([3, 2, 2.5, 4.5], vertical_alignment="center")
    with col_4a1:
        st.markdown('<div class="inline-text">El punto es : </div>', unsafe_allow_html=True)
    with col_4a2:
        val_p4_pt = st.session_state["respuestas_usuario"].get("p4_pt", "")
        opts_pt = datos["p4"]["opts_pt"]
        idx_pt = opts_pt.index(val_p4_pt) if val_p4_pt in opts_pt else 0
        respuestas["p4_pt"] = st.selectbox("", opts_pt, index=idx_pt, key="p4_pt", label_visibility="collapsed")
        dibujar_feedback("p4_pt")
    with col_4a3:
        if st.button("🔍 Validar", key="btn_val_p4", use_container_width=True):
            st.session_state["respuestas_usuario"]["p4_pt"] = respuestas["p4_pt"]
            p4_pt_ok = validate_string(respuestas["p4_pt"], datos["p4"]["punto_t_horiz"])
            st.session_state["feedback_respuestas"]["p4_pt"] = {"ok": p4_pt_ok, "ingresado": respuestas["p4_pt"], "esperado": datos["p4"]["punto_t_horiz"]}
            st.session_state["validada_p4"] = True
            st.rerun()
    with col_4a4:
        st.write("")

    with st.expander("Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
En este problema analizamos geométricamente las rectas tangentes horizontales:
1. **Pendiente Cero**: Una recta es completamente horizontal cuando su pendiente es exactamente cero.
2. **Ubicación en la Curva**: Dado que la pendiente de la recta tangente en cualquier punto es la primera derivada $f'(x)$, la recta tangente es horizontal únicamente en los puntos donde la primera derivada es cero ($f'(x) = 0$). Estos corresponden a los extremos locales de la función.
3. **Coordenadas del Punto**: Resolvemos la ecuación $f'(x) = 0$ para encontrar la coordenada $x$. Luego, evaluamos la función original $f(x)$ en ese valor para hallar la coordenada $y$ correspondiente, estructurando el punto como $(x, y)$.

### Aplicación Simple en la Vida Real
Se utiliza en el **diseño industrial y la arquitectura**. Al fabricar una pieza curva (por ejemplo, el techo arqueado de un edificio o la base moldeada de un envase plástico), los puntos con tangente horizontal representan las cúspides o los fondos planos (valles). Encontrar estos puntos con precisión matemática permite asegurar que la pieza se asiente de forma nivelada sobre una superficie horizontal sin tambalearse, o que tenga la altura máxima permitida por los límites de construcción.

### Guía Paso a Paso en GeoGebra Clásico
1. Define la función en la barra de entrada de GeoGebra, por ejemplo: `f(x) = 2x^4 - 8x`.
2. Para encontrar directamente los puntos donde la curva tiene extremos locales (y por ende rectas tangentes horizontales), escribe el comando: `Extremo(f)`.
3. GeoGebra marcará las coordenadas del punto en la gráfica.
""")

# ==================== PREGUNTA 5 ====================
with st.container(border=True):
    st.markdown('<div class="question-title">TENDENCIA DE RECTAS SECANTES A TANGENTES (25 puntos)</div>', unsafe_allow_html=True)
    st.write("Dada la función:")
    st.latex(datos["p5"]["función_latex"])
    st.write(f"a) Complete la tabla siguiente para calcular la pendiente de la recta tangente a la curva en $x_0 = {int(datos['p5']['x0'])}$ (20 puntos)")
    st.write("INDICACIÓN: Ingrese valores redondeados a 4 decimales.")
    
    # Renderizar la tabla de aproximación de secantes
    # Encabezados de columna
    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([1.5, 2.2, 2.2, 2.2, 2.2])
    with col_t1:
        st.markdown("**x**")
    with col_t2:
        st.markdown("**f(x)**")
    with col_t3:
        st.markdown("**Δx = x - x₀**")
    with col_t4:
        st.markdown("**Δy = f(x) - f(x₀)**")
    with col_t5:
        st.markdown("**M = Δy / Δx**")

    # Filas de la tabla
    for i, fila in enumerate(datos["p5"]["tabla"], 1):
        x_val = fila["x"]
        col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns([1.5, 2.2, 2.2, 2.2, 2.2], vertical_alignment="center")
        
        with col_r1:
            st.markdown(f'<div class="inline-text" style="font-weight: bold;">{x_val}</div>', unsafe_allow_html=True)
            
        with col_r2:
            key_fx = f"p5_row{i}_fx"
            val_fx = st.session_state["respuestas_usuario"].get(key_fx, "")
            respuestas[key_fx] = st.text_input("", value=val_fx, key=key_fx, label_visibility="collapsed")
            dibujar_feedback(key_fx)
            
        with col_r3:
            key_dx = f"p5_row{i}_dx"
            val_dx = st.session_state["respuestas_usuario"].get(key_dx, "")
            respuestas[key_dx] = st.text_input("", value=val_dx, key=key_dx, label_visibility="collapsed")
            dibujar_feedback(key_dx)
            
        with col_r4:
            key_dy = f"p5_row{i}_dy"
            val_dy = st.session_state["respuestas_usuario"].get(key_dy, "")
            respuestas[key_dy] = st.text_input("", value=val_dy, key=key_dy, label_visibility="collapsed")
            dibujar_feedback(key_dy)
            
        with col_r5:
            key_m = f"p5_row{i}_m"
            val_m = st.session_state["respuestas_usuario"].get(key_m, "")
            respuestas[key_m] = st.text_input("", value=val_m, key=key_m, label_visibility="collapsed")
            dibujar_feedback(key_m)

    # Botón para validar la tabla completa
    st.write("")
    col_tb1, col_tb2, col_tb3 = st.columns([4, 4, 4])
    with col_tb2:
        if st.button("🔍 Validar Tabla", key="btn_val_p5_a", use_container_width=True):
            for idx, fila in enumerate(datos["p5"]["tabla"], 1):
                key_fx = f"p5_row{idx}_fx"
                key_dx = f"p5_row{idx}_dx"
                key_dy = f"p5_row{idx}_dy"
                key_m = f"p5_row{idx}_m"
                
                st.session_state["respuestas_usuario"][key_fx] = respuestas[key_fx]
                st.session_state["respuestas_usuario"][key_dx] = respuestas[key_dx]
                st.session_state["respuestas_usuario"][key_dy] = respuestas[key_dy]
                st.session_state["respuestas_usuario"][key_m] = respuestas[key_m]
                
                fx_ok, _ = validate_numeric(respuestas[key_fx], fila["fx"], tolerance=0.0005)
                dx_ok, _ = validate_numeric(respuestas[key_dx], fila["dx"], tolerance=0.0005)
                dy_ok, _ = validate_numeric(respuestas[key_dy], fila["dy"], tolerance=0.0005)
                m_ok, _ = validate_numeric(respuestas[key_m], fila["m"], tolerance=0.005)
                
                st.session_state["feedback_respuestas"][key_fx] = {"ok": fx_ok, "ingresado": respuestas[key_fx], "esperado": fila["fx"]}
                st.session_state["feedback_respuestas"][key_dx] = {"ok": dx_ok, "ingresado": respuestas[key_dx], "esperado": fila["dx"]}
                st.session_state["feedback_respuestas"][key_dy] = {"ok": dy_ok, "ingresado": respuestas[key_dy], "esperado": fila["dy"]}
                st.session_state["feedback_respuestas"][key_m] = {"ok": m_ok, "ingresado": respuestas[key_m], "esperado": fila["m"]}
            
            st.session_state["validada_p5_a"] = True
            st.rerun()
            
    # b) Límite de tendencia
    st.markdown('<div class="subquestion-title">b) Observando la tabla anterior, ¿Hacia cuál valor tiende las pendientes M de las rectas secantes? (5 puntos)</div>', unsafe_allow_html=True)
    col_5b1, col_5b2, col_5b3, col_5b4 = st.columns([3, 2, 2.5, 4.5], vertical_alignment="center")
    with col_5b1:
        st.markdown('<div class="inline-text">Las pendientes M tienden al valor : </div>', unsafe_allow_html=True)
    with col_5b2:
        val_p5_limit = st.session_state["respuestas_usuario"].get("p5_limit", "")
        respuestas["p5_limit"] = st.text_input("", value=val_p5_limit, key="p5_limit", label_visibility="collapsed")
        dibujar_feedback("p5_limit")
    with col_5b3:
        if st.button("🔍 Validar b", key="btn_val_p5_b", use_container_width=True):
            st.session_state["respuestas_usuario"]["p5_limit"] = respuestas["p5_limit"]
            p5_limit_ok, _ = validate_numeric(respuestas["p5_limit"], datos["p5"]["lim_m"], tolerance=0.01)
            st.session_state["feedback_respuestas"]["p5_limit"] = {"ok": p5_limit_ok, "ingresado": respuestas["p5_limit"], "esperado": datos["p5"]["lim_m"]}
            st.session_state["validada_p5_b"] = True
            st.rerun()
    with col_5b4:
        st.write("")

    with st.expander("Ayudante Didáctico: ¿Cómo abordar este problema?"):
        st.markdown("""
### Razonamiento Pedagógico
Este ejercicio nos introduce conceptualmente a la definición de la derivada por medio de límites geométricos:
1. **Pendiente Secante**: La pendiente entre dos puntos de una curva se calcula como $M = \Delta y / \Delta x$. Esto representa el cambio promedio de la función.
2. **Aproximación Numérica**: Conforme acercamos el punto $x$ hacia $x_0$ (reduciendo $\Delta x$ a valores muy cercanos a cero), las rectas secantes cambian de inclinación y tienden a convertirse en la recta tangente en $x_0$.
3. **Tendencia al Límite**: El valor al que convergen o tienden las pendientes de las rectas secantes $M$ cuando $\Delta x \to 0$ es exactamente igual al límite de la razón de cambio, es decir, el valor de la derivada en dicho punto: $f'(x_0)$.

### Aplicación Simple en la Vida Real
Se aplica en el **análisis de telemetría y sensores en tiempo real** (por ejemplo, el velocímetro de un vehículo o sensores de ritmo cardíaco). Los dispositivos recopilan datos a intervalos discretos (cada segundo o milisegundo) y calculan la razón de cambio promedio (secante). Para mostrarte la velocidad o pulso instantáneo exacto en este milisegundo, la computadora del sensor reduce matemáticamente la ventana de tiempo analizada ($\Delta x \to 0$), encontrando el límite exacto (tangente) para entregarte un dato instantáneo fiel en pantalla.

### Guía Paso a Paso en GeoGebra Clásico
* **Para rellenar la tabla**
  1. Define la función en la barra de entrada de GeoGebra, por ejemplo: `f(x) = x^2 + 6x - 1`.
  2. Calcula el valor fijo del punto de tangencia escribiendo: `y0 = f(-2)`.
  3. Para evaluar cada fila (por ejemplo la de $x = -1.8$):
     * Escribe `f(-1.8)` para obtener la segunda columna.
     * Escribe `-1.8 - (-2)` para obtener el valor de la tercera columna ($\Delta x$).
     * Escribe `f(-1.8) - y0` para obtener la cuarta columna ($\Delta y$).
     * Divide los resultados escribiendo `dy / dx` o calcula la pendiente directamente.
* **Para el literal b (Tendencia)**
  1. Calcula analíticamente el valor límite derivando y evaluando la función:
     * En la entrada de GeoGebra escribe: `f'(x)`.
     * Luego escribe: `f'(-2)`. El resultado numérico obtenido es exactamente el valor de tendencia al que convergen las pendientes secantes.
""")

# ==================== BOTÓN DE ENVÍO Y CALIFICACIÓN ====================
st.markdown("---")

col_btn1, col_btn2 = st.columns([8, 4])
with col_btn1:
    btn_calificar = st.button("📝 Enviar Respuestas y Obtener Nota", type="primary", use_container_width=True, disabled=st.session_state["prueba_enviada"])
with col_btn2:
    btn_reiniciar = st.button("🔄 Reiniciar Prueba y Limpiar", type="secondary", use_container_width=True)

if btn_reiniciar:
    st.session_state["prueba_enviada"] = False
    st.session_state["respuestas_usuario"] = {}
    st.session_state["feedback_respuestas"] = {}
    st.session_state["puntos_obtenidos"] = 0.0
    st.session_state["nota_final"] = 1.0
    st.session_state["detalles"] = []
    
    # Limpiar banderas de validación
    for flag in subpreguntas_flags:
        st.session_state[flag] = False
    st.rerun()

if btn_calificar:
    # ----------------- CALIFICACIÓN DE RESPUESTAS -----------------
    puntos = 0.0
    detalles = []

    # PREGUNTA 1: 20 Puntos
    p1_a_ok, _ = validate_numeric(respuestas.get("p1_t_slope", ""), datos["p1"]["m_t"])
    p1_b_ok, _ = validate_numeric(respuestas.get("p1_n_slope", ""), datos["p1"]["m_n"])
    p1_c_ok = validate_string(respuestas.get("p1_eq_t", ""), datos["p1"]["eq_t"])
    p1_d_ok = validate_string(respuestas.get("p1_eq_n", ""), datos["p1"]["eq_n"])

    pts_1a = 3.0 if p1_a_ok else 0.0
    pts_1b = 3.0 if p1_b_ok else 0.0
    pts_1c = 7.0 if p1_c_ok else 0.0
    pts_1d = 7.0 if p1_d_ok else 0.0
    puntos += (pts_1a + pts_1b + pts_1c + pts_1d)
    
    detalles.append({"sub": "1.a (Pendiente Tangente)", "puntos": pts_1a, "max": 3.0, "ok": p1_a_ok, "ingresado": respuestas.get("p1_t_slope", ""), "esperado": datos["p1"]["m_t"]})
    detalles.append({"sub": "1.b (Pendiente Normal)", "puntos": pts_1b, "max": 3.0, "ok": p1_b_ok, "ingresado": respuestas.get("p1_n_slope", ""), "esperado": datos["p1"]["m_n"]})
    detalles.append({"sub": "1.c (Ecuación Tangente)", "puntos": pts_1c, "max": 7.0, "ok": p1_c_ok, "ingresado": respuestas.get("p1_eq_t", ""), "esperado": datos["p1"]["eq_t"]})
    detalles.append({"sub": "1.d (Ecuación Normal)", "puntos": pts_1d, "max": 7.0, "ok": p1_d_ok, "ingresado": respuestas.get("p1_eq_n", ""), "esperado": datos["p1"]["eq_n"]})

    # PREGUNTA 2: 15 Puntos
    p2_a_ok, _ = validate_numeric(respuestas.get("p2_slope_c", ""), datos["p2"]["m_c"], tolerance=0.05)
    p2_b_m_ok, _ = validate_numeric(respuestas.get("p2_eq_d_m", ""), datos["p2"]["eq_d_m"], tolerance=0.05)
    p2_b_n_ok, _ = validate_numeric(respuestas.get("p2_eq_d_n", ""), datos["p2"]["eq_d_n"], tolerance=0.05)
    p2_c_x_ok, _ = validate_numeric(respuestas.get("p2_inter_x", ""), datos["p2"]["inter_x"], tolerance=0.05)
    p2_c_y_ok, _ = validate_numeric(respuestas.get("p2_inter_y", ""), datos["p2"]["inter_y"], tolerance=0.05)

    pts_2a = 3.0 if p2_a_ok else 0.0
    pts_2b = 6.0 if (p2_b_m_ok and p2_b_n_ok) else 0.0
    pts_2c = 6.0 if (p2_c_x_ok and p2_c_y_ok) else 0.0
    puntos += (pts_2a + pts_2b + pts_2c)

    detalles.append({"sub": "2.a (Pendiente en C)", "puntos": pts_2a, "max": 3.0, "ok": p2_a_ok, "ingresado": respuestas.get("p2_slope_c", ""), "esperado": datos["p2"]["m_c"]})
    detalles.append({"sub": "2.b (Ecuación en D - Pendiente m)", "puntos": 3.0 if p2_b_m_ok else 0.0, "max": 3.0, "ok": p2_b_m_ok, "ingresado": respuestas.get("p2_eq_d_m", ""), "esperado": datos["p2"]["eq_d_m"]})
    detalles.append({"sub": "2.b (Ecuación en D - Intercepto n)", "puntos": 3.0 if p2_b_n_ok else 0.0, "max": 3.0, "ok": p2_b_n_ok, "ingresado": respuestas.get("p2_eq_d_n", ""), "esperado": datos["p2"]["eq_d_n"]})
    detalles.append({"sub": "2.c (Intersección X)", "puntos": 3.0 if p2_c_x_ok else 0.0, "max": 3.0, "ok": p2_c_x_ok, "ingresado": respuestas.get("p2_inter_x", ""), "esperado": datos["p2"]["inter_x"]})
    detalles.append({"sub": "2.c (Intersección Y)", "puntos": 3.0 if p2_c_y_ok else 0.0, "max": 3.0, "ok": p2_c_y_ok, "ingresado": respuestas.get("p2_inter_y", ""), "esperado": datos["p2"]["inter_y"]})

    # PREGUNTA 3: 7 Puntos
    p3_d1_a_ok, _ = validate_numeric(respuestas.get("p3_d1_a", ""), datos["p3"]["d1_a"])
    p3_d1_b_ok, _ = validate_numeric(respuestas.get("p3_d1_b", ""), datos["p3"]["d1_b"])
    p3_d1_c_ok, _ = validate_numeric(respuestas.get("p3_d1_c", ""), datos["p3"]["d1_c"])
    
    p3_d2_a_ok, _ = validate_numeric(respuestas.get("p3_d2_a", ""), datos["p3"]["d2_a"])
    p3_d2_b_ok, _ = validate_numeric(respuestas.get("p3_d2_b", ""), datos["p3"]["d2_b"])
    
    p3_d3_ok, _ = validate_numeric(respuestas.get("p3_d3", ""), datos["p3"]["d3"])

    pts_3a = 3.0 if (p3_d1_a_ok and p3_d1_b_ok and p3_d1_c_ok) else 0.0
    pts_3b = 2.0 if (p3_d2_a_ok and p3_d2_b_ok) else 0.0
    pts_3c = 2.0 if p3_d3_ok else 0.0
    puntos += (pts_3a + pts_3b + pts_3c)

    detalles.append({"sub": "3.a (1ra Derivada Coef x²)", "puntos": 1.0 if p3_d1_a_ok else 0.0, "max": 1.0, "ok": p3_d1_a_ok, "ingresado": respuestas.get("p3_d1_a", ""), "esperado": datos["p3"]["d1_a"]})
    detalles.append({"sub": "3.a (1ra Derivada Coef x)", "puntos": 1.0 if p3_d1_b_ok else 0.0, "max": 1.0, "ok": p3_d1_b_ok, "ingresado": respuestas.get("p3_d1_b", ""), "esperado": datos["p3"]["d1_b"]})
    detalles.append({"sub": "3.a (1ra Derivada Coef const)", "puntos": 1.0 if p3_d1_c_ok else 0.0, "max": 1.0, "ok": p3_d1_c_ok, "ingresado": respuestas.get("p3_d1_c", ""), "esperado": datos["p3"]["d1_c"]})
    detalles.append({"sub": "3.b (2da Derivada Coef x)", "puntos": 1.0 if p3_d2_a_ok else 0.0, "max": 1.0, "ok": p3_d2_a_ok, "ingresado": respuestas.get("p3_d2_a", ""), "esperado": datos["p3"]["d2_a"]})
    detalles.append({"sub": "3.b (2da Derivada Coef const)", "puntos": 1.0 if p3_d2_b_ok else 0.0, "max": 1.0, "ok": p3_d2_b_ok, "ingresado": respuestas.get("p3_d2_b", ""), "esperado": datos["p3"]["d2_b"]})
    detalles.append({"sub": "3.c (3ra Derivada)", "puntos": 2.0 if p3_d3_ok else 0.0, "max": 2.0, "ok": p3_d3_ok, "ingresado": respuestas.get("p3_d3", ""), "esperado": datos["p3"]["d3"]})

    # PREGUNTA 4: 6 Puntos
    p4_ok = validate_string(respuestas.get("p4_pt", ""), datos["p4"]["punto_t_horiz"])
    pts_4 = 6.0 if p4_ok else 0.0
    puntos += pts_4
    detalles.append({"sub": "4 (Punto Tangente Horizontal)", "puntos": pts_4, "max": 6.0, "ok": p4_ok, "ingresado": respuestas.get("p4_pt", ""), "esperado": datos["p4"]["punto_t_horiz"]})

    # PREGUNTA 5: 25 Puntos
    p5_tabla_ok = True
    c_puntos_tabla = 0.0
    for idx, fila in enumerate(datos["p5"]["tabla"], 1):
        key_fx = f"p5_row{idx}_fx"
        key_dx = f"p5_row{idx}_dx"
        key_dy = f"p5_row{idx}_dy"
        key_m = f"p5_row{idx}_m"
        
        r_fx, _ = validate_numeric(respuestas.get(key_fx, ""), fila["fx"], tolerance=0.0005)
        r_dx, _ = validate_numeric(respuestas.get(key_dx, ""), fila["dx"], tolerance=0.0005)
        r_dy, _ = validate_numeric(respuestas.get(key_dy, ""), fila["dy"], tolerance=0.0005)
        r_m, _ = validate_numeric(respuestas.get(key_m, ""), fila["m"], tolerance=0.005)
        
        c_puntos_tabla += (1.0 if r_fx else 0.0) + (1.0 if r_dx else 0.0) + (1.0 if r_dy else 0.0) + (1.0 if r_m else 0.0)
        
        if not (r_fx and r_dx and r_dy and r_m):
            p5_tabla_ok = False
            
    # La tabla vale 20 puntos totales, 1 punto por cada una de las 20 celdas
    puntos += c_puntos_tabla
    
    # Detalle de la tabla en reporte global
    detalles.append({"sub": "5.a (Tabla de Secantes - 20 celdas)", "puntos": c_puntos_tabla, "max": 20.0, "ok": p5_tabla_ok, "ingresado": "Múltiples celdas", "esperado": "Tabla correcta"})
    
    # Límite de tendencia
    p5_limit_ok, _ = validate_numeric(respuestas.get("p5_limit", ""), datos["p5"]["lim_m"], tolerance=0.01)
    pts_5b = 5.0 if p5_limit_ok else 0.0
    puntos += pts_5b
    detalles.append({"sub": "5.b (Valor límite de tendencia)", "puntos": pts_5b, "max": 5.0, "ok": p5_limit_ok, "ingresado": respuestas.get("p5_limit", ""), "esperado": datos["p5"]["lim_m"]})

    # Guardar en estado global
    st.session_state["puntos_obtenidos"] = puntos
    st.session_state["nota_final"] = calcular_nota(puntos, 73.0)
    st.session_state["detalles"] = detalles
    st.session_state["prueba_enviada"] = True
    
    # Cargar feedback individual
    for d in detalles:
        pass
    
    # Forzar el feedback individual en st.session_state para la revisión
    # Pregunta 1
    st.session_state["feedback_respuestas"]["p1_t_slope"] = {"ok": p1_a_ok, "ingresado": respuestas.get("p1_t_slope", ""), "esperado": datos["p1"]["m_t"]}
    st.session_state["feedback_respuestas"]["p1_n_slope"] = {"ok": p1_b_ok, "ingresado": respuestas.get("p1_n_slope", ""), "esperado": datos["p1"]["m_n"]}
    st.session_state["feedback_respuestas"]["p1_eq_t"] = {"ok": p1_c_ok, "ingresado": respuestas.get("p1_eq_t", ""), "esperado": datos["p1"]["eq_t"]}
    st.session_state["feedback_respuestas"]["p1_eq_n"] = {"ok": p1_d_ok, "ingresado": respuestas.get("p1_eq_n", ""), "esperado": datos["p1"]["eq_n"]}
    # Pregunta 2
    st.session_state["feedback_respuestas"]["p2_slope_c"] = {"ok": p2_a_ok, "ingresado": respuestas.get("p2_slope_c", ""), "esperado": datos["p2"]["m_c"]}
    st.session_state["feedback_respuestas"]["p2_eq_d_m"] = {"ok": p2_b_m_ok, "ingresado": respuestas.get("p2_eq_d_m", ""), "esperado": datos["p2"]["eq_d_m"]}
    st.session_state["feedback_respuestas"]["p2_eq_d_n"] = {"ok": p2_b_n_ok, "ingresado": respuestas.get("p2_eq_d_n", ""), "esperado": datos["p2"]["eq_d_n"]}
    st.session_state["feedback_respuestas"]["p2_inter_x"] = {"ok": p2_c_x_ok, "ingresado": respuestas.get("p2_inter_x", ""), "esperado": datos["p2"]["inter_x"]}
    st.session_state["feedback_respuestas"]["p2_inter_y"] = {"ok": p2_c_y_ok, "ingresado": respuestas.get("p2_inter_y", ""), "esperado": datos["p2"]["inter_y"]}
    # Pregunta 3
    st.session_state["feedback_respuestas"]["p3_d1_a"] = {"ok": p3_d1_a_ok, "ingresado": respuestas.get("p3_d1_a", ""), "esperado": datos["p3"]["d1_a"]}
    st.session_state["feedback_respuestas"]["p3_d1_b"] = {"ok": p3_d1_b_ok, "ingresado": respuestas.get("p3_d1_b", ""), "esperado": datos["p3"]["d1_b"]}
    st.session_state["feedback_respuestas"]["p3_d1_c"] = {"ok": p3_d1_c_ok, "ingresado": respuestas.get("p3_d1_c", ""), "esperado": datos["p3"]["d1_c"]}
    st.session_state["feedback_respuestas"]["p3_d2_a"] = {"ok": p3_d2_a_ok, "ingresado": respuestas.get("p3_d2_a", ""), "esperado": datos["p3"]["d2_a"]}
    st.session_state["feedback_respuestas"]["p3_d2_b"] = {"ok": p3_d2_b_ok, "ingresado": respuestas.get("p3_d2_b", ""), "esperado": datos["p3"]["d2_b"]}
    st.session_state["feedback_respuestas"]["p3_d3"] = {"ok": p3_d3_ok, "ingresado": respuestas.get("p3_d3", ""), "esperado": datos["p3"]["d3"]}
    # Pregunta 4
    st.session_state["feedback_respuestas"]["p4_pt"] = {"ok": p4_ok, "ingresado": respuestas.get("p4_pt", ""), "esperado": datos["p4"]["punto_t_horiz"]}
    # Pregunta 5
    for idx, f in enumerate(datos["p5"]["tabla"], 1):
        key_fx = f"p5_row{idx}_fx"
        key_dx = f"p5_row{idx}_dx"
        key_dy = f"p5_row{idx}_dy"
        key_m = f"p5_row{idx}_m"
        st.session_state["feedback_respuestas"][key_fx] = {"ok": validate_numeric(respuestas.get(key_fx, ""), f["fx"], tolerance=0.0005)[0], "ingresado": respuestas.get(key_fx, ""), "esperado": f["fx"]}
        st.session_state["feedback_respuestas"][key_dx] = {"ok": validate_numeric(respuestas.get(key_dx, ""), f["dx"], tolerance=0.0005)[0], "ingresado": respuestas.get(key_dx, ""), "esperado": f["dx"]}
        st.session_state["feedback_respuestas"][key_dy] = {"ok": validate_numeric(respuestas.get(key_dy, ""), f["dy"], tolerance=0.0005)[0], "ingresado": respuestas.get(key_dy, ""), "esperado": f["dy"]}
        st.session_state["feedback_respuestas"][key_m] = {"ok": validate_numeric(respuestas.get(key_m, ""), f["m"], tolerance=0.005)[0], "ingresado": respuestas.get(key_m, ""), "esperado": f["m"]}
    st.session_state["feedback_respuestas"]["p5_limit"] = {"ok": p5_limit_ok, "ingresado": respuestas.get("p5_limit", ""), "esperado": datos["p5"]["lim_m"]}
    
    st.rerun()

# ----------------- REPORTE DE RESULTADOS (MODO REVISAR) -----------------
if st.session_state["prueba_enviada"]:
    st.write("---")
    st.write("## 📝 Reporte de Calificación (Modo Revisión)")
    
    col_rep1, col_rep2, col_rep3 = st.columns([4, 4, 4])
    with col_rep1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state["puntos_obtenidos"]} / 73.0</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Puntaje Total Obtenido</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_rep2:
        nota = st.session_state["nota_final"]
        clase_nota = "nota-aprobado" if nota >= 4.0 else "nota-reprobado"
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="chilean-nota {clase_nota}">{nota}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Calificación Final</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_rep3:
        porcentaje = round((st.session_state["puntos_obtenidos"] / 73.0) * 100, 1)
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{porcentaje}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Porcentaje de Logro</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("### Detalles por Subpregunta")
    
    # Crear una tabla de reporte detallado
    tabla_detalles = []
    for d in st.session_state["detalles"]:
        estado = "✅ Correcto" if d["ok"] else "❌ Incorrecto"
        tabla_detalles.append({
            "Subpregunta": d["sub"],
            "Resultado": estado,
            "Puntos": f"{d['puntos']} / {d['max']}",
            "Ingresado": str(d["ingresado"]),
            "Esperado (Correcto)": str(d["esperado"])
        })
    st.table(pd.DataFrame(tabla_detalles))
