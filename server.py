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
cars_st = ec.create_cars_st(3)  # todo lock storage


def assign_car(rq, j):
    # try to assign the next available car with as few seats as possible
    car = next((value for key, value in cars_st.items() if value.seats >= j.size and value.available), None)
    if car:
        begin = time.time()
        car.available = False
        car.journey = j
        print("storage_updated: ", cars_st)
        rq.sendall(pickle.dumps(car))
        leave_car(rq, car, begin)
    else:
        rq.sendall(pickle.dumps("No available car now for the required journey size, try again later"))


def leave_car(rq, car, b):
    rq.recv(1024)
    msg = f"Your trip is over." \
          f"Receipt: " \
          f"{er.Receipt(time.time() - b, car)}"
    rq.sendall(pickle.dumps(msg))
    car.journey = None
    car.available = True
    print("storage_updated: ", cars_st)


# custom handle method
class ThreadingTCPHandler(ss.BaseRequestHandler):
    def handle(self):
        # read msg
        print(f"[NEW CONNECTION] --> thread: {threading.current_thread()}")
        journey = pickle.loads(self.request.recv(1024))
        print(f"|--> message received: {journey} |--> from client: {self.client_address}, ")
        assign_car(self.request, journey)


# ss with threads to handle new connections
class ThreadingTCPServer(ss.ThreadingMixIn, ss.TCPServer):
    allow_reuse_address = True  # avoid waiting kernel to flush unused address
    daemon_threads = True  # it will exit immediately at shut down


if __name__ == '__main__':
    # read .env file
    load_dotenv()
    host = os.getenv('HOST', __defaultHost__)
    port = os.getenv('PORT', __defaultPort__)
    print("cars_storage: ", cars_st)

    # create server and bind at host on port
    with ThreadingTCPServer((host, int(port)), ThreadingTCPHandler) as server:
        # activate server, it will keep running until keyboard interruption
        print("WELCOME TO THE CAR POOLING APP")
        print(f"server listening on {host}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Server is shutting down...")
        finally:
            server.shutdown()
