from mg_modset_json import read_json_return

faction_types = ["factionsOcc", "factionsInv", "factionsReb", "factionsRiv", "factionsCiv"]

all_dlc = ["vanilla", "ws", "gm", "vn", "none"]
all_climates = ["arid", "arctic", "temperate", "tropical"]
all_modsets = read_json_return("modsets", "modsets")

setting_force_faction_occ = read_json_return("settings", "force_faction_occ")
setting_force_faction_inv = read_json_return("settings", "force_faction_inv")
setting_force_faction_reb = read_json_return("settings", "force_faction_reb")
setting_force_faction_riv = read_json_return("settings", "force_faction_riv")
setting_force_faction_civ = read_json_return("settings", "force_faction_civ")

setting_debug_level = read_json_return("settings", "debug_level")