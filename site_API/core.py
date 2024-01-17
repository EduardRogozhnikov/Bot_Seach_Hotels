from site_API.utils.seach_hotels import SiteApiInterface
from site_API.utils.get_hotels_photo import HotelPhoto


hotelphoto = HotelPhoto()
siteApi = SiteApiInterface()


def _hotels(dest_id, data_arrival, data_departure, price_min, price_max, limit):
    hotels = siteApi.seach_hotel_response()
    photos = hotelphoto.hotels_photo()
    if hotels == "Error":
        return hotels

    hotels = hotels(dest_id, data_arrival, data_departure, price_min, price_max)
    answer = {}

    count = 0
    if len(hotels["data"]["hotels"]) == 0:
        return "empty"

    for hotel in hotels["data"]["hotels"]:

        id_hotel = hotel['hotel_id']
        description = hotel["accessibilityLabel"]

        photo = photos(id_hotel, data_arrival, data_departure)
        if photo == "Error":
            answer[count] = {photo: "Ошибка, не удалось получить фото."}

        else:
            photo_list = []
            photo_count = 0

            key_photos = [key for key, value in photo["data"]["rooms"].items()]
            key_photos = key_photos[0]

            for i_elem in photo["data"]["rooms"][key_photos]["photos"]:
                photo_list.append(i_elem["url_original"])
                photo_count += 1

                if photo_count == 7:
                    break

            answer[count] = {
                "id_hotel": id_hotel,
                "description": description,
                "url": photo["data"]["url"],
                "photo": photo_list
            }

        count += 1
        if limit == count:
            break

    return answer


class HotelCore():

    @staticmethod
    def hotels():
        return _hotels


if __name__ == "__main__":
    _hotels()

    HotelCore()
