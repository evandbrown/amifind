"""
This module provides utility functions for filtering lists of images
"""
import re

def filter_object_list(list_to_search, attr_to_filter, re_string):
    """
    Apply a regular expression to the specified attribute of each item in the
    list, returning a list of items whose attributes match the expression
    
    :param list_to_search: List to search
    :type list_to_search: list
    
    :param attr_to_filter: Attribute of each list item to apply regex to
    :type attr_to_filter: string
    
    :param re_string: Regular expression string to apply
    :type re_string: string
    """ 
    filter_re = re.compile(re_string)
    filtered = [ i for i in list_to_search if hasattr(i, attr_to_filter) and getattr(i, attr_to_filter) is not None and filter_re.match(getattr(i, attr_to_filter)) ]
    return filtered