#!/usr/bin/python3

'''
this is for you peter
'''

import sys
import requests

API_CALL_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units={}&origins={}&destinations={}"


def get_response(origin, destination, use_metric=False):
    return requests.get(API_CALL_URL.format('metric' if use_metric else 'imperial',
                        origin, destination)).json()


def verify_correct(loc_str):
    if not loc_str:
        return False
    return input("Is [{}] correct? (y/n): ".format(loc_str)).lower() == 'y'


def main():
    origin, destination, do_origin_query = None, None, True
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
            origin = get_response(input_origin, 'usa')["origin_addresses"][0]
            if verify_correct(origin):
                with open('howfar_data.txt', 'w') as f:
                    f.write(origin)
                break

    while(True):
        h_name = input("Enter hackathon name, or Q to exit: ").strip().lower()
        if h_name == 'q':
            break

        #

    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
