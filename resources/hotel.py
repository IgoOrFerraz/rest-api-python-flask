from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required


def normalize_path_params(city=None,
                          stars_min=0,
                          stars_max=5,
                          daily_min=0,
                          daily_max=10000,
                          limit=50,
                          offset=0, **data):
    if city:
        return {
            'stars_min': stars_min,
            'stars_max': stars_max,
            'daily_min': daily_min,
            'daily_max': daily_max,
            'city': city,
            'limit': limit,
            'offset': offset}
    return {
        'stars_min': stars_min,
        'stars_max': stars_max,
        'daily_min': daily_min,
        'daily_max': daily_max,
        'limit': limit,
        'offset': offset}


class Hotels(Resource):
    query_params = reqparse.RequestParser()
    query_params.add_argument("city",
                              type=str,
                              default="",
                              location="args")
    query_params.add_argument("stars_min",
                              type=float,
                              default=0,
                              location="args")
    query_params.add_argument("stars_max",
                              type=float,
                              default=0,
                              location="args")
    query_params.add_argument("daily_min",
                              type=float,
                              default=0,
                              location="args")
    query_params.add_argument("daily_max",
                              type=float,
                              default=0,
                              location="args")

    def get(self):
        filters = Hotels.query_params.parse_args()
        query = HotelModel.query

        if filters["city"]:
            query = query.filter(HotelModel.city == filters["city"])
        if filters["stars_min"]:
            query = query.filter(HotelModel.stars >= filters["stars_min"])
        if filters["stars_max"]:
            query = query.filter(HotelModel.stars <= filters["stars_max"])
        if filters["daily_min"]:
            query = query.filter(HotelModel.daily >= filters["daily_min"])
        if filters["daily_max"]:
            query = query.filter(HotelModel.daily <= filters["daily_max"])

        return {"hotels": [hotel.json() for hotel in query]}


class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('name',
                      type=str,
                      required=True,
                      help="The field 'name' cannot be left blank")
    args.add_argument('stars')
    args.add_argument('daily')
    args.add_argument('city')
    args.add_argument('site_id',
                      type=int,
                      required=True,
                      help="Every hotel needs to be linked")

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

        if not SiteModel.find_by_id(data['site_id']):
            return {"message": "Site not found"}, 404  # not found

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
