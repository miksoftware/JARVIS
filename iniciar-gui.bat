@echo off
title MIK-JARVIS - Interfaz Grafica
cd /d "%~dp0"
echo ============================================================
echo   Iniciando MIK-JARVIS GUI (Interfaz Web y Servidor API)
echo   Powered by MIK Software
echo ============================================================
uv run mik-jarvis gui
pause
