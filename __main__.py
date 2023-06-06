#!/bin/python3
from .__init__ import *
from argparse import ArgumentParser

if __name__ == "__main__":
    arguments = ArgumentParser()
    arguments.add_argument("-h", "--host", default="127.0.0.1")
    arguments.add_argument("-p", "--port", default=65535)
    arguments = arguments.parse_args()

    server.run(host=arguments.host, port=int(arguments.port))
