import json
import os

path = os.getcwd()
# path = os.getcwd() + "\modset_generator"

def validate_key(dict, key, value_default):

    if (dict == value_default):
        raise KeyError(f"Key {key} was not found.")

def read_json_return_dict(file_name, key="", value_default="default_return"):

    # json.loads is a beautiful thing honestly. 
    # Can't believe it took me this long to try it out
    
    with open(f'{path}/json/{file_name}.json', 'r') as file:

        read_file = file.read()
        dict = json.loads(read_file)

        if (key != ""):

            if (isinstance(key, list)): # if key is a list
                if (len(key) > 2): exit() # exit early if list has more than 2 elements

                dict = dict.get(key[0], value_default)

                validate_key(dict, key[0], value_default)

                try:
                    dict = dict[key[1]]
                    
                    return dict
                except KeyError:
                    raise KeyError(f"Key {key[1]} was not found. ( {key[0]} >> {key[1]} )")
                except:
                    raise Exception("Something went wrong.")

            dict = dict.get(key, value_default)

            validate_key(dict, key, value_default)
        else:
            return dict

    return dict

def save_json(data, file_name):

    with open(f'{path}/json/{file_name}.json', 'w+') as file:
        json.dump(data, file, indent=4)

def read_json(file_name):
    with open(f'{path}/json/{file_name}.json', 'r') as file:
        y = json.load(file)

    return y

def read_json_return(file_name, data):
    if ("/" in file_name):
        
        with open(f'json/{file_name}', 'r') as file:
            x = json.load(file)

    else:

        with open(f'{path}/json/{file_name}.json', 'r') as file:
            x = json.load(file)

    if (data not in x):
        x.update({data: ""})

    y = x[data]

    return y

def update_json(data, file_name):

    print(data)

    try:

        with open(f'{path}/json/{file_name}.json', 'r') as file:
            y = json.load(file)

        y.update(data)

        save_json(y, file_name)

    except:
        print("Woops!")
        # prompt.user_error("Error", "Something went wrong whilst saving settings. Some things may still work. Try creating an empty packer.json file")