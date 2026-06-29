@echo off
title Iniciar Prueba Interactiva de Matemáticas
echo.
echo =========================================================
echo   Iniciando Servidor de la Prueba de Matematicas...
echo =========================================================
echo.
:: Activar el entorno virtual y lanzar streamlit
call .venv\Scripts\activate.bat
streamlit run app.py
pause
