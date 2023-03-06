import argparse
import os
import pickle
import re
import socket as socket

import entities.car as ec
import entities.journey as ej

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Car pooling client")
    parser.add_argument('-s', '--size', type=int, required=True, choices=range(1, 5), help="client journey size")
    parser.add_argument('-p', '--port', default=os.getenv('PORT', '8080'), type=int, help="server port")
    parser.add_argument('-a', '--address', default=os.getenv('HOST', 'localhost'), type=str, help="server address")
    args = parser.parse_args()

    ipv = socket.AF_INET  # use ipv4 socket
    if args.address.startswith('::') or re.match(r"\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b", args.address):
        ipv = socket.AF_INET6  # use ipv6 socket

    if os.getenv('HOST') is not None:
        args.address = 'server'

    # create journey as required
    journey = ej.Journey(args.size)

    with socket.socket(ipv, socket.SOCK_STREAM) as sock:
        # connect to server
        sock.connect((args.address, int(args.port)))
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
