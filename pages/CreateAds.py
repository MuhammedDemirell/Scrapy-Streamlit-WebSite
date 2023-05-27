import psycopg2
import streamlit as st
import sys

sys.path.append("..")

connection = psycopg2.connect(
    host="localhost",
    database="hepsiEmlak",
    user="postgres",
    password="123123",
)

cursor = connection.cursor()

create_table_query = '''CREATE TABLE IF NOT EXISTS add_apartment (
    id SERIAL PRIMARY KEY,
    apartment_image text,
    apartment_advert_title text,
    apartment_size text,
    number_of_apartment_rooms text,
    apartment_price text,
    apartment_property_type text,
    apartment_location text,
    apartment_advert_date text
);'''

cursor.execute(create_table_query)
st.set_page_config(page_title="İlan Yayınlama", page_icon=":house:")

connection.commit()

st.header("İlan Oluştur")

with st.form("AddAparments", clear_on_submit=True):
    apartmentAdvertTitle = st.text_input("İlan Başlık")
    apartmentSize = st.text_input("Dairenin Büyüklüğü")
    numberOfApartmentRooms = st.selectbox("Oda Sayısı",
                                          ['Ekleyiniz', '1 + 0', '1 + 1', '1 + 2', '1 + 3', '1 + 4', '1 + 5', '2 + 0',
                                           '2 + 1', '2 + 2', '2 + 3', '2 + 4', '2 + 5', '3 + 0', '3 + 1', '3 + 2',
                                           '3 + 3', '3 + 4', '3 + 5', '4 + 0', '4 + 1', '4 + 2', '4 + 3', '4 + 4',
                                           '4 + 5', '5 + 0', '5 + 1', '5 + 2', '5 + 3', '5 + 4', '5 + 5'])
    apartmentPrice = st.text_input("Fiyat")
    apartmentPropertyType = st.selectbox("Daire Tipi", ["Kiralık", "Satılık"])
    apartmentLocation = st.text_input("Lokasyon")
    apartmentAdvertDate = st.text_input("Yayınlanma Tarihi")
    image = st.file_uploader("İlan Resmi Ekleyiniz")
    add = st.form_submit_button("Resim Ekle")

    if add:
        if apartmentAdvertTitle and apartmentSize and numberOfApartmentRooms != 'Ekleyiniz' and apartmentPrice and apartmentPropertyType and apartmentLocation and apartmentAdvertDate:
            imageUrl = None
            if image is not None:
                imageUrl = "img/" + image.name
                with open(imageUrl, "wb") as f:
                    f.write(image.read())
            cursor.execute(
                "SELECT COALESCE(MAX(id), 0) + 1 FROM add_apartment"
            )
            new_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO add_apartment (id, apartment_image, apartment_advert_title, apartment_size, number_of_apartment_rooms, apartment_price, apartment_property_type, apartment_location, apartment_advert_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (new_id, imageUrl, apartmentAdvertTitle, apartmentSize, numberOfApartmentRooms,
                 apartmentPrice, apartmentPropertyType, apartmentLocation, apartmentAdvertDate))

            connection.commit()
            st.success("İlan Başarıyla Eklendi")
        else:
            st.warning("Lütfen Tüm Alanları Doldurun.")
