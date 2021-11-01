

BASE_URL = "https://raw.communitydragon.org/"


def strip_k(string: str) -> str:
    '''Strips char k if string start with k'''
    if string is None: return string
    return string[1:] if string[0] == "k" else string


def abs_url(link: str, version="latest") -> str:
    '''Return the CDragon url for the given game asset url'''
    if link is None: return link
    link = link.lower()
    splited = link.split("/lol-game-data/assets/")
    if len(splited) == 2:
        return BASE_URL + version + "/plugins/rcp-be-lol-game-data/global/default/" + splited[1]
    return BASE_URL + version + "/plugins/rcp-be-lol-game-data/global/default/" + link


def sanitize(string: str) -> str:
    '''Sanitize CDragon descriptions'''
    if string is None: return string
    new_string = ""
    is_tag = False
    is_at = False
    tag = ""
    for s in string:
        if not is_tag and not is_at and s not in "<>@": new_string += s
        if s == "<": is_tag = True
        elif s == ">":
            is_tag = False
            if tag == "br" and len(new_string) > 0 and new_string[-1] != " ": new_string += "\n"
            tag = ""
        elif s == "@" and not is_at:
            is_at = True
            new_string += "(?)"
        elif s == "@": is_at = False
        if is_tag and s not in "<>": tag += s
    return new_string
