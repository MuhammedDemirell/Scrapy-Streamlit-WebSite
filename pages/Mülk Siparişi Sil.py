import streamlit as st
import psycopg2

st.set_page_config(page_title="İlan Sil", page_icon=":house:")
st.header("Mülk Siparişi Sil")

connection = psycopg2.connect(
    host="localhost",
    database="hepsiEmlak",
    user="postgres",
    password="123123",
)

cursor = connection.cursor()

silinenIsim = st.text_input("Silinecek Kişinin adını girin:")
if st.button("Sil"):
    cursor.execute("SELECT * FROM orders WHERE ad_soyad = %s", (silinenIsim,))
    if cursor.rowcount == 0:
        st.error("Kişinin İlanı Bulunamadı.")
    else:
        cursor.execute("DELETE FROM orders WHERE ad_soyad = %s", (silinenIsim,))
        connection.commit()
        st.success(f"{silinenIsim} başarıyla silindi.")
