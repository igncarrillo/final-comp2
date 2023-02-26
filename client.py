import pickle
import socket as socket
import argparse
from entities.journey import Journey

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Car pooling client")
    parser.add_argument('-s', '--size', type=int, required=True, choices=range(1, 5), help="client journey size")
    parser.add_argument('-p', '--port', type=int, required=True, help="server port")
    parser.add_argument('-a', '--address', type=str, required=True, help="server address")

    args = parser.parse_args()
    journey = Journey(args.size)
    print(f"{journey} created successfully")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # connect to server
        sock.connect((args.address, args.port))
        # send request
        sock.sendall(pickle.dumps(journey))

        # receive data from server
        while True:
            msg = sock.recv(1024)
            if not msg:
                break
            print(pickle.loads(msg))
