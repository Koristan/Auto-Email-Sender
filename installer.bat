@echo off

call git clone https://github.com/Koristan/Auto-Email-Sender.git

cd Auto-Email-Sender\autoEmailsSender

set /p mail=Enter YANDEX-mail: 
set /p token=Enter token:

@echo ==============DATA=================
@echo ACCOUNT_NAME = '%mail%' > app\config.py 
@echo ACCOUNT_OUT_PASSWORD = '%token%' >> app\config.py 

@echo ==============LOADING...=================

call python -m venv venv
call venv\Scripts\activate.bat
call pip install -r req.txt

@echo @echo off >> start.bat
@echo call venv\Scripts\activate.bat >> start.bat
@echo start "" http://127.0.0.1:5000 >> start.bat
@echo python -m client.main >> start.bat
@echo pause >> start.bat

@echo ===============READY TO USE====================
pause