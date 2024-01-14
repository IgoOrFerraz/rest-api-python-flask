from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hotels = [
            {
                'hotel_id': 'bravo',
                'name': 'Bravo Hotel',
                'stars': 4.4,
                'daily': 380.90,
                'city': 'Santa Catarina'
            },
            {
                'hotel_id': 'charlie',
                'name': 'Charlie Hotel',
                'stars': 3.9,
                'daily': 320.90,
                'city': 'Santa Catarina'
            }
        ]


class Hotels(Resource):
    def get(self):
        return {'hotels': hotels}


class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('name')
    args.add_argument('stars')
    args.add_argument('daily')
    args.add_argument('city')

    def find_hotel(hotel_id):
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if not hotel:
            return {'message': 'Hotel not found'}, 404  # not found
        return hotel

    def post(self, hotel_id):
        data = Hotel.args.parse_args()
        hotel_obj = HotelModel(hotel_id, **data)
        new_hotel = hotel_obj.json()

        hotels.append(new_hotel)
        return new_hotel, 200

    def put(self, hotel_id):
        data = Hotel.args.parse_args()
        hotel_obj = HotelModel(hotel_id, **data)
        new_hotel = hotel_obj.json()

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(new_hotel)
            return new_hotel, 200  # OK
        hotels.append(new_hotel)
        return new_hotel, 201  # created

    def delete(self, hotel_id):
        global hotels
        hotels = [hotel for hotel in hotels if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted.'}
