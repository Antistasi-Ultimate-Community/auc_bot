from mg_modset_json import read_json_return
from mg_modset_json import read_json_return_dict

from config import guild_log_file

from log import log_message

from mg_select_random import select_random

import mg_faction_validation

from file_operations import write_to_file

from mg_common_vars import *

# from modset import *

def grab_faction_data(modset, faction_type, faction):
    faction_data = read_json_return_dict("factions", modset)

    return faction_data[faction_type][faction]

def grab_random_factions(faction_dict):
    factions = []

    for faction_type in faction_types:
        faction_values = list(faction_dict[faction_type].keys())
        if (faction_values == []):
            faction_values = ["N/A"]

        # print(faction_values)
        faction = select_random(faction_values)
        if (faction_values == ["N/A"]):
            faction_name = "N/A"
        else:
            faction_name = faction_dict[faction_type][faction]["title"]

        factions.append([faction, faction_name])
        
    return factions

def return_faction_choices(modset, climates=[""], era="", key="", dlc=[""], double_occ=0):

    modset_dict = read_json_return_dict("modsets")

    # print(climates, era, key, dlc, double_occ)

    faction_dict = grab_modset_data(modset, modset_dict)
    faction_dict_unfiltered = grab_modset_data(modset, modset_dict)

    if (double_occ == 1):
        factions_occ = faction_dict["factionsOcc"]
        factions_inv = faction_dict["factionsInv"]

        faction_dict["factionsOcc"].update(factions_inv)
        faction_dict["factionsInv"].update(factions_occ)

    mg_faction_validation.validate_faction_data(faction_dict, modset_dict, climates=climates, era=era, key=key, dlc=dlc, double_occ=double_occ)
    # print(faction_dict)
    factions = grab_random_factions(faction_dict)

    return [factions, faction_dict_unfiltered]

def check_forced_factions(faction, faction_dict, faction_type):
    name = ""

    if (setting_force_faction_occ != [] and faction_type == "Occ"):
        name = faction_dict[setting_force_faction_occ[0]][setting_force_faction_occ[1]]["title"]
        # name = grab_faction_object(setting_force_faction_occ[0], setting_force_faction_occ[1], setting_force_faction_occ[2], "title")

    if (setting_force_faction_inv != [] and faction_type == "Inv"):
        name = faction_dict[setting_force_faction_inv[0]][setting_force_faction_inv[1]]["title"]
    
    if (setting_force_faction_reb != [] and faction_type == "Reb"):
        name = faction_dict[setting_force_faction_reb[0]][setting_force_faction_reb[1]]["title"]
    
    if (setting_force_faction_riv != [] and faction_type == "Riv"):
        name = faction_dict[setting_force_faction_riv[0]][setting_force_faction_riv[1]]["title"]
    
    if (setting_force_faction_civ != [] and faction_type == "Civ"):
        name = faction_dict[setting_force_faction_civ[0]][setting_force_faction_civ[1]]["title"]

    if (name != ""):
        return [setting_force_faction_occ[1], name]
    else:
        return faction

def display_factions(factions, faction_dict, simple=False, collections={}):
    # log_message(1, factions)

    factions_occ = factions[0]
    factions_inv = factions[1]
    factions_reb = factions[2]
    factions_riv = factions[3]
    factions_civ = factions[4]

    factions_occ = check_forced_factions(factions_occ, faction_dict, "Occ")
    factions_inv = check_forced_factions(factions_inv, faction_dict, "Inv")
    factions_reb = check_forced_factions(factions_reb, faction_dict, "Reb")
    factions_riv = check_forced_factions(factions_riv, faction_dict, "Riv")
    factions_civ = check_forced_factions(factions_civ, faction_dict, "Civ")

    if (simple):
        message = f"\nOccupier: {factions_occ[1]}.\nInvader: {factions_inv[1]}.\nRebel: {factions_reb[1]}.\nRivals: {factions_riv[1]}.\nCivilians: {factions_civ[1]}."
        message_debug = f"\nOccupier: {factions_occ[0]}.\nInvader: {factions_inv[0]}.\nRebel: {factions_reb[0]}.\nRivals: {factions_riv[0]}.\nCivilians: {factions_civ[0]}."
    else:
        message = f"\nYour Occupier is the {factions_occ[1]}.\nyou are being invaded by the {factions_inv[1]}.\nYou'll be playing as the {factions_reb[1]} with your rivals being the {factions_riv[1]}.\nLocal civilians are {factions_civ[1]}."
        message_debug = f"\nYour Occupier is the {factions_occ[0]}.\nyou are being invaded by the {factions_inv[0]}.\nYou'll be playing as the {factions_reb[0]} with your rivals being the {factions_riv[0]}.\nLocal civilians are {factions_civ[0]}."

    collections_list = list(collections.values())
    message = f"{message}\n\nTo play these factions, you will need:"
        
    for collection in collections_list:
        if (len(collections) <= 1):
            message = f"{message}\n{collection}"
        else:
            message = f"{message}\n<{collection}>"

    log_message(-1, "Writing file with modset data.")
    log_message(-1, f"Final factions: {factions_occ[0]}, {factions_inv[0]}, {factions_reb[0]}, {factions_riv[0]}, {factions_civ[0]}")

    return message

def grab_modset_data(modset, modset_dict):

    faction_dict = {"factionsOcc": {}, "factionsInv": {}, "factionsReb": {}, "factionsRiv": {}, "factionsCiv": {}}

    if (isinstance(modset, list)):
        for faction_type in faction_types:
            for mod in modset:
                mod_factions = modset_dict[mod][faction_type]

                if ("None" in mod_factions):
                    continue

                for faction in mod_factions:
                    faction_data = grab_faction_data(mod, faction_type, faction)
                    faction_dict[faction_type].update({faction: faction_data})
                    faction_dict[faction_type][faction].update({"modset": mod})

    return faction_dict

def grab_modset(modset=""):
    if (modset == ""):

        setting_modsets = read_json_return("settings", "modsets")

        if (setting_modsets == "random"):
            modset = modset_factions.grab_random_modset("modsets", "modsets", random_modset=setting_modsets)
        elif (setting_modsets == "random_multiple"):
            modset = read_json_return("modsets", "modsets")
        else:
            modset = setting_modsets

    return modset