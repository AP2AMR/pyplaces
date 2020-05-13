import requests
import json
import time
import csv
class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details
if __name__ == '__main__':
    api = GooglePlaces("AIzaSyC4D5cHGJeug9PpA9lbSfi08aK6EM9CLlY")
    places = api.search_places_by_coordinate("40.662298,-73.931464", "500", "hospital")
    fields = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']
    for place in places:
        details = api.get_place_details(place['place_id'], fields)
        with open('test.csv', mode='w') as csv_file:
            fieldnames = ['Name', 'Website', 'Address', 'Phone Number']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            try:
                website = details['result']['website']
            except KeyError:
                website = ""

            try:
                name = details['result']['name']
            except KeyError:
                name = ""

            try:
                address = details['result']['formatted_address']
            except KeyError:
                address = ""

            try:
                phone_number = details['result']['international_phone_number']
            except KeyError:
                phone_number = ""

            try:
                reviews = details['result']['reviews']
            except KeyError:
                reviews = []
            writer.writerow({'Name': name, 'Website': website, 'Address': address, 'Phone Number': phone_number})
