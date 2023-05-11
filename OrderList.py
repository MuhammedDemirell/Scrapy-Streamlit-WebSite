import pandas as pd
import streamlit as st
import psycopg2
import streamlit.components.v1 as stc

st.set_page_config(page_title="Ana Sayfa", page_icon=":house:")

st.header("Siparişler")

connection = psycopg2.connect(
    host="localhost",
    database="hepsiEmlak",
    user="postgres",
    password="123123",
)

cursor = connection.cursor()
cursor.execute("SELECT * FROM orders")
orders = cursor.fetchall()

df = pd.DataFrame(orders, columns=["Ad ve Soyad", "Boyut", "Oda Sayısı", "Fiyat", "Tip", "Lokasyon", "Tarih"])
df.index += 1

st.markdown("""
<style>
    .dataframe th, .dataframe td {
        padding: 12px;
        text-align: center;
        font-size: 18px;
    }
    .dataframe th {
        background-color: #FFC107;
        color: white;
    }
    .dataframe tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .dataframe tr:hover {
        background-color: #FFC107;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.table(df.style.set_table_styles([{
    'selector': 'th',
    'props': [
        ('font-size', '20px'),
        ('background-color', '#FFC107'),
        ('color', 'white')
    ]
}, {
    'selector': 'td',
    'props': [
        ('font-size', '18px')
    ]
}]))

stc.html(
    """
    <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
    </style>
    """,
    height=0,
)
