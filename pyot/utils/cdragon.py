from .common import snakecase


_base_url = "https://raw.communitydragon.org/latest/"

def start_k(string: str) -> str:
    '''Removes k if string start with k'''
    if string is None: return string
    return string[1:] if string[0] == "k" else string


def cdragon_url(link: str) -> str:
    '''Return the CDragon url for the given game asset url'''
    if link is None: return link
    link = link.lower()
    if len(link.split("/lol-game-data/assets/")) == 2:
        link = _base_url+ "plugins/rcp-be-lol-game-data/global/default/" + link.split("/lol-game-data/assets/")[1]
    return link


def tft_url(link: str) -> str:
    '''Return the CDragon url for the given tft asset url'''
    if link is None: return link
    link = link.lower()
    if link[-3:] not in ["png","jpg","jpeg"]:
        link = link[:-3] + "png"
    link = _base_url + "game/" + link
    return link


def cdragon_sanitize(string: str) -> str:
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
            if tag == "br" and len(new_string) > 0 and new_string[-1] != " ": new_string += " "
            tag = ""
        elif s == "@" and not is_at:
            is_at = True
            new_string += "(?)"
        elif s == "@": is_at = False
        if is_tag and s not in "<>": tag += s
    return new_string


def tft_item_sanitize(string: str, obj: dict) -> str:
    '''Sanitize CDragon tft item descriptions'''
    if string is None: return string
    new_string = ""
    is_tag = False
    is_at = False
    is_percent = False
    percent = ""
    tag = ""
    at = ""
    for s in string:
        if not is_tag and not is_at and not is_percent and s not in "<>@": new_string += s
        if s == "<": is_tag = True
        elif s == ">":
            is_tag = False
            if tag == "br" and len(new_string) > 0 and new_string[-1] != " ": new_string += " "
            tag = ""
        elif s == "@" and not is_at: is_at = True
        elif s == "@":
            is_at = False
            try: new_string += str(obj[at])
            except KeyError: new_string += "(?)"
            at = ""
        elif s == "%": is_percent = True
        elif is_percent and s == " " and percent == "":
            is_percent = False
            new_string += s
        elif s == "%" and is_percent and len(percent) > 1:
            is_percent = False
            new_string = new_string[:-1]
        if is_tag and s not in "<>": tag += s
        if is_at and s != "@": at += s
        if is_percent and s != "%": percent += s
    return new_string


def tft_champ_sanitize(string: str, list_of_obj: list) -> str:
    '''Sanitize CDragon tft champion descriptions'''
    if string is None: return string
    new_string = ""
    is_tag = False
    is_at = False
    tag = ""
    at = ""
    for s in string:
        if not is_tag and not is_at and s not in "<>@": new_string += s
        if s == "<": is_tag = True
        elif s == ">":
            is_tag = False
            if tag == "br" and len(new_string) > 0 and new_string[-1] != " ": new_string += " "
            tag = ""
        elif s == "@" and not is_at: is_at = True
        elif s == "@":
            is_at = False
            tags = snakecase(tag).split("_")
            found = False
            for t in tags:
                for obj in list_of_obj:
                    if t in snakecase(obj["name"]):
                        new_string += "/".join([str(vall) for vall in obj["value"][1:4]])
                        found = True
                        break
                if found: break
            if not found: new_string += "(?)"
            at = ""
        if is_tag and s not in "<>":
            tag += s
        if is_at and s != "@":
            at += s
    return new_string
