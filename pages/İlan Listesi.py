import streamlit as st
import psycopg2

st.set_page_config(page_title="Katalog", page_icon=":house:")
st.header("İlan Listesi")
connection = psycopg2.connect(
    host="localhost",
    database="hepsiEmlak",
    user="postgres",
    password="123123",
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM add_apartment LIMIT 20 OFFSET 0")
apartment = cursor.fetchall()

page_number = st.sidebar.number_input("Page Number", min_value=1, step=1, value=1)
offset = (page_number - 1) * 20

cursor.execute(f"SELECT * FROM add_apartment LIMIT 20 OFFSET {offset}")
apartment   = cursor.fetchall()

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

for _apartment in apartment:
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        if _apartment[1] is not None:
            st.image(_apartment[1], width=150)
    with col3:
        st.write(_apartment[3])
    with col4:
        st.write(_apartment[4])
    with col5:
        st.write(_apartment[5])
    with col6:
        st.text(_apartment[6])
    with col7:
        st.text(_apartment[7])
    with col8:
        st.text(_apartment[8])

num_rows = cursor.rowcount
num_pages = (num_rows // 20) + 1
if num_rows > 20:
    st.sidebar.write(f"Page {page_number} of {num_pages}")
    if page_number > 1:
        st.sidebar.button("Previous Page", key="prev")
    if page_number < num_pages:
        st.sidebar.button("Next Page", key="next")
