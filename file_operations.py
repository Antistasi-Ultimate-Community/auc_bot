import os

def write_to_file(filename="output", data="", type="a+"):
    with open(f"{filename}", type) as file:
        for line in data:
            file.write(str(line) + "\n")