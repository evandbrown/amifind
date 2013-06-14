"""
This module provides utility functions for filtering lists of images
"""
import re
import exceptions

def filter_object_list(list_to_filter, attr_to_filter, re_string):
    """
    Apply a regular expression to the specified attribute of each item in the
    list, returning a list of items whose attributes match the expression
    
    :param list_to_filter: List to search
    :type list_to_filter: list
    
    :param attr_to_filter: Attribute of each list item to apply regex to
    :type attr_to_filter: string
    
    :param re_string: Regular expression string to apply
    :type re_string: string
    """
    
    if list_to_filter is None or len(list_to_filter) == 0:
        raise exceptions.AMIFilterException("Can't filter empty list.")
    
    filter_re = re.compile(re_string)
    filtered = [ i for i in list_to_filter if getattr(i, attr_to_filter) is not None and filter_re.match(getattr(i, attr_to_filter)) ]
    return filtered
    
def sort_object_list(list_to_sort, attr_to_sort_on, descending=False):
    
    # No empty lists
    if list_to_sort is None or len(list_to_sort) == 0:
        raise exceptions.AMIFilterException("Can't filter empty list.")
        
    # Sort list. Exception will be thrown if sort attribute doesn't exist in list items
    return sorted(list_to_sort, key=lambda item: getattr(item, attr_to_sort_on), reverse=descending)