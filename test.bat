@echo off
for /R %%f in (*.pyc) do (
	REM C:\python24\python.exe unpyc.pyc -D "%%f" > "%%f.py" 2>&1
	echo %%f
	python.exe ..\unc2.py "%%f" > "%%f.py" 2>&1
)