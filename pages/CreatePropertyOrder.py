import streamlit as st
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="hepsiEmlak",
    user="postgres",
    password="123123",
)

cursor = connection.cursor()

create_table_query = '''CREATE TABLE IF NOT EXISTS orders (
    ad_soyad text,
    apartment_size text,
    number_of_apartment_rooms text,
    apartment_price text,
    apartment_property_type text,
    apartment_location text,
    apartment_advert_date text
);'''

cursor.execute(create_table_query)

connection.commit()

st.set_page_config(page_title="Daire Siparis Ver", page_icon=":house:")

cursor.execute("SELECT apartment_advert_title FROM add_apartment")
apartmentAdvertTitle = cursor.fetchall()

apartmentAdvertTitleList = []
for i in apartmentAdvertTitle:
    apartmentAdvertTitleList.append(i[0])

st.header("Mülk Siparişi Oluştur")

with st.form("Sipariş", clear_on_submit=True):
    firstNameAndSurName = st.text_input("Ad ve Soyad")
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
    siparisVer = st.form_submit_button("Sipariş Ver")

    if siparisVer:
        if not firstNameAndSurName or not apartmentSize or not numberOfApartmentRooms or not apartmentPrice or not apartmentPropertyType or not apartmentLocation or not apartmentAdvertDate:
            st.warning("Lütfen tüm alanları doldurun")
        else:
            cursor.execute("INSERT INTO orders VALUES (%s, %s, %s, %s,%s, %s, %s)", (
                firstNameAndSurName, apartmentSize, numberOfApartmentRooms, apartmentPrice, apartmentPropertyType,
                apartmentLocation,
                apartmentAdvertDate))
            connection.commit()
            st.success("Sipariş Başarılı Bir Şekilde Gerçekleştirildi")
