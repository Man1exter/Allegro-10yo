@echo off

:: Sprawdź, czy Python jest zainstalowany
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nie jest zainstalowany. Zainstaluj go przed uruchomieniem aplikacji.
    exit /b 1
)

:: Sprawdź, czy Streamlit jest zainstalowany
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Streamlit nie jest zainstalowany. Instalowanie...
    pip install streamlit
)

:: Sprawdź, czy API działa
curl -s --head --request GET http://127.0.0.1:8000/sales | find "200 OK" >nul
if %errorlevel% neq 0 (
    echo API nie działa. Upewnij się, że API jest uruchomione na localhost:8000.
    exit /b 1
)

:: Uruchom aplikację Streamlit
echo Wszystkie zależności są poprawne. Uruchamianie aplikacji...
streamlit run app.py