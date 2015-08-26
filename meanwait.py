import requests

from contextlib import closing

API_URL = "https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{}"
API = "d3b0e772c1d5440cb03ea495d21a2a00"


def get_wait_for_station(station_code):
    """Given a station code, return the mean wait across all trains across all
    trains."""
    with closing(requests.get(API_URL.format(station_code),
                              headers={'api_key': API})) as r:
        response = r.json()
    destinations = set(i['DestinationName']
                       for i in response["Trains"]) - set(["No Passenger"])
    destwaits = []
    for dest in destinations:
        trains = [i for i in response["Trains"]
                  if i["DestinationName"] == dest]
        minutes = [0 if not i["Min"].isdigit() else float(i["Min"])
                   for i in trains]
        destwaits.append(sum([i - j
                              for i, j in zip(minutes, [0] + minutes[:-1])])
                         / len(minutes))
    meanweight = sum(destwaits) / len(destwaits)
    return meanweight
