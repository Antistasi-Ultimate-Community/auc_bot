from ast import literal_eval

import handle_json

def recieve_webhook(content=None):
    if (content == None):
        raise Exception("Retrieved webhook with no content.")

    print(content)

    payload_filter = content.replace("\n", "")
    payload_filter = payload_filter.replace(" ", "")

    payload = payload_filter.split("+")
    payload = [index for index in payload if index != ""]

    payload_type = payload[0]

    payload.remove(payload_type)

    payload_final = handle_payload(payload=payload, payload_type=payload_type)

    return [payload, payload_type, payload_final]

def handle_payload(payload=None, payload_type=None):
    if (payload == None or payload_type == None):
        raise Exception(f"Payload returned payload: {payload}, payload_type: {payload_type}.")

    if (payload_type == "[GENERIC]"):
        payload_final = payload

    if (payload_type == "[STEAMID]"):
        payload_final = literal_eval(payload[0])

        for steamid in payload_final.keys():

            user_steamid = str(steamid)

            user_name = payload_final[user_steamid]["name"]
            user_name_steam = payload_final[user_steamid]["name_steam"]
            user_account = f"https://steamcommunity.com/profiles/{steamid}/"

            user = {
                user_steamid: {"name": user_name, "name_steam": user_name_steam, "account": user_account}
            }

            handle_json.update_json(data=user, file_name="members")

    print(payload_final)