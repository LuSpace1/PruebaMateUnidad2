# 📐 Prueba Interactiva de Matemáticas (Cálculo y Álgebra)

Este proyecto es una aplicación web interactiva desarrollada en **Python** con **Streamlit** que permite rendir una prueba matemática basada en 5 problemas complejos de cálculo, progresiones aritméticas y ajuste de curvas logísticas. Evalúa las respuestas del alumno de manera automatizada bajo la **escala de notas chilena** (1.0 a 7.0) con exigencia parametrizable.

## ✨ Características del Proyecto

* **3 Variaciones Dinámicas**: Incluye tres sets de datos numéricos distintos que preservan la estructura y complejidad matemática original.
* **Validación de Respuestas Inteligente**: Diseñado para ser flexible con la sintaxis de las respuestas ingresadas por el alumno (admite comas `,` y puntos `.`, ignora espacios accidentales en expresiones matemáticas, e intervalos).
* **Ayudante Pedagógico Integrado**: Cada sección cuenta con un panel desplegable ("Ayudante Didáctico") que explica:
  * El razonamiento matemático pedagógico del problema.
  * Los comandos de **GeoGebra** necesarios para resolverlo paso a paso en software gráfico.
  * La implicancia y aplicación práctica del problema en el mundo real.
* **Escala de Notas Chilena Oficial**: Implementa las ecuaciones oficiales de calificación con nota de aprobación 4.0 al alcanzar el porcentaje de exigencia determinado (60% por defecto).

---

## 🛠️ Requisitos Previos

Solo necesitas tener instalado **Python 3.8 o superior** en tu sistema.

---

## 🚀 Instalación y Uso Rápido (Windows)

Si estás utilizando Windows, se incluye un script automático que configura y arranca la aplicación sin que tengas que usar la terminal:

1. Descarga o clona este repositorio.
2. Haz doble clic en el archivo:
   👉 `iniciar_prueba.bat`
3. El script creará un entorno virtual local de forma aislada, instalará las dependencias necesarias (`streamlit` y `pandas`) y levantará el servidor web en tu navegador de forma automática.

---

## 💻 Instalación Manual (Cualquier Sistema Operativo)

Si prefieres realizar la instalación de forma manual o estás en macOS/Linux, sigue estos pasos:

### Opción A: Usando `uv` (Recomendado por su velocidad)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/proyecto-matematicas.git
cd proyecto-matematicas

# 2. Crear el entorno virtual e instalar dependencias automáticamente
uv venv
uv pip install streamlit pandas

# 3. Iniciar la aplicación
uv run streamlit run app.py
```

### Opción B: Usando `pip` estándar

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/proyecto-matematicas.git
cd proyecto-matematicas

# 2. Crear el entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
source .venv/bin/activate

# 4. Instalar las dependencias
pip install streamlit pandas

# 5. Iniciar la aplicación
streamlit run app.py
```

---

## 📈 Estructura del Código

* `app.py`: Archivo de código fuente principal con la interfaz, base de datos de variaciones, funciones de validación lógica y renders HTML/LaTeX.
* `test_validation.py`: Script para probar y depurar la lógica de validación matemática bajo casos de prueba simulados.
* `iniciar_prueba.bat`: Ejecutable para el inicio automático y simplificado en entornos Windows.

---

## 🇨🇱 Cálculo del Rendimiento Escolar

El sistema evalúa el puntaje sobre un máximo de **103 puntos** desglosados en:
* **Pregunta 1**: 20 Puntos (Estudio de función desconocida cúbica).
* **Pregunta 2**: 8 Puntos (Puntos críticos y de inflexión).
* **Pregunta 3**: 20 Puntos (Integración y cinemática de una partícula).
* **Pregunta 4**: 30 Puntos (Crecimiento, máximos y concavidades).
* **Pregunta 5**: 25 Puntos (Modelamiento y ajuste de curvas logísticas).

La nota se asigna mediante la fórmula estándar de la escala en Chile:
* Si $Puntaje < Exigencia \times Max$:
  $$\text{Nota} = 1.0 + 3.0 \cdot \frac{Puntaje}{Exigencia \times Max}$$
* Si $Puntaje \ge Exigencia \times Max$:
  $$\text{Nota} = 4.0 + 3.0 \cdot \frac{Puntaje - Exigencia \times Max}{Max - Exigencia \times Max}$$
