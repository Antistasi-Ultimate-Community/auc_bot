def has_identifier(message=0, identifier=""):
    if (message == 0):
        raise TypeError("No message was passed to the has_identifier function!")

    if (identifier == ""):
        raise TypeError("No identifier was passed to the has_identifier function!")

    if (identifier in message):
        return True

    return False