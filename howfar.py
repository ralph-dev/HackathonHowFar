#!/usr/bin/python3

'''
Python script that outputs distance + driving time from a given origin location.

Supports (current month) to December (current year) hackathons.
Uses Google Maps API 3.x, Hackalist API 1.0 and the requests library.

this is for you peter <3
'''

import sys
import requests
from string import ascii_lowercase
from datetime import datetime

GMAPS_API_CALL_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={}&destinations={}"
HACKALIST_API_CALL_URL = "http://www.hackalist.org/api/1.0/{}/{}.json"


def get_travel_info(orig, dest):
    return requests.get(GMAPS_API_CALL_URL.format(orig, dest)).json()


def get_hackathon_info(year, month):
    return requests.get(HACKALIST_API_CALL_URL.format(year, month)).json()


def simplify_hackathon_name(h):
    '''desensitize hackathon name keys for easier end-user lookup'''
    return ''.join([c for c in h.lower() if c in ascii_lowercase])


def retrieve_hackathon_info():
    hackathons, now = dict(), datetime.now()
    print("Downloading hackathon info from this month ({}) to the end of year {}..."
          .format(now.month, now.year))
    for i in range(now.month, 13):
        for h in list(get_hackathon_info(now.year, str(i).zfill(2)).values())[0]:
            hackathons[simplify_hackathon_name(h['title'])] = h
    return hackathons


def verify_correct(loc_str):
    '''prompt user to verify whether input addresses were mapped correctly'''
    if not loc_str:
        return False
    return input("Is [{}] correct? (y/n): ".format(loc_str)).lower() == 'y'


def main():
    origin, do_origin_query = None, True
    try:
        with open('howfar_origin.txt', 'r') as f:
            print("Detected saved origin location information.")
            origin = f.read().strip()
            do_origin_query = not verify_correct(origin)
    except FileNotFoundError:
        print("Unable to locate saved origin location information.")

    if do_origin_query:
        while(True):
            print("Where are you travelling to hackathons from?")
            input_origin = input('> ')
            origin = get_travel_info(input_origin, 'usa')["origin_addresses"][0]
            if verify_correct(origin):
                with open('howfar_origin.txt', 'w') as f:
                    f.write(origin)
                break

    hackathons = retrieve_hackathon_info()

    while(True):
        raw_name = input("\nEnter hackathon name, or Q to exit: ").strip()
        if raw_name.lower() == 'q':
            break

        try:
            # h = hackathons[simplify_hackathon_name(raw_name)]
            h = next(v for k, v in hackathons.items() if simplify_hackathon_name(raw_name) in k)
            print("\n{} is located in {}.".format(h['title'], h['city']))
            print("Duration: ({} - {})".format(h['startDate'], h['endDate']))
            print("Website: {}".format(h['url']))

            travel_info = get_travel_info(origin, h['city'])
            dist_metric = travel_info['rows'][0]['elements'][0]['distance']['text']
            dist_imperial = round(float(''.join([c for c in dist_metric if c.isdigit()])) * 0.621371, 2)
            commute_time = travel_info['rows'][0]['elements'][0]['duration']['text']
            print("Distance from you: {} / {} mi".format(dist_metric, dist_imperial))
            print("Approx. commute time: {}".format(commute_time))

        except StopIteration:
            print("[{}] invalid or not found.".format(raw_name))

    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
