import multiprocessing
import os
import pickle
import socketserver as ss
import threading
import time

from dotenv import load_dotenv

import entities.car as ec
import entities.receipt as er

__defaultHost__ = 'localhost'
__defaultPort__ = '8080'
__defaultCarsQuantity__ = 5


def assign_car(j):
    # try to assign the next available car with as few seats as possible
    with cars_lock:
        car_id = next((key for key, value in cars_st.items() if value.seats >= j.size and value.available), None)
        if car_id:
            begin = time.time()
            # permutation to edit shared dict
            to_edit = cars_st[car_id]
            to_edit.available = False
            to_edit.journey = j
            cars_st[car_id] = to_edit
            return cars_st[car_id], begin
        else:
            return None, None


def leave_car(car_id):
    with cars_lock:
        # permutation to edit shared dict
        to_edit = cars_st[car_id]
        to_edit.journey = None
        to_edit.available = True
        cars_st[car_id] = to_edit
    return time.time()


def print_receipt(t, car):
    return f"Your trip is over\n" \
           f"Here is your receipt: " \
           f"{er.Receipt(t, car)}"


# custom handler
class ThreadingTCPHandler(ss.BaseRequestHandler):
    def handle(self):
        # read msg
        print(f"[NEW CONNECTION] --> thread: {threading.current_thread()}")
        journey = pickle.loads(self.request.recv(1024))
        print(f"|--> message received: {journey} |--> from client: {self.client_address}, ")
        car, b = assign_car(journey)
        if car:
            self.request.sendall(pickle.dumps(car))  # assigned car
            self.request.recv(1024)  # wait keyboard input
            f = leave_car(car.id)  # leave the car
            self.request.sendall(pickle.dumps(print_receipt(f - b, car)))  # send receipt
        else:
            self.request.sendall(pickle.dumps("No available car now for the required journey size, try again later"))


# ss with threads to handle new connections
class ThreadingTCPServer(ss.ThreadingMixIn, ss.TCPServer):
    allow_reuse_address = True  # avoid waiting kernel to flush unused address
    daemon_threads = True  # it will exit immediately at shut down

    # wrap constructor to add mp pool
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.pool = multiprocessing.Pool()  # as many pool process as cpu cores


if __name__ == "__main__":
    # read .env file
    load_dotenv()
    host = os.getenv('HOST', __defaultHost__)
    port = os.getenv('PORT', __defaultPort__)

    # shared on memory storage
    cars_st = multiprocessing.Manager().dict()
    cars_st.update(ec.create_cars_st(__defaultCarsQuantity__))

    # shared lock
    cars_lock = multiprocessing.Manager().Lock()

    # create server and bind at host on port
    with ThreadingTCPServer((host, int(port)), ThreadingTCPHandler) as server:
        server.pool.apply_async(assign_car)
        server.pool.apply_async(leave_car)
        server.pool.apply_async(print_receipt)

        # activate server, it will keep running until keyboard interruption
        print("WELCOME TO THE CAR POOLING APP")
        print(cars_st)
        print(f"server listening on {host}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Server is shutting down...")
        finally:
            server.pool.terminate()  # forcefully terminate all child worker
            server.shutdown()
