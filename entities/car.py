import random


class Car(object):
    def __init__(self, id: str, seats: int):
        self.id = id
        self.seats = seats
        self.journey = None
        self.available = True

    def __repr__(self):
        return f'<<<Car id:{self.id}, seats:{self.seats}, journey:{self.journey}, available:{self.available}>>>'
