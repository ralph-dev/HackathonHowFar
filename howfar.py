#!/usr/bin/python3

'''
this is for you peter <3
note: 2016 August - December hackathons ONLY, for now
'''

# TODO add support for 2017 when they release the new jsons

import sys
import requests
from string import ascii_lowercase

GMAPS_API_CALL_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units={}&origins={}&destinations={}"
HACKALIST_API_CALL_URL = "http://www.hackalist.org/api/1.0/2016/{}.json"


def get_gmaps_response(origin, destination, use_metric=False):
    return requests.get(GMAPS_API_CALL_URL.format('metric' if use_metric else 'imperial',
                        origin, destination)).json()


def simplify_hackathon_name(h):
    '''desensitize key lookup so user can make more
    mistakes when entering hackathon name'''
    return ''.join([c for c in h.lower() if c in ascii_lowercase])


def retrieve_hackathon_info():
    hackathons = dict()
    for i in range(8, 13):  # aug to dec 2016
        month = str(i).zfill(2)
        for h in list(requests.get(HACKALIST_API_CALL_URL.format(month)).json().values())[0]:
            hackathons[simplify_hackathon_name(h['title'])] = h
    return hackathons


def verify_correct(loc_str):
    if not loc_str:
        return False
    return input("Is [{}] correct? (y/n): ".format(loc_str)).lower() == 'y'


def main():
    origin, do_origin_query = None, True
    try:
        with open('howfar_data.txt', 'r') as f:
            print("Detected saved origin location information.")
            origin = f.read().strip()
            do_origin_query = not verify_correct(origin)
    except FileNotFoundError:
        print("Unable to locate saved origin location information.")

    if do_origin_query:
        while(True):
            print("Where are you travelling to hackathons from?")
            input_origin = input('> ')
            origin = get_gmaps_response(input_origin, 'usa')["origin_addresses"][0]
            if verify_correct(origin):
                with open('howfar_data.txt', 'w') as f:
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
            travel_info = get_gmaps_response(origin, h['city'])
            print("Distance:", travel_info['rows'][0]['elements'][0]['distance']['text'])
            print("Approximate commute time:", travel_info['rows'][0]['elements'][0]['duration']['text'])
        except StopIteration:
            print("[{}] invalid or not found.".format(raw_name))

    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
