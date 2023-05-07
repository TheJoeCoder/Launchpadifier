from math import sqrt

from os import listdir
from os.path import isfile, splitext
from os.path import join as pathjoin

from json import loads as jloads

def closest_colour(colours: list[tuple], colour: tuple) -> tuple:
    # Finds the closest colour in the colours list to the specified colour
    # from https://stackoverflow.com/a/54242348
    # Replace with Numpy? https://stackoverflow.com/a/54244301
    r, g, b = colour
    colour_diffs = []
    for clr in colours:
        cr, cg, cb = clr
        colour_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        colour_diffs.append((colour_diff, clr))
    return min(colour_diffs)[1]

def closest_vel_from_colour(colour_mapping: dict, colour: tuple) -> int:
    # Gets closest velocity from colour mapping and colour
    colour_list = []
    vel_list = []
    for cm in colour_mapping:
        colour_list.append(cm["col"])
        vel_list.append(cm["vel"])
    found_cl = closest_colour(colour_list, colour)
    found_index = colour_list.index(found_cl)
    found_vel = vel_list[found_index]
    return found_vel

def load_colour_mappings() -> list[tuple]:
    colour_mappings = []
    for fil in listdir("colour_mappings"):
        # Get joined path
        pathjoined = pathjoin("colour_mappings", fil)
        # Is file a file and a json file?
        if (isfile(pathjoined) and splitext(fil)[1] == ".json"):
            # Import contents as JSON
            fjson = gimmejson(pathjoined)
            # Append name and values to array
            colour_mappings.append([fjson["name"], fjson["values"]])
        else:
            print("file not load", pathjoined)
    return colour_mappings

def gimmejson(filename) -> object:
    with open(filename, "r") as fil:
        mread = fil.read()
        mjson = jloads(mread)
        fil.close()
    return mjson

def chunkify(lst: list, size: int) -> list[list]:
    # Split a list into equally-sized chunks.
    # from https://stackoverflow.com/a/75855076
    chunks = []
    for i in range(0, len(lst), size):
        chunks.append(lst[i:i+size])
    return chunks