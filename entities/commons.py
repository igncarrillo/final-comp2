import os
import re
import socket

__defaultHost__ = '::1'
__defaultPort__ = '8080'
__defaultCarsQuantity__ = 5


def fillValues():
    host = os.getenv('HOST', __defaultHost__)
    port = os.getenv('PORT', __defaultPort__)

    ipv = socket.AF_INET  # use ipv4 socket
    if host.startswith('::') or re.match(r"\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b", host):
        ipv = socket.AF_INET6  # use ipv6 socket

    print(f"{host},int({port}),{ipv}")
    return host, int(port), ipv
