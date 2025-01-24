import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import requests

# Konfiguracja strony
st.set_page_config(page_title="Analiza sprzedaży Allegro", layout="wide")
st.title("Analiza sprzedaży na Allegro (2013-2022)")

# Funkcja do pobierania danych z API
@st.cache_data  # Cache'owanie danych dla wydajności
def fetch_data():
    url = "https://api.example.com/sales"  # Zastąp prawdziwym URL API
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Nie udało się pobrać danych z API.")
        return pd.DataFrame()

# Pobieranie danych
data = fetch_data()

# Sprawdzenie, czy dane zostały pobrane
if data.empty:
    st.stop()

# Wybór branży
industries = data["industry"].unique()
selected_industry = st.sidebar.selectbox("Wybierz branżę", industries)

# Filtrowanie danych dla wybranej branży
industry_data = data[data["industry"] == selected_industry]

# Wyświetlenie danych
st.subheader(f"Dane sprzedaży dla branży: {selected_industry}")
st.write(industry_data)

# Wykres sprzedaży w czasie
st.subheader("Sprzedaż w czasie")
plt.figure(figsize=(10, 6))
plt.plot(industry_data["year"], industry_data["sales_amount"], marker="o")
plt.title(f"Sprzedaż w branży {selected_industry} (2013-2022)")
plt.xlabel("Rok")
plt.ylabel("Sprzedaż (PLN)")
plt.grid()
st.pyplot(plt)

# Model wzrostu (regresja liniowa)
st.subheader("Prognoza wzrostu")
X = industry_data["year"].values.reshape(-1, 1)
y = industry_data["sales_amount"].values

model = LinearRegression()
model.fit(X, y)
future_years = np.array([2023, 2024, 2025]).reshape(-1, 1)
predictions = model.predict(future_years)

# Wyświetlenie prognozy
st.write("Prognoza sprzedaży na lata 2023-2025:")
future_data = pd.DataFrame({
    "Rok": future_years.flatten(),
    "Prognozowana sprzedaż": predictions
})
st.write(future_data)

# Wykres prognozy
plt.figure(figsize=(10, 6))
plt.plot(industry_data["year"], industry_data["sales_amount"], marker="o", label="Dane historyczne")
plt.plot(future_years, predictions, marker="o", linestyle="--", label="Prognoza")
plt.title(f"Prognoza sprzedaży dla branży {selected_industry}")
plt.xlabel("Rok")
plt.ylabel("Sprzedaż (PLN)")
plt.legend()
plt.grid()
st.pyplot(plt)

# Porównanie branż
st.subheader("Porównanie sprzedaży między branżami")
plt.figure(figsize=(12, 8))
sns.lineplot(data=data, x="year", y="sales_amount", hue="industry", marker="o")
plt.title("Porównanie sprzedaży między branżami (2013-2022)")
plt.xlabel("Rok")
plt.ylabel("Sprzedaż (PLN)")
plt.legend(title="Branża")
plt.grid()
st.pyplot(plt)