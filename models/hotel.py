from sql_alchemy import database


class HotelModel(database.Model):
    __tablename__ = 'hotels'

    hotel_id = database.Column(database.String, primary_key=True)
    name = database.Column(database.String(80))
    stars = database.Column(database.Float(precision=1))
    daily = database.Column(database.Float(precision=2))
    city = database.Column(database.String(40))
    site_id = database.Column(database.Integer,
                              database.ForeignKey('sites.site_id'))

    def __init__(self, hotel_id, name, stars, daily, city, site_id):
        self.hotel_id = hotel_id
        self.name = name
        self.stars = stars
        self.daily = daily
        self.city = city
        self.site_id = site_id

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'stars': self.stars,
            'daily': self.daily,
            'city': self.city,
            'site_id': self.site_id
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        database.session.add(self)
        database.session.commit()

    def update_hotel(self, name, stars, daily, city):
        self.name = name
        self.stars = stars
        self.daily = daily
        self.city = city

    def delete_hotel(self):
        database.session.delete(self)
        database.session.commit()
