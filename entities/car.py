import random
import uuid


class Car(object):
    def __init__(self, seats: int):
        self.id = uuid.uuid4().__str__()
        self.seats = seats
        self.journey = None
        self.available = True

    def __repr__(self):
        return f'<<<Car id:{self.id}, seats:{self.seats}, journey:{self.journey}, available:{self.available}>>>'


def create_cars_st(qty):
    # create cars from one to six seats and return ordered asc by seats
    local_st = {car.id: car for car in [Car(random.randint(1, 6)) for car in range(qty)]}
    return {k: v for k, v in sorted(local_st.items(), key=lambda cars: cars[1].seats)}
