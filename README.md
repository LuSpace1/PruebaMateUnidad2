# Prueba Interactiva de Matemáticas (Cálculo y Álgebra)

Esta es una aplicación web interactiva desarrollada en Python con Streamlit para resolver y evaluar una prueba de matemáticas basada en 5 problemas de cálculo, progresiones y curvas logísticas. Evalúa las respuestas de forma automática y calcula la calificación final según la escala de notas chilena (1.0 a 7.0).

## Características

* 3 variaciones dinámicas con diferentes valores numéricos.
* Validación flexible de respuestas (soporta comas, puntos y omite espacios).
* Ayudante didáctico integrado por cada ejercicio con instrucciones para resolver en GeoGebra y su aplicación en la vida real.
* Cálculo de nota final basado en la escala chilena oficial (exigencia parametrizable, 60% por defecto).

## Estructura del Proyecto

* app.py: Código principal de la aplicación Streamlit.
* test_validation.py: Script para comprobar la lógica de evaluación de respuestas.
* iniciar_prueba.bat: Ejecutable para inicializar el entorno y correr la app en Windows.
* .gitignore: Configuración para excluir archivos del entorno virtual en Git.

## Instalación y Uso

### Windows (Inicio Rápido)

1. Descargue o clone este repositorio.
2. Ejecute el archivo iniciar_prueba.bat haciendo doble clic en él.
3. Se creará el entorno virtual, se instalarán las dependencias e iniciará la aplicación en el navegador web de forma automática.

### Ejecución Manual (Cualquier Sistema)

1. Clonar el repositorio:
   git clone https://github.com/LuSpace1/PruebaMateUnidad2.git
   cd PruebaMateUnidad2

2. Crear y activar un entorno virtual:
   python -m venv .venv
   # En Windows: .venv\Scripts\activate
   # En macOS/Linux: source .venv/bin/activate

3. Instalar dependencias:
   pip install streamlit pandas

4. Ejecutar la aplicación:
   streamlit run app.py
