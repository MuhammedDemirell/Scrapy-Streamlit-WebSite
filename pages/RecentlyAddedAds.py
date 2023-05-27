import streamlit as st
import psycopg2

st.set_page_config(page_title="Son Eklenen İlanlar", page_icon=":house:")

st.header("En Son Eklenen İlanlar")
connection = psycopg2.connect(
    host="localhost",
    database="hepsiEmlak",
    user="postgres",
    password="123123",
)
cursor = connection.cursor()
cursor.execute("SELECT * FROM add_apartment ORDER BY id DESC LIMIT 10")
lastAdverts = cursor.fetchall()

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
with col1:
    st.write("**İlan Resmi**")
with col3:
    st.write("**Boyut**")
with col4:
    st.write("**Oda Sayısı**")
with col5:
    st.write("**Fiyat**")
with col6:
    st.write("**İlan Tipi**")
with col7:
    st.write("**Lokasyon**")
with col8:
    st.write("**İlan Tarihi**")

for advert in lastAdverts:
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        if advert[1] is not None:
            st.image(advert[1], width=160)
    with col3:
        st.write(advert[3])
    with col4:
        st.write(advert[4])
    with col5:
        st.write(advert[5])
    with col6:
        st.write(advert[6])
    with col7:
        st.text(advert[7])
    with col8:
        st.write(advert[8])
