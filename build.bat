REM Batch File To Automate the build process

REM Delete the dist folder and recreate it
rmdir /Q /S dist
mkdir dist

REM Build PySnake using PyInstaller
pyinstaller --noconsole --onefile --name PySnake main.py

REM Copy player_data.txt to the root of dist
copy player_data.txt dist\

REM Copy the entire assets folder to the root of dist
xcopy /E /I assets dist\assets\

REM Pause to keep the command prompt window open for inspection (optional)
pause
