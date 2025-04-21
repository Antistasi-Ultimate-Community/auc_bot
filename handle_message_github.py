from web import return_url

def return_pull(pull_index=-1):
    fallback_url = "https://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/issues/#"

    if (pull_index == -1 or pull_index == "" or pull_index is None):
        raise TypeError("pull_index was not passed to return_pull function!")

        return
    else:
        url = return_url(url=f"https://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/pull/{pull_index}", suppress=False)
        
        # If URL isn't a valid pull request, perhaps it's a valid issue
        if (url == False):
            issue_url = return_url(url=f"https://github.com/SilenceIsFatto/A3-Antistasi-Ultimate/issues/{pull_index}", suppress=False)
            # If it isn't a valid issue, then we can assume it's not a valid link at all
            if (issue_url == False): # in case of false positive, pull_index is not provided. We can assume that if we're still at fallback_url, we can quit
                raise Exception("URL returned 404/was not found.")

                return
            else:
                url = issue_url

        print(f"url returned is {url}")

        if (url != fallback_url):
            return url
        else:
            raise Exception("URL was fallback, not sending")

    return False