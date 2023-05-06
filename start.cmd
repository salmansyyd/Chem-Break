REM Type: Batch file
REM Description: Starts the program

start "" /B pythonw.exe chem_break.pyw >> logs/break.log 2>&1


@REM Stop the program
@REM taskkill /F /IM pythonw.exe