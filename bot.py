import requests
import pandas as pd
import time
from datetime import datetime

# Konfiguracja
API_URL = "http://127.0.0.1:8000/sales"  # URL API
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_url"  # Webhook Discord
SALES_THRESHOLD = 100000  # Próg sprzedaży do monitorowania
CHECK_INTERVAL = 60  # Częstotliwość sprawdzania (w sekundach)

# Funkcja do pobierania danych z API
def fetch_sales_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        print("Nie udało się pobrać danych z API.")
        return pd.DataFrame()

# Funkcja do wysyłania powiadomień na Discord
def send_discord_notification(message):
    payload = {
        "content": message
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("Powiadomienie wysłane na Discord.")
    else:
        print("Nie udało się wysłać powiadomienia na Discord.")

# Funkcja do generowania raportu
def generate_report(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sales_report_{timestamp}.csv"
    data.to_csv(filename, index=False)
    print(f"Raport wygenerowany: {filename}")

# Główna pętla bota
def monitor_sales():
    print("Bot rozpoczął monitorowanie sprzedaży...")
    while True:
        data = fetch_sales_data()
        if not data.empty:
            # Sprawdź, czy sprzedaż spadła poniżej progu
            low_sales = data[data["sales_amount"] < SALES_THRESHOLD]
            if not low_sales.empty:
                message = "⚠️ **Alert:** Sprzedaż spadła poniżej progu!\n"
                message += low_sales.to_string(index=False)
                send_discord_notification(message)

            # Generuj raport co godzinę
            if datetime.now().minute == 0:  # Generuj raport o pełnej godzinie
                generate_report(data)

        # Poczekaj przed kolejnym sprawdzeniem
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_sales()