import os

from mg_modset_json import read_json_return
from mg_modset_json import read_json_return_dict

from log import log_message

from file_operations import write_to_file
from config import guild_log_file
from config import guild_log_modset_init_start
from config import guild_log_modset_init_finish

from mg_faction import return_faction_choices
from mg_faction import display_factions
from mg_faction import grab_modset

def grab_collections(modsets=[""]):
    if (len(modsets) >= 3):
        collections = {"all": "Too many modsets for auto-grab. You will have to look for them one by one.\nhttps://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/wiki/Mods"}
        return collections

    modset_dict = read_json_return_dict("modsets")
    collections = {}
    for modset in modsets:
        collection = modset_dict[modset]["collection"]
        if (collection != ""):
            collections.update({modset: collection})

    return collections

def init(modsets=[""], climates=[""], era="", key="", dlc=[""], double_occ=0, simple=False):
    # os.system('cls')
    log_message(-1, guild_log_modset_init_start, space=True)

    if (climates == ["all"]):
        climates = ["arid", "arctic", "temperate", "tropical"]

    setting_choices = read_json_return("settings", "choices")

    print(modsets)

    if (modsets == [""] or modsets[0] == "all"):
        modset = read_json_return("modsets", "modsets")
    else:
        modset = modsets

    log_message(-1, f"Final Modset(s): {modset}")
    log_message(-1, f"Climate: {climates}")
    log_message(-1, f"Era: {era}")
    log_message(-1, f"Key: {key}")
    log_message(-1, f"DLC: {dlc}")
    log_message(-1, f"Double Occ: {double_occ}")

    collections = grab_collections(modset)
    log_message(-1, collections)

    if (setting_choices <= 0):
        raise Exception("Choice is 0 or lower, please change.")

    if (setting_choices >= 100):
        raise Exception("Choice is 100 or higher, for the sake of your CPU i'm cancelling this early.")

    for i in range(setting_choices):
        factions = return_faction_choices(modset, climates=climates, era=era, key=key, dlc=dlc, double_occ=double_occ)

        message = display_factions(factions[0], factions[1], simple=simple, collections=collections)

    log_message(-1, f"{guild_log_modset_init_finish}\n")

    return message

# message = init(modsets="random_multiple", climates=["arctic"], era="lowtech", key="", dlc=["none"], double_occ=0)