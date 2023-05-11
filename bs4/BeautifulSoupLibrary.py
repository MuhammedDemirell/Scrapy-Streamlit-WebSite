import requests
from bs4 import BeautifulSoup
import json

url = "https://www.hepsiemlak.com/istanbul-sahibinden"
apartmentCounter = 1


def apartmentPriceClear(apartmentPrice):
    if apartmentPrice:
        apartmentPrice = apartmentPrice.replace('\n', '')
        apartmentPrice = apartmentPrice.replace('TL', '').strip()
        apartmentPrice += " ₺"
        return apartmentPrice
    return apartmentPrice


def apartmenPropertyTypeClear(apartmentPropertyType):
    if apartmentPropertyType:
        apartmentPropertyType = apartmentPropertyType.strip('\n ')
        return apartmentPropertyType
    return apartmentPropertyType


def apartmentLocationClear(apartmentLocation):
    if apartmentLocation:
        apartmentLocation = apartmentLocation.strip('\n ')
        apartmentLocation = apartmentLocation.replace(",", "")
        return apartmentLocation
    return apartmentLocation


def apartmentSizeClear(apartmentSize):
    if apartmentSize:
        apartmentSize = apartmentSize.strip('\n ')
        apartmentSize += "²"
        return apartmentSize
    return apartmentSize


def apartmentAdvertDateClear(apartmentAdvertDate):
    if apartmentAdvertDate:
        apartmentAdvertDate = apartmentAdvertDate.strip('\n ')
        return apartmentAdvertDate
    return apartmentAdvertDate


def apartmentAdvertTitleClear(apartmentAdvertTitle):
    if apartmentAdvertTitle:
        apartmentAdvertTitle = apartmentAdvertTitle.strip('\n ')
        return apartmentAdvertTitle
    return apartmentAdvertTitle


def scrape_apartments():
    url = "https://www.hepsiemlak.com/istanbul-sahibinden"
    apartmentCounter = 1

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        apartments = soup.select(".listView > ul > li")
        for apartment in apartments:
            apartmentImage = apartment.select_one(".list-view-image.ignore-lazy, .he-lazy-image.list-view-image")["src"]
            apartmentAdvertTitle = apartment.select_one(".list-view-header h3").get_text().strip()

            NumberOfApartmentRooms_elem = apartment.select_one(".houseRoomCount span")
            NumberOfApartmentRooms = NumberOfApartmentRooms_elem.get_text().strip() if NumberOfApartmentRooms_elem else None

            apartmentPrice = apartment.select_one(".top span").get_text().strip()
            apartmentPropertyType = apartment.select_one(".list-view-location > span:first-of-type").get_text().strip()
            apartmentAdvertDate = apartment.select_one(".list-view-date").get_text().strip()
            apartmentLocation = apartment.select_one(".list-view-location > span:last-of-type").get_text().strip()

            yield {
                'id': apartmentCounter,
                'apartmentImage': apartmentImage,
                'apartmentAdvertTitle': apartmentAdvertTitleClear(apartmentAdvertTitle),
                'numberOfApartmentRooms': NumberOfApartmentRooms,
                'apartmentPrice': apartmentPriceClear(apartmentPrice),
                'apartmentPropertyType': apartmenPropertyTypeClear(apartmentPropertyType),
                'apartmentLocation': apartmentLocationClear(apartmentLocation),
                'apartmentAdvertDate': apartmentAdvertDateClear(apartmentAdvertDate)
            }
            apartmentCounter += 1

        nextPage = soup.select_one(".he-pagination__navigate-text--next")["href"] if soup.select_one(
            ".he-pagination__navigate-text--next") else None
        url = f"https://www.hepsiemlak.com{nextPage}" if nextPage else None


import keyboard

apartments_data = []

for apartment in scrape_apartments():
    print(apartment)
    apartments_data.append(apartment)

    if keyboard.is_pressed('s'):
        print("Stopping the script.")
        break

with open("apartments_data.json", "w", encoding="utf-8") as f:
    json.dump(apartments_data, f, ensure_ascii=False, indent=4)
