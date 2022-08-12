import os
import json


def GetConfig(config_path):
    '''
    Extracts user variables from json dictionary.
    Args:
        config_path: <string> config file path
    Returns:
        <dict> user variables dictionary
    '''
    if config_path:
        with open(config_path, 'r') as file:
            return json.load(file)
