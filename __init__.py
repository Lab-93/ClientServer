#!/bin/python3
"""
The back-end api provides a uniform interface for retrieving information the system produces as output.  At a very
high level, it's a URL based filesystem indexing information conjured on the fly; or it's a handy way to remember
exactly *what* can be conjured, at any given point.

To give an example of it's behavior, one could go to the address:
                                                              `https://api.guyyatsu.me/finance/btc-usd/live-data/charts`

to watch the price of Bitcoin change in real time valued in terms of US Dollars; while the address:
                                                                      `https://api.guyyatsu.me/occult/tarot/trumps/xii`

would bring up all the information related to the Death card in Tarot.


Getting more technical with it, it combines a Flask Web Server with a TCP/IP Socket Server to act as a hub for 
daemons running in the background to report their work as it's produced to then be picked up by clients as it's
requested.
"""


# python.flask; for building our own http API and URI.
from flask import Flask
from .payload import *

# Define our Flask instance as `server`, out of convention.
server = Flask(__name__)
from .routes import *

# Define our data object, so we have access to a static `data.payload` object.
data = dataPacket()
