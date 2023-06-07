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

        # The buffers offer stacks for staging timeseries data for the designated time.
        self.buffers = {
            6:  [], 12: [], 24:  [],
            48: [], 96: [], 192: [],
        }

        self.incrementLoad(self.stream(host, port))


    def stream( self, host, port ) -> bytes:
        """
        The dataPayload.stream object defines an asynchronous socket connection that continously reads bytecode
        from the line and captures it as a .payload object ready to return to the user.  The data retrieved
        during the process is fed as the only argument to dataPayload.incrementLoad in a constant loop.
        """

        # Open a connection with the socket server @ host:port;
        with socket( TCP, STREAM ) as server:

            # Attempt to initiate contact with server through connection;
            try: server.connect( host, port )
            except Exception as error: return error

            while True: yield bytes( server.recv( 1024 ) ); sleep(.3)


    def incrementLoad( self, artifact: bytes ) -> None:
        """
        As new data is introduced to the stack, defined as an `artifact`, the current payload
        must be updated to reflect the incoming artifact and added to the appropriate buffers.

        As new data is introduced to the buffer, the buffer must be trimmed of any values that
        exceed its threshold.
        """


        def update_buffer( buffer: list = [ 0, 1, 2, 3, 4, 5 ],
                                 limit:  int = 4                      ) -> None:
            """
            To determine if a value should be removed from the buffer, subtract
            the first number in the buffer from the last, and if the difference
            is greater than the integer value of the name of the buffer then
            delete the first value in the buffer.  Repeat as needed.
            """
            while buffer[ -1 ] - buffer[ 0 ] > int( limit ): del buffer[ 0 ]; sleep(.3)


        # Decode and deserialize the bytes artifact and load it to memory.
        self.payload = deserialize( artifact.decode() )


        ''' Feed the artifact into the buffer, updating each as needed. '''
        '''
        for buffer in self.buffers\
                          .keys():

            # Append JSON artifact to each timeseries buffer.
            self.buffers[ buffer ]\
                .append( artifact )

            update_buffer(self.buffers[ buffer ])
        '''
