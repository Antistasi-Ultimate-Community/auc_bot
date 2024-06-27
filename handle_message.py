from handle_message_github import return_pull

def has_identifier(message=0, identifier=""):
    if (message == 0):
        raise TypeError("No message was passed to the has_identifier function!")

    if (identifier == ""):
        raise TypeError("No identifier was passed to the has_identifier function!")

    if (identifier in message):
        return True

    return False

def identifier_is_github(content=None):
    if (content == None):
        return False

    is_pull = has_identifier(content, "##")
    
    return is_pull

def identifier_github(content=None):
    if (content == None):
        return False

    # Split all content that isn't related to a pull request index
    pull_index_filter = content.split(" ")
    
    # Filter the resulting list to remove any elements that don't have the identifier
    index = [index for index in pull_index_filter if "##" in index][0]
    
    pull_index = index.split("##")[1]

    url = return_pull(pull_index=pull_index)

    return url