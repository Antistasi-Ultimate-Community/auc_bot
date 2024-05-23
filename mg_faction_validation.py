from mg_common_vars import *

def validate_faction_dlc(faction_dlc, desired_dlc=[""]):
    if (desired_dlc == [""]):
        return True

    if (isinstance(desired_dlc, list)):
        for dlc in faction_dlc:
            if (dlc in desired_dlc):
                return True

        return False

    if (faction_dlc == desired_dlc):
        return True
    else:
        return False

def validate_faction_era(faction_era, desired_era=""):
    if (desired_era == ""):
        return True

    if (faction_era in desired_era):
        return True
    else:
        return False

def validate_faction_key(faction_key, desired_key=""):
    if (desired_key == ""):
        return True

    if (faction_key == ""):
        return True

    if (faction_key == desired_key):
        return True
    else:
        return False

def validate_faction_climate(faction_climate, desired_climate=[""]):
    if (desired_climate == [""]):
        return True

    if (isinstance(desired_climate, list)):
        for climate in desired_climate:
            if (climate in faction_climate):
                return True

        return False

    if (desired_climate in faction_climate):
        return True
    else:
        return False

def validate_faction(faction_climates, faction_era, faction_key, faction_dlc, climates=[""], era="", key="", dlc=[""], double_occ=0):
    # print(climates, era, key, dlc, double_occ)

    validation_climate = validate_faction_climate(faction_climates, desired_climate=climates)
    validation_era = validate_faction_era(faction_era, desired_era=era)
    validation_key = validate_faction_key(faction_key, desired_key=key)
    validation_dlc = validate_faction_dlc(faction_dlc, desired_dlc=dlc)

    if (validation_climate == False or validation_dlc == False or validation_era == False or validation_key == False):
    
        return False

    return True

def validate_faction_data(faction_dict, modset_dict, climates=[""], era="", key="", dlc=[""], double_occ=0):

    for faction_type in faction_types:

        factions = list(faction_dict[faction_type].keys())

        for faction in factions:

            faction_climates = faction_dict[faction_type][faction]["climates"]
            faction_modset = faction_dict[faction_type][faction]["modset"]
            faction_dlc = faction_dict[faction_type][faction]["dlc"]

            faction_key = modset_dict[faction_modset]["type"]
            faction_era = modset_dict[faction_modset]["era"]

            # print(climates, era, key, dlc, double_occ)
            
            validation = validate_faction(faction_climates, faction_era, faction_key, faction_dlc, climates=climates, era=era, key=key, dlc=dlc, double_occ=double_occ)
            
            if (validation == False):
                del faction_dict[faction_type][faction]