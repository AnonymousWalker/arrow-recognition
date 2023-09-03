@echo off
:: Batch script to run a Python script as administrator
:: Replace "your_script.py" with the actual name of your Python script
:: Replace "C:\your\directory" with the actual directory path

:: Change directory
cd /d "E:/SchoolProjects/arrow-recognition"

:: Prompt for admin rights and keep the window open
powershell -Command "Start-Process cmd -ArgumentList '/k python "gui.py"' -Verb RunAs"
