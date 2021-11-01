from typing import Dict
from ..text import snakecase


BASE_URL = "https://raw.communitydragon.org/"


def join_set_data(data: Dict, set: int, collection_key: str):
    set = int(max(data["sets"], key=int)) if set == -1 else set
    collected = {}
    for set_data in data["setData"]:
        if set_data["number"] != set:
            continue
        for item in set_data[collection_key]:
            collected[item["apiName"]] = item
    for item in data["sets"][str(set)][collection_key]:
        collected[item["apiName"]] = item
    return list(collected.values())


def abs_url(link: str, version="latest") -> str:
    '''Return the CDragon url for the given tft asset url'''
    if link is None: return link
    link = link.lower()
    if link[-3:] not in ["png","jpg","jpeg"]:
        link = link[:-3] + "png"
    return BASE_URL + version + "/game/" + link


def sanitize_item(string: str, obj: dict) -> str:
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


def sanitize_champion(string: str, list_of_obj: list) -> str:
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
