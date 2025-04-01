@echo off
pushd "%~dp0"

python -m venv env
call env\Scripts\activate.bat

pip install -e .

pause