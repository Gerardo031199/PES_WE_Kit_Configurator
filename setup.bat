@echo on
set PY_FILE=kit_configurator.py
set PROJECT_NAME=Kit Configurator
set VERSION=1.1.0
set FILE_VERSION=file_version_info.txt 

pyinstaller --onefile --noconsole "%PY_FILE%" --name "%PROJECT_NAME% %VERSION%" --version-file "%FILE_VERSION%"

pause