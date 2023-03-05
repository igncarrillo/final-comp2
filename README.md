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
Start the server
```bash
docker-compose up --build
```
Build client containers
```bash
docker build --rm -f Dockerfile.client -t client_image:latest .
```
Run client containers with desired journey size (-s = 1 on this example)
```bash
docker run -it --network final_client-server --env-file .env client_image:latest -s 1
```

## Environment Variables

You should set the following environment variables to your .env file

`HOST`

`PORT`


## Features

- Multithreading TCP Socket Server
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
