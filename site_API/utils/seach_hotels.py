from settings import SiteSettings
import requests
from typing import Dict


site = SiteSettings()


def _make_response(url: str, params: Dict, success=200):
    headers = {
        "X-RapidAPI-Key": site.api_key.get_secret_value(),
        "X-RapidAPI-Host": site.host_api
    }

    response = requests.get(url, headers=headers, params=params)

    status_code = response.status_code
    if status_code == success:
        return response

    return "Error"


def _seach_city_requests(city: str) -> str:
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"

    params = {"query": city}

    response = _make_response(url, params)
    if response == "Error":
        return response

    else:
        response = response.json()
        # dest_id = response
        # dest_id = dest_id["data"][0]["dest_id"]
        return response


def _seach_hotel_response(dest_id: str, data_arrival: str, data_departure: str, price_min=None, price_max=None):

    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"

    params = {
        "dest_id": dest_id,
        "search_type": "CITY",
        "arrival_date": data_arrival,
        "departure_date": data_departure,
        "adults": "2", "children_age": None,
        "room_qty": "1", "page_number": "1",
        "price_min": price_min,
        "price_max": price_max,
        "languagecode":"ru",
        "currency_code":"USD"}

    response = _make_response(url, params)
    if response == "Error":
        return response
    else:
        hotels = response.json()
        return hotels


class SiteApiInterface:

    @staticmethod
    def seach_hotel_response():
        return _seach_hotel_response

    @staticmethod
    def seach_city_requests():
        return _seach_city_requests



if __name__ == "__main__":
    _seach_hotel_response()
    _make_response()
    _seach_city_requests()

    SiteApiInterface()
