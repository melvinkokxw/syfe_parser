import json

def reit_lookup(text):
    with open('reit_lookup.json') as json_file: 
        lookup_dict = json.load(json_file)
    return lookup_dict.get(text, "PLEASE DEFINE SYMBOL IN LOOKUP.JSON")