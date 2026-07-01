# Prueba Interactiva de Matemáticas (Cálculo y Álgebra)

Esta es una suite de aplicaciones web interactivas desarrolladas en Python con Streamlit para resolver, estudiar y evaluar guías de ejercicios de cálculo y derivadas. Evalúa las respuestas de forma automática y calcula la calificación final según la escala de notas chilena (1.0 a 7.0).

---

## 📚 Guías de Ejercicios Disponibles

### 📘 Guía 1: Cálculo de Variaciones, Optimización y Curvas Logísticas (103 Puntos)
* **Archivo Principal**: app.py
* **Lanzador Rápido**: iniciar_prueba.bat
* **Test de Validación**: test_validation.py
* **Contenido**:
  1. Interpolación de una función cúbica mediante un sistema lineal de 4 variables.
  2. Puntos críticos de derivada cero e inflexión.
  3. Recuperación de función de posición $f(x)$ a partir de tabla de pendientes de recta tangente (Integración).
  4. Análisis completo de una curva cúbica dada (crecimiento, máximos, concavidad y tangentes).
  5. Ajuste y comportamiento de una curva de crecimiento logístico.

### 📗 Guía 2: Rectas Tangentes, Derivadas Sucesivas y Secantes (73 Puntos)
* **Archivo Principal**: app2.py
* **Lanzador Rápido**: iniciar_prueba2.bat
* **Test de Validación**: test_validation2.py
* **Contenido**:
  1. Cálculo de pendientes y ecuaciones explícitas de rectas tangentes y normales.
  2. Extracción analítica e intersección de rectas tangentes a partir de gráficas interactivas dibujadas dinámicamente con `matplotlib`.
  3. Desarrollo algebraico de derivadas sucesivas (primera, segunda y tercera derivada).
  4. Localización de puntos con recta tangente horizontal ($f'(x) = 0$).
  5. Aproximación numérica de pendientes secantes y su tendencia al límite de la derivada.

---

## ✨ Características Comunes

* **Variaciones Dinámicas**: Cada guía cuenta con 3 variaciones diferentes que modifican los números y gráficos de forma consistente.
* **Cero Emojis en Explicaciones**: Las ayudas didácticas mantienen un tono formal y académico.
* **Validadores Individuales**: Botones de validación rápida al lado de cada respuesta para verificar aciertos al instante.
* **Sección de Revisión**: Al enviar la prueba se despliega un reporte detallado con las respuestas incorrectas y correctas en rojo para retroalimentación.
* **Cálculo de Nota Chilena**: Escala chilena de 1.0 a 7.0 con exigencia parametrizada al 60%.

---

## 🚀 Instalación y Uso

### Windows (Inicio Rápido Todo en Uno)
Haga doble clic en el archivo `.bat` correspondiente a la guía que desea rendir:
* Para iniciar la **Guía 1**: Doble clic en `iniciar_prueba.bat`
* Para iniciar la **Guía 2**: Doble clic en `iniciar_prueba2.bat`

El archivo se encargará automáticamente de inicializar el entorno virtual `.venv`, instalar las dependencias necesarias de `requirements.txt` y abrir la app en su navegador.

### Ejecución Manual con uv
1. Crear el entorno virtual:
   ```bash
   uv venv
   ```
2. Instalar dependencias:
   ```bash
   uv pip install -r requirements.txt
   ```
3. Ejecutar la aplicación deseada:
   * Para Guía 1: `uv run streamlit run app.py`
   * Para Guía 2: `uv run streamlit run app2.py`

### Ejecución Manual con pip estándar
1. Crear y activar el entorno virtual:
   ```bash
   python -m venv .venv
   # En Windows: .venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar:
   * Para Guía 1: `streamlit run app.py`
   * Para Guía 2: `streamlit run app2.py`

---

## 🧪 Desarrollo y Pruebas Offline

Para validar la lógica matemática de la evaluación offline en la consola, puede ejecutar los scripts de prueba:
* Para testear la Guía 1:
  ```bash
  python test_validation.py
  ```
* Para testear la Guía 2:
  ```bash
  python test_validation2.py
  ```
