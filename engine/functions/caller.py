#!/usr/bin/env python

"""
Helper module to manage imports of awe function and their pipelined calls.
"""

from bs4 import BeautifulSoup
import importlib


def run_pipeline(data):
    """
    Main method to run each tag through its pipeline.

    Parameters:
        data <dict> Contains the HTML snippet along with a str list of its pipeline

    Return:
        <dict> The same data but with the snippet fixed
    """
    if type(data) is dict:
        # running pipeline of indirect functions
        data["snippet"] = BeautifulSoup(data["snippet"], "html.parser").find()

        return _compose_pipeline(data["pipeline"])(data)
    else:
        # running pipeline of direct functions
        data.tag_data["snippet"] = BeautifulSoup(
            data.tag_data["snippet"], "html.parser"
        ).find()

        return _compose_pipeline(data.tag_data["pipeline"])(data)


def _compose_pipeline(function_names):
    """
    Changes the str list of function names into curried pipeline function
    ['a', 'b', 'c'] -> a.run(b.run(c.run(x)))

    Parameters:
        pipeline <list> List of the function names the snippet must go through

    Return:
        <function> Curried pipelined function calls the snippet will go through
    """
    if len(function_names) == 0:
        return lambda x: x

    function_list = tuple(_import_function(name) for name in function_names)

    def compose(acc, x, function_list):
        if not function_list:
            return acc.run(x)
        return acc.run(compose(function_list[0], x, function_list[1:]))

    return lambda x: compose(function_list[0], x, function_list[1:])


def _import_function(function_name):
    """
    Imports the received function name dynamically and returns the module.

    Parameters:
        function_name <str> name of the module to import

    Return:
        <function> The run function of the imported module
    """
    parent = ".".join(__name__.split(".")[:-1])
    module_name = function_name.replace("-", "_")
    return importlib.import_module(f"{parent}.{module_name}.{module_name}")
