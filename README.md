# Car Pooling App

Car Pooling App is a prototype application that allows users to book trips based on group size,
in order to contribute to environment and reduce the carbon footprint

## Installation Guide

```bash
git clone https://github.com/igncarrillo/final-comp2.git
```

```bash
cd final-comp2
```

Build server image

```bash
docker build --rm -f Dockerfile.server -t server_image:latest .
```

Start the server

```bash
docker-compose up --build
```

Build client image

```bash
docker build --rm -f Dockerfile.client -t client_image:latest .
```

Run client containers with desired journey size (-s = 1 on this example)

```bash
docker run -it --network client-server --env-file .env client_image:latest -s 1
```

## Environment Variables

You should set the following environment variables to your `.env` file to run server.\
If not set on clients, they will try to connect on `localhost` and port `8080` by default

`HOST`

`PORT`

## Features

- Multithreading TCP Socket Server -ipv4 and ipv6 ready-
- Async pool of process for Car Pooling functions
- Thread and Process safe by IPC as shared memory and locks.
- Client arguments parser
- Pickle serialization and deserialization
- Docker ready

## Documentation

- [socketserver](https://docs.python.org/3/library/socketserver.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [threading](https://docs.python.org/3/library/threading.html)
- [pickle](https://docs.python.org/3/library/pickle.html)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [docker](https://docs.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)

## Development Issues

- [docker ipv6 network on macos](https://github.com/docker/for-mac/issues/1432)

