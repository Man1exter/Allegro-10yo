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

# Filtrowanie danych po roku
st.sidebar.subheader("Filtruj dane po roku")
min_year = int(data["year"].min())
max_year = int(data["year"].max())
year_range = st.sidebar.slider(
    "Wybierz zakres lat",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)
filtered_data = data[(data["year"] >= year_range[0]) & (data["year"] <= year_range[1])]

# Wybór branży
st.sidebar.subheader("Wybierz branżę do analizy")
industries = filtered_data["industry"].unique()
selected_industry = st.sidebar.selectbox("Branża", industries)

# Filtrowanie danych dla wybranej branży
industry_data = filtered_data[filtered_data["industry"] == selected_industry]

# Statystyki opisowe
st.subheader(f"Statystyki opisowe dla branży: {selected_industry}")
stats = industry_data["sales_amount"].describe()
st.write(stats)

# Wykres sprzedaży w czasie
st.subheader("Sprzedaż w czasie")
plt.figure(figsize=(10, 6))
plt.plot(industry_data["year"], industry_data["sales_amount"], marker="o", label="Dane historyczne")
plt.title(f"Sprzedaż w branży {selected_industry} ({year_range[0]}-{year_range[1]})")
plt.xlabel("Rok")
plt.ylabel("Sprzedaż (PLN)")
plt.grid()
plt.legend()
st.pyplot(plt)

# Analiza trendów (regresja liniowa)
st.subheader("Analiza trendów")
X = industry_data["year"].values.reshape(-1, 1)
y = industry_data["sales_amount"].values

model = LinearRegression()
model.fit(X, y)
trend_line = model.predict(X)

plt.figure(figsize=(10, 6))
plt.plot(industry_data["year"], industry_data["sales_amount"], marker="o", label="Dane historyczne")
plt.plot(industry_data["year"], trend_line, linestyle="--", label="Trend liniowy")
plt.title(f"Trend sprzedaży dla branży {selected_industry}")
plt.xlabel("Rok")
plt.ylabel("Sprzedaż (PLN)")
plt.grid()
plt.legend()
st.pyplot(plt)

# Porównanie dwóch branż
st.sidebar.subheader("Porównanie dwóch branż")
industry_1 = st.sidebar.selectbox("Wybierz pierwszą branżę", industries, key="industry_1")
industry_2 = st.sidebar.selectbox("Wybierz drugą branżę", industries, key="industry_2")

if industry_1 != industry_2:
    st.subheader(f"Porównanie sprzedaży: {industry_1} vs {industry_2}")
    industry_1_data = filtered_data[filtered_data["industry"] == industry_1]
    industry_2_data = filtered_data[filtered_data["industry"] == industry_2]

    plt.figure(figsize=(12, 8))
    plt.plot(industry_1_data["year"], industry_1_data["sales_amount"], marker="o", label=industry_1)
    plt.plot(industry_2_data["year"], industry_2_data["sales_amount"], marker="o", label=industry_2)
    plt.title(f"Porównanie sprzedaży: {industry_1} vs {industry_2}")
    plt.xlabel("Rok")
    plt.ylabel("Sprzedaż (PLN)")
    plt.grid()
    plt.legend()
    st.pyplot(plt)
else:
    st.warning("Wybierz dwie różne branże do porównania.")

# Eksport danych
st.subheader("Eksport danych")
if st.button("Pobierz dane jako CSV"):
    csv = filtered_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Kliknij, aby pobrać",
        data=csv,
        file_name="sales_data.csv",
        mime="text/csv"
    )