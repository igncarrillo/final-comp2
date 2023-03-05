import csv
import sys

import entities.car as ec

__filename__ = 'cars.csv'


def get_from_csv():
    try:
        with open(__filename__, newline='') as file:
            cars = []
            for row in csv.DictReader(file):
                cars.append(ec.Car(row['id'], row['seats']))
            return {k: v for k, v in sorted({car.id: car for car in cars}.items(), key=lambda cars: cars[1].seats)}
    except FileNotFoundError:
        print(f"try to read from csv failed. {__filename__} not found")
        sys.exit(1)
