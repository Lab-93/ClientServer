#!/bin/python3

"""
"""

# python.socket; for connecting and communicating with TCP servers.
from socket import socket
from socket import AF_INET as TCP
from socket import SOCK_STREAM as STREAM

# python.json; for reading and writing data to the web or a stream.
from json import loads as deserialize

# python.time.sleep; for maintaining memory access.
from time import sleep


class dataPacket:
    """
    The dataPayload is an object representing the queue of data streaming from
    the hub socket server; it accepts a single argument: payload, which is a
    KV store of data pertinent to many potential clients through the use of
    `sub-packeting`.

    Within the payload dictionary are several nested dictionaries segregated
    by subject matter, such as finance or linguistics.  This structure future-
    proofs the system for reusability of the API server on any other project
    going forward.


    There is also a buffer system in place for managing persistent data that
    degrades over time; such as if you're trying to calculate moving cross
    averages.  Each key in this dictionary is an integer value denoting
    the maximum amount of minutes the buffer can hold a unit of data.

    For example, the dataPayload.buffers[6] list will hold the most recent
    unit for 6 minutes before it is removed from the stack.  Same with the
    dataPayload.buffers[192] list; which persists for 192 minutes.
    """


    def __init__( self,
                  initial_payload: dict={},
                  host: str = "127.0.0.1",
                  port: int = 65535    ) -> None:

        # The payload is a dictionary container for sub-packeted data.
        self.payload = initial_payload

        # Open a connection with the socket server @ host:port;
        with socket( TCP, STREAM ) as server:

            # Attempt to initiate contact with server through connection;
            try: server.connect( host, port )
            except Exception as error: return error

            while True: 
                self.payload = deserialize( server.recv( 1024 )\
                                                  .decode()      )
                sleep(.3)

