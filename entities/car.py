import uuid


class Car(object):
    def __init__(self, seats: int):
        self.party = None
        self.id = uuid.uuid4()
        self.seats = seats
        self.available = True
