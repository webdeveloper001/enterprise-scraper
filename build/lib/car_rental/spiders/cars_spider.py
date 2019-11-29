import scrapy
import urllib
import json
from car_rental.items import CarRentalItem
import datetime
import time

indexDate = {}
count = 0
class CarsSpider(scrapy.Spider):
    name = "cars"
# frmdata = {"id": "com.supercell.boombeach", "reviewType": 0, "reviewSortOrder": 0, "pageNum":0}
#         url = "https://play.google.com/store/getreviews"
#         yield Request(url, callback=self.parse, method="POST", body=urllib.urlencode(frmdata))

    def start_requests(self):
        count = 0
        indexStr = "{}T12:00"
        indexDate = datetime.datetime.now()
        indexDate = indexDate + datetime.timedelta(days = 1)
        fromDate = indexDate.strftime("%Y-%m-%d")
        indexDate = indexDate + datetime.timedelta(days = 1)
        toDate = indexDate.strftime("%Y-%m-%d")
        url1Format = 'https://prd-west.webapi.enterprise.com/enterprise-ewt/enterprise/reservations/initiate?locale=en_US&1562055819682';

        frmdata = {
            "pickupLocation": {
                "id":"1044943",
                "name":"San Francisco Union Square",
                "latitude":"37.7849",
                "longitude":"-122.4102",
                "type":"BRANCH",
                "locationType":"BRANCH",
                "dateTime": indexStr.format(fromDate),
                "countryCode":""
                },
            "returnLocation": {
                "id":"1044943",
                "name":None,
                "latitude":"37.7849",
                "longitude":"-122.4102",
                "type":"BRANCH",
                "locationType":"BRANCH",
                "dateTime": indexStr.format(toDate),
                "countryCode":""
            },
            "contract_number": None,
            "renter_age":25,
            "country_of_residence_code":"US",
            "enable_north_american_prepay_rates":False,
            "sameLocation":True,
            "view_currency_code":"USD",
            "additional_information":[]
        }
        header = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        yield scrapy.Request(url=url1Format, callback=self.initParse, method="POST", headers=header, body=json.dumps(frmdata), meta = {'from': fromDate, 'to': toDate, 'count': count})
        
    def initParse(self, response):
        print(response.body)

        url2Format = "https://prd-west.webapi.enterprise.com/enterprise-ewt/enterprise/reservations/vehicles/availability?&now={}&locale=en_US"
        url2 = url2Format.format(int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()))
        header = {
            "Accept": "*/*",
            "Origin": "https://www.enterprise.ca",
            "Referer": "https://www.enterprise.ca/en/reserve.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        yield scrapy.Request(url=url2, callback=self.parse, method="GET", headers= header, meta = response.meta)

    def parse(self, response):
        
        if 'code' not in json.loads(response.body):
            for data in json.loads(response.body)['availablecars']:
                carItem = CarRentalItem()
                carItem['pickupDate'] = response.meta['from'];
                carItem['returnDate'] = response.meta['to'];
                carItem['carClass'] = data['name']
                carItem['carType'] = data['make_model_or_similar_text']

                if data['charges']:
                    if data['charges']['PAYLATER']:
                        carItem['totalPrice'] = data['charges']['PAYLATER']['total_price_view']['amount']
                        if(data['charges']['PAYLATER']['rates']):
                            carItem['dailyPrice'] = data['charges']['PAYLATER']['rates'][0]['unit_amount_payment']['amount']
                            yield carItem
        count = response.meta['count'];
        if count <= 90:
            count += 1
            # print datetime
            indexStr = "{}T12:00"
            fromDate = datetime.datetime.strptime(response.meta['from'], '%Y-%m-%d') + datetime.timedelta(days = 1)
            toDate = fromDate + datetime.timedelta(days = 1)
            fromDate = datetime.datetime.strftime(fromDate, '%Y-%m-%d')
            toDate = datetime.datetime.strftime(toDate, '%Y-%m-%d')

            urlFormat1 = 'https://prd-west.webapi.enterprise.com/enterprise-ewt/enterprise/reservations/initiate?locale=en_US&{}';
            url1 = urlFormat1.format(int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()));
            frmdata = {
                "pickupLocation": {
                    "id":"1044943",
                    "name":"San Francisco Union Square",
                    "latitude":"37.7849",
                    "longitude":"-122.4102",
                    "type":"BRANCH",
                    "locationType":"BRANCH",
                    "dateTime": indexStr.format(fromDate),
                    "countryCode":""
                    },
                "returnLocation": {
                    "id":"1044943",
                    "name":None,
                    "latitude":"37.7849",
                    "longitude":"-122.4102",
                    "type":"BRANCH",
                    "locationType":"BRANCH",
                    "dateTime": indexStr.format(toDate),
                    "countryCode":""
                },
                "contract_number": None,
                "renter_age":25,
                "country_of_residence_code":"US",
                "enable_north_american_prepay_rates":False,
                "sameLocation":True,
                "view_currency_code":"USD",
                "additional_information":[]
            }
            header = {
                'Content-Type': 'application/json; charset=UTF-8'
            }
            yield scrapy.Request(url=url1, callback=self.initParse, method="POST", headers=header, body=json.dumps(frmdata), meta = {'from': fromDate, 'to': toDate, 'count': count})
        elif count <= 182:
            
            indexStr = "{}T12:00"
            if count == 91:
                indexDate = datetime.datetime.now()
                indexDate = indexDate + datetime.timedelta(days = 1)
                fromDate = indexDate.strftime("%Y-%m-%d")
                indexDate = indexDate + datetime.timedelta(days = 2)
                toDate = indexDate.strftime("%Y-%m-%d")
            else:
                fromDate = datetime.datetime.strptime(response.meta['from'], '%Y-%m-%d') + datetime.timedelta(days = 1)
                toDate = fromDate + datetime.timedelta(days = 2)
                fromDate = datetime.datetime.strftime(fromDate, '%Y-%m-%d')
                toDate = datetime.datetime.strftime(toDate, '%Y-%m-%d')
            count += 1
            urlFormat1 = 'https://prd-west.webapi.enterprise.com/enterprise-ewt/enterprise/reservations/initiate?locale=en_US&{}';
            url1 = urlFormat1.format(int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()));
            frmdata = {
                "pickupLocation": {
                    "id":"1044943",
                    "name":"San Francisco Union Square",
                    "latitude":"37.7849",
                    "longitude":"-122.4102",
                    "type":"BRANCH",
                    "locationType":"BRANCH",
                    "dateTime": indexStr.format(fromDate),
                    "countryCode":""
                    },
                "returnLocation": {
                    "id":"1044943",
                    "name":None,
                    "latitude":"37.7849",
                    "longitude":"-122.4102",
                    "type":"BRANCH",
                    "locationType":"BRANCH",
                    "dateTime": indexStr.format(toDate),
                    "countryCode":""
                },
                "contract_number": None,
                "renter_age":25,
                "country_of_residence_code":"US",
                "enable_north_american_prepay_rates":False,
                "sameLocation":True,
                "view_currency_code":"USD",
                "additional_information":[]
            }
            header = {
                'Content-Type': 'application/json; charset=UTF-8'
            }
            yield scrapy.Request(url=url1, callback=self.initParse, method="POST", headers=header, body=json.dumps(frmdata), meta = {'from': fromDate, 'to': toDate, 'count': count})
        elif count <= 274:
            
            indexStr = "{}T12:00"
            if count == 183:
                indexDate = datetime.datetime.now()
                indexDate = indexDate + datetime.timedelta(days = 1)
                fromDate = indexDate.strftime("%Y-%m-%d")
                indexDate = indexDate + datetime.timedelta(days = 7)
                toDate = indexDate.strftime("%Y-%m-%d")
            else:
                fromDate = datetime.datetime.strptime(response.meta['from'], '%Y-%m-%d') + datetime.timedelta(days = 1)
                toDate = fromDate + datetime.timedelta(days = 7)
                fromDate = datetime.datetime.strftime(fromDate, '%Y-%m-%d')
                toDate = datetime.datetime.strftime(toDate, '%Y-%m-%d')
            count += 1
            urlFormat1 = 'https://prd-west.webapi.enterprise.com/enterprise-ewt/enterprise/reservations/initiate?locale=en_US&{}';
            url1 = urlFormat1.format(int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()));
            frmdata = {
                "pickupLocation": {
                    "id":"1044943",
                    "name":"San Francisco Union Square",
                    "latitude":"37.7849",
                    "longitude":"-122.4102",
                    "type":"BRANCH",
                    "locationType":"BRANCH",
                    "dateTime": indexStr.format(fromDate),
                    "countryCode":""
                    },
                "returnLocation": {
                    "id":"1044943",
                    "name":None,
                    "latitude":"37.7849",
                    "longitude":"-122.4102",
                    "type":"BRANCH",
                    "locationType":"BRANCH",
                    "dateTime": indexStr.format(toDate),
                    "countryCode":""
                },
                "contract_number": None,
                "renter_age":25,
                "country_of_residence_code":"US",
                "enable_north_american_prepay_rates":False,
                "sameLocation":True,
                "view_currency_code":"USD",
                "additional_information":[]
            }
            header = {
                'Content-Type': 'application/json; charset=UTF-8'
            }
            yield scrapy.Request(url=url1, callback=self.initParse, method="POST", headers=header, body=json.dumps(frmdata), meta = {'from': fromDate, 'to': toDate, 'count': count})

        # for 