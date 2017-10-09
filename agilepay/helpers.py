from __future__ import print_function

import json




def dicts_merge(*dicts):
    """
    Merge an undefined number of dicts

    :return:
    :rtype: dict
    """
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result


def dict_to_json(dictionary):
    """
    Turn a dictionary into a json

    note separators=(',', ':') is required
    this will get rid of a space after the colons
    that json.dumps add by default ex : {"key": "value"}

    :param dictionary:
    :param dictionary: dict
    :return:
    :rtype str
    """

    return json.dumps(dictionary, separators=(',', ':'))


def is_json(string):
    """
    Whether the provided string is a json

    :param string:
    :return: bool
    """

    try:
        json.loads(string)
    except ValueError, e:
        return False
    return True


def json_to_dict(string):
    """
    Turns a json into a dictionary

    :param string:
    :return: dict
    """

    return json.loads(string)


def print_dict(dictionary):
    print(json.dumps(dictionary, indent=4))
