#!/bin/bash

# Sprawdź, czy Python jest zainstalowany
if ! command -v python3 &> /dev/null
then
    echo "Python3 nie jest zainstalowany. Zainstaluj go przed uruchomieniem aplikacji."
    exit 1
fi

# Sprawdź, czy Streamlit jest zainstalowany
if ! python3 -c "import streamlit" &> /dev/null
then
    echo "Streamlit nie jest zainstalowany. Instalowanie..."
    pip install streamlit
fi

# Sprawdź, czy API działa
API_URL="http://127.0.0.1:8000/sales"
if ! curl -s --head --request GET "$API_URL" | grep "200 OK" > /dev/null
then
    echo "API nie działa. Upewnij się, że API jest uruchomione na localhost:8000."
    exit 1
fi

# Uruchom aplikację Streamlit
echo "Wszystkie zależności są poprawne. Uruchamianie aplikacji..."
streamlit run app.py