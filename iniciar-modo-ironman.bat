@echo off
chcp 65001 > nul
title MIK-JARVIS - INTERFAZ HOLOGRAFICA IRON MAN
cd /d "%~dp0"
echo =========================================================================
echo   INICIANDO MIK-JARVIS: INTERFAZ HOLOGRAFICA ARC REACTOR (IRON MAN)
echo   Powered by MIK Software
echo   Abriendo en tu navegador predeterminado (http://localhost:5000)...
echo =========================================================================
uv run python servidor_ironman.py
pause
