import uuid

import entities.car

flatRate = 2


class Receipt(object):
    def __init__(self, time: float, car: entities.car.Car):
        self.id = uuid.uuid4().__str__()
        self.car = car
        self.journey = car.journey
        self.flatRate = flatRate
        self.time = time
        self.total = flatRate * self.time

    def __repr__(self):
        return f'\n+++++++++++++++++++++++' \
               f'\nReceipt id:{self.id}' \
               f'\nAssigned Car: {self.car.id}' \
               f'\nJourney: {self.journey.id}' \
               f'\nTrip time: {self.time}s' \
               f'\nRate: ${self.flatRate}/s' \
               f'\nTotal: ${self.total}' \
               f'\n+++++++++++++++++++++++'
