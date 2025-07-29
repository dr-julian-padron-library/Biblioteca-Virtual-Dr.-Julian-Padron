@echo off
:loop
git fetch --all
timeout /t 60 >nul
goto loop