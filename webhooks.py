from ast import literal_eval

import handle_json

def recieve_webhook(content=None, payload_type=None, author_id=None):
    if (content == None):
        raise Exception("Retrieved webhook with no content.")

    payload_filter = content.replace("\n", "")
    payload_filter = payload_filter.replace(" ", "")

    payload = payload_filter.split("+")
    payload = [index for index in payload if index != ""]

    if (author_id == 474144080801169418):
        if ("webhook" not in payload):
            return
        else:
            payload.remove("webhook")

    ## use for pythia formatted webhook
    # payload_type = payload[0]
    # payload.remove(payload_type)

    handle_payload(payload=payload, payload_type=payload_type)

    return [payload, payload_type]

def handle_payload(payload=None, payload_type=None):
    if (payload == None):
        raise Exception(f"Payload returned payload: {payload}, payload_type: {payload_type}.")

    if (payload_type == None):
        
        if (len(payload) == 3):
            user_name = payload[0]
            user_name_steam = payload[1]
            user_steamid = str(payload[2])
            user_account = f"https://steamcommunity.com/profiles/{user_steamid}/"

            user = {
                user_steamid: {
                    "name": user_name,
                    "name_steam": user_name_steam,
                    "account": user_account
                }
            }

            handle_json.update_json(data=user, file_name="members")

    # if (payload_type == "[GENERIC]"):
    #     payload_final = payload

    # if (payload_type == "[STEAMID]"):
    #     payload_final = literal_eval(payload[0])

    #     for steamid in payload_final.keys():

    #         user_steamid = str(steamid)

    #         user_name = payload_final[user_steamid]["name"]
    #         user_name_steam = payload_final[user_steamid]["name_steam"]
    #         user_account = f"https://steamcommunity.com/profiles/{steamid}/"

    #         user = {
    #             user_steamid: {"name": user_name, "name_steam": user_name_steam, "account": user_account}
    #         }

    #         handle_json.update_json(data=user, file_name="members")