import requests

from contextlib import closing

API_URL = "https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{}"
API = "d3b0e772c1d5440cb03ea495d21a2a00"


def get_wait_for_station(station_code, destination_name):
    """Given a station code and destination, return the mean wait across all
    trains across all trains."""
    with closing(requests.get(API_URL.format(station_code),
                              headers={'api_key': API})) as r:
        response = r.json()
    trains = [i for i in response["Trains"]
              if i["DestinationName"] == destination_name]
    minutes = [0 if not i["Min"].isdigit() else float(i["Min"])
               for i in trains]
    meanwait = (sum([i - j for i, j in zip(minutes, [0] + minutes[:-1])])
                / len(minutes))
    return {"meanwait": meanwait,
            "trains": minutes}
