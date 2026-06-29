@echo off
title Iniciar Prueba Interactiva de Matemáticas
echo.
echo =========================================================
echo   Iniciando Servidor de la Prueba de Matemáticas...
echo =========================================================
echo.

:: Comprobar si existe el entorno virtual
if not exist ".venv" (
    echo El entorno virtual no existe. Creándolo...
    
    :: Intentar crear con uv
    where uv >nul 2>nul
    if %errorlevel% equ 0 (
        echo Detectado 'uv'. Inicializando entorno virtual con uv...
        uv venv .venv
        if %errorlevel% neq 0 (
            echo Error al crear entorno con uv. Abortando.
            pause
            exit /b
        )
        echo Instalando dependencias con uv...
        uv pip install -r requirements.txt
    ) else (
        :: Si no hay uv, usar python estándar
        echo 'uv' no detectado. Intentando inicializar con python -m venv...
        where python >nul 2>nul
        if %errorlevel% neq 0 (
            echo Error: No se detectó Python en el sistema. Por favor instálelo para continuar.
            pause
            exit /b
        )
        python -m venv .venv
        if %errorlevel% neq 0 (
            echo Error al crear el entorno virtual con Python. Abortando.
            pause
            exit /b
        )
        echo Instalando dependencias con pip...
        call .venv\Scripts\activate.bat
        pip install -r requirements.txt
    )
)

:: Activar el entorno e iniciar la aplicación
echo Iniciando aplicación web...
call .venv\Scripts\activate.bat
streamlit run app.py
pause
