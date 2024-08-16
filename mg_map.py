from handle_json import read_json_return_dict
from web import format_embed
import discord

def map_to_embed(map_name, interaction):
    map_returned = return_map(map_name=map_name)
    map_image = map_returned[1]
    map_climates = map_returned[2]
    map_climates_string = "\n".join(map_climates)
    map_scenario = map_returned[3]
    map_id = map_returned[4]

    if ("http" in map_id):
        map_link = f"{map_id}"
    else:
        map_link = f"https://steamcommunity.com/sharedfiles/filedetails/?id={map_id}"

    map_file = discord.File(f"images/maps/{map_image}")
    map_description = f"Map Climates: {map_climates_string}\n\n[Map Link](<{map_link}>)"

    embed = format_embed(interaction=interaction, title=map_name, description=map_description)
    embed.set_image(url=f"attachment://{map_image}")
    embed.set_footer(text=map_scenario)
        
    return [map_file, embed]

def link_to_map(map_name):
    # Splits to id&searchtext
    map_id = map_name.rsplit('?id=', 1)
    # Filters to id, searchtext
    map_id = map_id[1].rsplit('&', 1)
    # Grabs just the ID
    map_id = map_id[0]

    map_dict = grab_maps(1)
    map_ids = map_dict[1]

    print(map_id)

    if (map_id not in map_ids.keys()):
        raise Exception("This link is not supported, or malformed.")

    map_name = list(map_ids[map_id].keys())

    print(map_name)

    if (len(map_name) == 1):
        map_name = map_name[0]
    else:
        map_name = map_name

    return map_name

def dict_init(dict, key):

    dict[key] = {}

    return dict

def grab_maps(type=0):
    maps_dict = read_json_return_dict("maps")

    # Needed for the ability to use a steam link instead of map name
    maps_dict_links = {}

    # need to initialise the dict for each key first, really can not be bothered writing a proper method for it
    for map_name in maps_dict:
        map_id = maps_dict[map_name]["id"]
        dict_init(maps_dict_links, map_id)

    # cry harder
    for map_name in maps_dict:
        map_id = maps_dict[map_name]["id"]
        maps_dict_links[map_id].update({map_name: ""})

    if (type == 0):
        return maps_dict
    else:
        return [maps_dict, maps_dict_links]   

def map_exists(maps_dict=None, map_name=None):
    if (maps_dict == None):
        maps_dict = grab_maps()

    # if map does exist, a key exception will not be raised and true will be returned
    try:
        map_validation = maps_dict[map_name]

        return True
    except:
        raise Exception(f"Map '{map_name}' does not exist, or is not supported.")

def grab_map_image(maps_dict=None, map_name=None):
    if (maps_dict == None):
        maps_dict = grab_maps()

    map_exists(maps_dict=maps_dict, map_name=map_name)

    map_image = maps_dict[map_name]["image"]

    return map_image

def grab_map_climate(maps_dict=None, map_name=None):
    if (maps_dict == None):
        maps_dict = grab_maps()

    map_exists(maps_dict=maps_dict, map_name=map_name)

    map_climate = maps_dict[map_name]["climates"]

    return map_climate

def grab_map_scenario(maps_dict=None, map_name=None):
    if (maps_dict == None):
        maps_dict = grab_maps()

    map_exists(maps_dict=maps_dict, map_name=map_name)

    map_scenario = maps_dict[map_name]["map_name"]

    return map_scenario

def grab_map_id(maps_dict=None, map_name=None):
    if (maps_dict == None):
        maps_dict = grab_maps()

    map_exists(maps_dict=maps_dict, map_name=map_name)

    map_id = maps_dict[map_name]["id"]

    return map_id

def grab_map_names(maps_dict=None):
    if (maps_dict == None):
        maps_dict = grab_maps()

    map_keys = maps_dict.keys()

    map_names = list(map_keys)

    return map_names

def return_map(maps_dict=None, map_name=None):

    if (map_name == ""):
        return

    map_exists(maps_dict=maps_dict, map_name=map_name)

    try:
        map_image = grab_map_image(maps_dict=maps_dict, map_name=map_name)
        map_climate = grab_map_climate(maps_dict=maps_dict, map_name=map_name)
        map_scenario = grab_map_scenario(maps_dict=maps_dict, map_name=map_name)
        map_id = grab_map_id(maps_dict=maps_dict, map_name=map_name)
    except Exception as exp:
        print(exp)
    except:
        print("Something went wrong when grabbing the image, climate, id, or scenario name.")

    return [map_name, map_image, map_climate, map_scenario, map_id]

if (__name__ == "__main__"):
    maps = grab_maps(1)

    maps_dict = maps[0]
    maps_links = maps[1]

    print(maps_links)