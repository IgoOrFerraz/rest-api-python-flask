from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required


class Hotels(Resource):
    def get(self):
        return {'hotels': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('name',
                      type=str,
                      required=True,
                      help="The field 'name' cannot be left blank")
    args.add_argument('stars')
    args.add_argument('daily')
    args.add_argument('city')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel not found"}, 404  # not found

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {
                "message": "Hotel id '{}' already exists".format(hotel_id)
            }, 400

        data = Hotel.args.parse_args()
        hotel = HotelModel(hotel_id, **data)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred"}, 500
        return hotel.json()

    @jwt_required()
    def put(self, hotel_id):
        data = Hotel.args.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            # update an exists hotel
            hotel.update_hotel(**data)
            try:
                hotel.save_hotel()
            except:
                return {"message": "An internal error ocurred"}, 500
            return hotel.json(), 200
        # create a new hotel
        hotel = HotelModel(hotel_id, **data)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred"}, 500
        return hotel.json(), 201  # created

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {"message": "An internal error ocurred"}, 500
            return {"message": "Hotel deleted."}
        return {"message": "Hotel not found."}, 404
