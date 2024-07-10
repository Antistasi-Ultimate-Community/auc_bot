from web import return_url

def return_pull(pull_index=-1):
    if (pull_index == -1):
        raise TypeError("pull_index was not passed to return_pull function!")
    else:
        url = return_url(url=f"https://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/pull/{pull_index}", suppress=True)
        
        # If URL isn't a valid pull request, perhaps it's a valid issue
        if (url == False):
            issue_url = return_url(url=f"https://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/issues/{pull_index}", suppress=True)
            # If it isn't a valid issue, then we can assume it's not a valid link at all
            if (issue_url == False):
                raise Exception("URL returned 404/was not found.")
            else:
                url = issue_url

        return url

    return False