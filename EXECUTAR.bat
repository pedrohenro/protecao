@echo off
REM ============================================================
REM SISTEMA DE PROTEÇÃO DE MÁQUINA - VERSÃO WINDOWS
REM ============================================================
REM Clique duplo neste arquivo para executar

setlocal enabledelayedexpansion

REM Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO: Python não está instalado ou não está no PATH!
    echo.
    echo Siga estes passos:
    echo 1. Visite: https://www.python.org/downloads/
    echo 2. Baixe Python 3.9 ou superior
    echo 3. IMPORTANTE: Marque "Add Python to PATH" durante instalação
    echo 4. Reinicie o computador
    echo 5. Execute este arquivo novamente
    echo.
    pause
    exit /b 1
)

REM Verifica privilégios de admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  AVISO: Recomenda-se executar como Administrador
    echo Relançando com privilégios elevados...
    echo.
    
    REM Tenta executar como admin
    powershell -Command "Start-Process cmd -ArgumentList '/c %0' -Verb RunAs"
    exit /b 0
)

REM Limpa tela
cls

REM Exibe banner
echo.
echo ============================================================
echo           🛡️  PROTEÇÃO DE MÁQUINA - VERSÃO 1.0
echo ============================================================
echo.

REM Localiza o arquivo Python
set "script_path=%~dp0protecao_maquina.py"

REM Verifica se arquivo existe
if not exist "%script_path%" (
    echo ❌ ERRO: Arquivo 'protecao_maquina.py' não encontrado!
    echo.
    echo Certifique-se de que protecao_maquina.py está na mesma pasta
    echo.
    pause
    exit /b 1
)

REM Executa o programa
echo ✅ Iniciando Sistema de Proteção...
echo.

python "%script_path%"

REM Se chegou aqui, programa encerrou
echo.
echo 👋 Proteção encerrada
echo.
pause
