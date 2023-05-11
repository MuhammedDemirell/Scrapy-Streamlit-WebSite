import scrapy


class apartmentForRent(scrapy.Spider):
    name = "apartmentForRent"
    allowed_domains = ["hepsiemlak.com"]
    start_urls = ["https://www.hepsiemlak.com/istanbul-sahibinden"]
    apartmentCounter = 1

    def apartmentPriceClear(self, apartmentPrice):
        if apartmentPrice:
            apartmentPrice = apartmentPrice.strip('\n ')
            apartmentPrice += " ₺"
            return apartmentPrice
        return apartmentPrice

    def apartmenPropertyTypeClear(self, apartmentPropertyType):
        if apartmentPropertyType:
            apartmentPropertyType = apartmentPropertyType.strip('\n ')
            return apartmentPropertyType
        return apartmentPropertyType

    def apartmentLocationClear(self, apartmentLocation):
        if apartmentLocation:
            apartmentLocation = apartmentLocation.strip('\n ')
            apartmentLocation = apartmentLocation.replace(",", "")
            return apartmentLocation
        return apartmentLocation

    def apartmentSizeClear(self, apartmentSize):
        if apartmentSize:
            apartmentSize = apartmentSize.strip('\n ')
            apartmentSize += "²"
            return apartmentSize
        return apartmentSize

    def apartmentAdvertDateClear(self, apartmentAdvertDate):
        if apartmentAdvertDate:
            apartmentAdvertDate = apartmentAdvertDate.strip('\n ')
            return apartmentAdvertDate
        return apartmentAdvertDate

    def apartmentAdvertTitleClear(self, apartmentAdvertTitle):
        if apartmentAdvertTitle:
            apartmentAdvertTitle = apartmentAdvertTitle.strip('\n ')
            return apartmentAdvertTitle
        return apartmentAdvertTitle

    def parse(self, response):
        apartments = response.xpath("//div[@class='listView']/ul/li")
        for apartment in apartments:
            apartmentImage = apartment.xpath(".//img[@class='list-view-image ignore-lazy']/@src")
            if not apartmentImage:
                apartmentImage = apartment.xpath(".//img[@class='he-lazy-image list-view-image']/@src")
            apartmentImage = apartmentImage.get() if apartmentImage else None
            apartmentAdvertTitle = apartment.xpath(
                ".//section[@class='bottom sibling']/div[@class='left']/div/header[@class='list-view-header']/hgroup/h3/text()").get()
            apartmentSize = apartment.xpath(
                ".//section[@class='middle sibling']/div[@class='top']/div[@class='right']/span[@class='celly squareMeter list-view-size']/span/span/span/text()").get()
            NumberOfApartmentRooms = apartment.xpath(
                ".//section[@class='middle sibling']/div[@class='top']/div[@class='right']/span[@class='celly houseRoomCount']/span/span/text()").get()
            apartmentPrice = apartment.xpath(".//div[@class='top']/span/text()").get()
            apartmentPropertyType = apartment.xpath(
                ".//section[@class='middle sibling']/div[@class='top']/div[@class='left']/span[1]/text()").get()
            apartmentAdvertDate = apartment.xpath(
                ".//section[@class='upper sibling']/div[@class='top']/span[@class='list-view-date']/text()").get()
            apartmentLocation = apartment.xpath(
                ".//section[@class='bottom sibling']/div[@class='left']/section/div[@class='list-view-location']/span/text()").get()
            yield {
                'id': self.apartmentCounter,
                'apartmentImage': apartmentImage,
                'apartmentAdvertTitle': self.apartmentAdvertTitleClear(apartmentAdvertTitle),
                'apartmentSize': self.apartmentSizeClear(apartmentSize),
                'numberOfApartmentRooms': NumberOfApartmentRooms,
                'apartmentPrice': self.apartmentPriceClear(apartmentPrice),
                'apartmentPropertyType': self.apartmenPropertyTypeClear(apartmentPropertyType),
                'apartmentLocation': self.apartmentLocationClear(apartmentLocation),
                'apartmentAdvertDate': self.apartmentAdvertDateClear(apartmentAdvertDate),

            }
            self.apartmentCounter += 1

        nextPage = response.xpath(
            "//a[@class='he-pagination__navigate-text he-pagination__navigate-text--next']/@href").get()
        if nextPage:
            fullLink = f"https://www.hepsiemlak.com{nextPage}"
            yield scrapy.Request(url=fullLink, callback=self.parse)
