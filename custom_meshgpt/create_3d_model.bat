@echo off
pushd "%~dp0"

rem Remove or comment out the local environment activation line
rem call env\Scripts\activate.bat

rem Run the script using the already activated global environment (cad_env)
python custom_meshgpt/main.py

pause
