from mappy_utils import closest_vel_from_colour, load_colour_mappings, gimmejson, chunkify
from midi_writer import MIDIFile

# load all colour mappings into an array
colour_mappings = load_colour_mappings()

# Load preset grid mapping
mappingjson = gimmejson("grid_mappings/launchpadmini.json")
gridx, gridy = mappingjson["grid"]
devices = mappingjson["devices"]
pixels = mappingjson["pixels"]

device_colour_mapping = [] 
for device in devices:
    # Creates array entry for each device with its colour mapping
    # inefficient for significantly large numbers of devices
    # implement lookup system?
    dcm = device["colour_mapping"]
    found = False
    for cm in colour_mappings:
        if cm[0] == dcm:
            device_colour_mapping.append(cm[1])
            found = True
    if (not found):
        device_colour_mapping.append([])

# Chunkify pixel map into array[y][x]
pixelmap = chunkify(pixels, gridx)

# Helper method to get chunk x,y instead of y,x 
def get_pixel_device_xy(x, y) -> dict:
    return pixelmap[y][x]

# x, y, colour, miditime
test_pixels = [
    [0, 0, (255, 255, 255), 0],
    [7, 0, (255, 255, 255), 0],
    [0, 7, (255, 255, 255), 0],
    [7, 7, (255, 255, 255), 0],
    [3, 3, (190, 200, 255), 0],
    [3, 4, (190, 200, 255), 0],
    [4, 3, (190, 200, 255), 0],
    [4, 4, (190, 200, 255), 0],
]

f_bpm = 60

MF = MIDIFile(len(devices))

#for i in range(0, devices):
#    MF.add_tempo(i, 0, f_bpm)

MF.add_tempo(0, 0, f_bpm)

for pixel in test_pixels:
    # Get data from array
    px = pixel[0]
    py = pixel[1]
    ptarget_col = pixel[2]
    ptime = pixel[3]
    # Get pixel data
    pxy = get_pixel_device_xy(px, py)
    # Get note for pixel
    p_note = pxy["note"]
    # Get device id on pixel
    pd_id = pxy["device"]
    # Get colour mapping
    pd_colmap = device_colour_mapping[pd_id]
    # Get colour
    pd_vel = closest_vel_from_colour(pd_colmap, ptarget_col)
    # Get channel and track
    pd_channel = devices[pd_id]["channel"]
    pd_track = pd_id
    p_duration = 1
    # Add note to file
    MF.add_note(pd_track, pd_channel, p_note, ptime, p_duration, pd_vel)
    print(pd_track, pd_channel, p_note, ptime, p_duration, pd_vel)

with open("test.mid", "wb") as out_file:
    MF.write_file(out_file)
    out_file.close()