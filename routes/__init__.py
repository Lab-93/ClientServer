#!/bin/python3


"""
Flask Route Definition.
At it's most basic, the api is a Flask server that streams the various segments
within `data.payload` to the appropriate url for interpretation on their end.

Behind the scenes, the data payload is recieving serialized dictionaries from
a socket server acting as mediator between any other one-off scripts posting
to the same server.  
"""



from .. import server, data

# python.flask; for building our own http API and URI.
from flask import Response
from flask import stream_with_context as flask_stream



@server.route("/<asset>/live-data/")
def liveAuctionDataServer(asset):
    """
    The liveAuctionDataServer route view gives a dynamic chart generated by a stream_with_context
    instance of a generator constantly reading from the data packet.
    """

    def ChartData(asset):
        """
        The liveAuctionDataServer.ChartData function provides a constant, steady stream
        of time-series data points representing the live fluctuations of the asset market
        as they happen.

        Data is returned as a streamable object given to chart.js on the front-end to help
        visualise the assets proceedings over time.
        """

        # In a loop, check for a new instance of 'Live Market Data'.
        while True:
            if data[ "Live Market Data" ]:
                # If it exists, then return it to the caller.
                yield data[ "Live Market Data" ]\
                          [ asset.upper()\
                                 .replace( "-", "/" ) ]


    response = Response( flask_stream( ChartData() ),
                         mimetype="text/event-stream"        )

    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"

    return response
