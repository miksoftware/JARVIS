@echo off
chcp 65001 > nul
title MIK-JARVIS - MODO CONSOLA
cd /d "%~dp0"
echo =========================================================================
echo   INICIANDO MIK-JARVIS: MODO CONSOLA (TERMINAL)
echo   Powered by MIK Software
echo =========================================================================
uv run python modo_ironman.py
pause
