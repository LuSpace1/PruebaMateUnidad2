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
* iniciar_prueba.bat: Ejecutable para Windows que realiza de forma 100% automática la creación del entorno virtual, la instalación de dependencias y la ejecución de la app.
* requirements.txt: Archivo de dependencias del proyecto.
* .gitignore: Configuración para excluir archivos del entorno virtual en Git.

## Instalación y Uso

### Windows (Inicio Rápido Todo en Uno)

1. Descargue o clone este repositorio en su computadora.
2. Haga doble clic en el archivo iniciar_prueba.bat.
3. El archivo automatizado se encargará de todo: detectará su instalación de Python/uv, creará el entorno virtual local .venv de forma aislada, instalará las dependencias necesarias de requirements.txt y abrirá la aplicación interactiva directamente en su navegador web listo para usar.

### Instalación Manual con uv (Recomendado)

1. Clonar el repositorio:
   git clone https://github.com/LuSpace1/PruebaMateUnidad2.git
   cd PruebaMateUnidad2

2. Crear el entorno virtual:
   uv venv

3. Instalar dependencias:
   uv pip install -r requirements.txt

4. Ejecutar la aplicación:
   uv run streamlit run app.py

### Instalación Manual con pip estándar

1. Clonar el repositorio:
   git clone https://github.com/LuSpace1/PruebaMateUnidad2.git
   cd PruebaMateUnidad2

2. Crear y activar el entorno virtual:
   python -m venv .venv
   # En Windows: .venv\Scripts\activate
   # En macOS/Linux: source .venv/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Ejecutar la aplicación:
   streamlit run app.py
