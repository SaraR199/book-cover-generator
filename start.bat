@echo off
cd /d "%~dp0"

REM Try VS 2022 first
if exist "%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\Launch-VsDevShell.ps1" (
    powershell -NoExit -Command "& '%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\Launch-VsDevShell.ps1'; Set-Location '%~dp0'; claude"
) else if exist "%ProgramFiles%\Microsoft Visual Studio\2022\Professional\Common7\Tools\Launch-VsDevShell.ps1" (
    powershell -NoExit -Command "& '%ProgramFiles%\Microsoft Visual Studio\2022\Professional\Common7\Tools\Launch-VsDevShell.ps1'; Set-Location '%~dp0'; claude"
) else if exist "%ProgramFiles%\Microsoft Visual Studio\2022\Community\Common7\Tools\Launch-VsDevShell.ps1" (
    powershell -NoExit -Command "& '%ProgramFiles%\Microsoft Visual Studio\2022\Community\Common7\Tools\Launch-VsDevShell.ps1'; Set-Location '%~dp0'; claude"
) else (
    echo Visual Studio 2022 Developer PowerShell not found
    echo Opening regular PowerShell instead...
    start powershell -NoExit -Command "Set-Location '%~dp0'; claude"
)