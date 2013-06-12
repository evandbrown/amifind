"""
This module provides utility functions for filtering lists of images
"""
import re

def filter_object_list(list, attr_to_filter, filter_re_string):
    """
    Apply a regular expression to the specified attribute of each item in the
    list, returning a list of items whose attributes match the expression
    """
    filtered = [ i for i in list if hasattr(i, attr_to_filter) and getattr(i, attr_to_filter) is not None and re.match(filter_re_string, getattr(i, attr_to_filter)) ]
    return filtered