import requests
from settings import SiteSettings
import json

site = SiteSettings()


def _hotels_photo(hotel_id: str, data_arrival: str, data_departure: str, success=200):

	url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/getHotelDetails"

	querystring = {
		"hotel_id": hotel_id,
		"arrival_date": data_arrival,
		"departure_date": data_departure,
		"languagecode": "en-us",
		"currency_code": "USD"}

	headers = {
		"X-RapidAPI-Key": site.api_key.get_secret_value(),
		"X-RapidAPI-Host": site.host_api
	}

	response = requests.get(url, headers=headers, params=querystring)

	status_code = response.status_code
	if status_code == success:
		response = response.json()
		return response

	return "Error"


class HotelPhoto:

	@staticmethod
	def hotels_photo():
		return _hotels_photo


if __name__=="__main__":
	_hotels_photo()

	HotelPhoto()
