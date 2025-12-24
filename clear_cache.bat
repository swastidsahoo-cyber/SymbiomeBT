@echo off
echo Clearing Streamlit cache...
if exist .streamlit\cache rmdir /s /q .streamlit\cache
if exist __pycache__ rmdir /s /q __pycache__
if exist modules\__pycache__ rmdir /s /q modules\__pycache__

echo.
echo Cache cleared! Now restart Streamlit with:
echo streamlit run app.py
echo.
echo Or if Streamlit is already running, press 'C' then 'R' in your browser
pause
