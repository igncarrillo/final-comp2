import argparse
import pickle
import socket as socket

import entities.car as ec
import entities.commons as commons
import entities.journey as ej

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Car pooling client")
    parser.add_argument('-s', '--size', type=int, required=True, choices=range(1, 5), help="client journey size")
    args = parser.parse_args()

    host, port, ipv = commons.fill_values()
    if host != commons.__defaultHost__:
        host = 'server'

    # create journey as required
    journey = ej.Journey(args.size)

    print(f"{host}:{port} -> ipv {ipv}")
    with socket.socket(ipv, socket.SOCK_STREAM) as sock:
        # connect to server
        sock.connect((host, port))
        # send request
        sock.sendall(pickle.dumps(journey))

        # receive data from server
        while True:
            msg = sock.recv(1024)
            if not msg:
                break
            rsp = pickle.loads(msg)
            if type(rsp) == ec.Car:  # if car is assigned
                k = input(f"you are on car {rsp.id}\npress enter key to finish the trip...\n")
                sock.sendall(pickle.dumps(k))
                rsp = pickle.loads(sock.recv(1024))
            print(rsp)
