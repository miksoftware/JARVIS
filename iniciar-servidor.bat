@echo off
title MIK-JARVIS - Servidor API y Web
cd /d "%~dp0"
echo ============================================================
echo   Iniciando Servidor API y Web MIK-JARVIS en http://localhost:8000
echo   Powered by MIK Software
echo ============================================================
uv run mik-jarvis serve --host 127.0.0.1 --port 8000
pause
