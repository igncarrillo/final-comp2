import os
import pickle
import socketserver as ss
import threading

from dotenv import load_dotenv

defaultHost = 'localhost'
defaultPort = '8080'


# custom handle method
class ThreadingTCPHandler(ss.BaseRequestHandler):
    def handle(self):
        # read msg
        print(f"[NEW CONNECTION] --> thread: {threading.current_thread()}")
        party = pickle.loads(self.request.recv(1024))
        print(f"|--> message received: {party} |--> from client: {self.client_address}, ")
        # answer msg
        self.request.sendall(pickle.dumps(party))


# ss with threads to handle new connections
class ThreadingTCPServer(ss.ThreadingMixIn, ss.TCPServer):
    allow_reuse_address = True  # avoid waiting kernel to flush unused address
    daemon_threads = True  # it will exit immediately at shut down


if __name__ == '__main__':
    # read .env file
    load_dotenv()
    host = os.getenv('HOST', defaultHost)
    port = os.getenv('PORT', defaultPort)

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
