import streamlit as st
import psycopg2

st.set_page_config(page_title="İlan Güncelle", page_icon=":house:")
st.header("Mülk Siparişi Güncelle")

connection = psycopg2.connect(
    host="localhost",
    database="hepsiEmlak",
    user="postgres",
    password="123123",
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM orders")
ilanlar = cursor.fetchall()

nameToUpdate = st.selectbox("Güncellenecek kişiyi seçin:", [ilan[0] for ilan in ilanlar])
person = [ilan for ilan in ilanlar if ilan[0] == nameToUpdate]
if person:
    person = person[0]
    apartmentSize, numberOfApartmentRooms, apartmentPrice, apartmentPropertyType, apartmentLocation, apartmentAdvertDate = person[
                                                                                                                           1:]

    newFirstNameAndSurName = st.text_input("Yeni isim:", value=nameToUpdate)
    newApartmentSize = st.text_input("Yeni boyut:", value=apartmentSize)
    newNumberOfApartmentRooms = st.text_input("Yeni oda sayısı:", value=numberOfApartmentRooms)
    newApartmentPrice = st.text_input("Yeni fiyat:", value=apartmentPrice)
    newApartmentPropertyType = st.selectbox("Daire Tipi", ["Kiralık", "Satılık"],
                                            index=["Kiralık", "Satılık"].index(apartmentPropertyType))
    newApartmentLocation = st.text_input("Yeni lokasyon:", value=apartmentLocation)
    newApartmentAdvertDate = st.text_input("Yeni tarih:", value=apartmentAdvertDate)
    if st.button("Güncelle"):
        update_query = "UPDATE orders SET ad_soyad = %s, apartment_price = %s, apartment_size = %s, number_of_apartment_rooms = %s, apartment_property_type = %s, apartment_location = %s, apartment_advert_date = %s WHERE ad_soyad = %s"
        cursor.execute(update_query, (
            newFirstNameAndSurName, apartmentPrice, newApartmentSize, newNumberOfApartmentRooms,
            newApartmentPropertyType,
            newApartmentLocation, newApartmentAdvertDate, nameToUpdate))
        num_rows_updated = cursor.rowcount
        connection.commit()
        if num_rows_updated == 0:
            st.error("Kişinin İlanı Bulunamadı.")
        else:
            st.success(f"{nameToUpdate} başarıyla güncellendi.")
else:
    st.error("Kişinin İlanı Bulunamadı.")
