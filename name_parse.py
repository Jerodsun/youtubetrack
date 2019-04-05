"""
Supporting functions to get and parse names.

Using the ProPublica Congress API, these functions return different name variations.

"""
from congress import Congress
from secrets import api_key_congress

congress = Congress(api_key_congress)

def get_names(house = "house", nametype = "official"):
    members = get_members(house)
    if nametype == "official":
        return official(members)
    elif nametype == "partisan":
        return officialwparty(members)
    elif nametype == "unofficial":
        return unofficial(members)
    elif nametype == "neutral":
        return neutral(members)
    else: return officialwparty(members)


def get_members(chamber):
    """Specify house or senate for members"""
    members = congress.members.filter(chamber = chamber)[0]["members"]
    return members


def official(namelist):
    """
    Returns the list of formal names of all members of Congress in a specific chamber.
    Ex. Rep. Bill Flores
    """
    official = ["".join([i["short_title"], " ", i["first_name"], " ", i["last_name"]]) for i in namelist]
    return official

def officialwparty(namelist):
    """official, except with party mapped and name MAPPED.
    
    Ex. """
    
    partymap = [{"name": "".join([i["short_title"], " ", i["first_name"], " ", i["last_name"]]), "party" : i["party"]}  for i in namelist]
    
    return partymap
    

def unofficial(namelist):
    """
    Returns a partisan-defined list of all members of Congress in a specific chamber.
    In general, adding Democrat/Republican increases political sensitivity and entrenchedness.
    
    Ex. Democrat Alma Adams
    """
    unofficial = ["".join(["Democrat" if i["party"] == "D" else "Republican" if i["party"] == "R" else "", " ", i["first_name"], " ", i["last_name"]]) for i in namelist]
    return unofficial


def neutral(namelist):
    """
    Returns a politically neutral list of all members of Congress in a specific chamber by state.
    Ex. John Barrasso WY
    """
    neutral = ["".join([i["first_name"], " ", i["last_name"], " ", i["state"]]) for i in namelist]
    return neutral

if __name__ == "__main__":
    house_members, senate_members = get_members("house"), get_members("senate")
    official_house = official(house_members)
    official_senate = official(senate_members)
