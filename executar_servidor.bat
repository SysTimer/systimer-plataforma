@echo off
:inicio
cd /d %~dp0
title Servidor Tailwind CSS Auto Reload Browse - Rene
cls
python manage.py tailwind start
echo.
echo Pressione Enter para iniciar novamente o comando ou feche a janela para sair.
pause >nul
goto inicio
