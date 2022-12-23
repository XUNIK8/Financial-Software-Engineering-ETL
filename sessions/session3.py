from copy import deepcopy


# Tuple Q1
def tuple_types(input_tuple):
    """
    Checks every element of given tuple and reports back on its type;
    :param input_tuple: tuple
    :return: tuple; resulted tuple of types
    """
    res = list()
    for i in input_tuple:
        res.append(type(i))
    return tuple(res)


# Tuple Q2
def remove_element_tuple(input_tuple, element):
    """
    Removes an element from given tuple;
    :param input_tuple: tuple
    :param element:
    :return: tuple;resulted tuple
    """
    if element not in input_tuple:
        print(element, 'is not found.')
        return input_tuple

    element_index = input_tuple.index(element)
    return input_tuple[:element_index] + \
        input_tuple[element_index + 1:]


# String Q1
def check_containment(input_string, lookup_string):
    """
    Checks for substring availability in given string;
    :param input_string: string
    :param lookup_string: string
    :return: boolean
    """
    return lookup_string in input_string


# String Q2
def reverse(input_string):
    """
    Reverses given string;
    :param input_string: string
    :return: string
    """
    return input_string[::-1]


# List Q1
def concatenate(list1, list2):
    """
    Concatenates two lists index-wise;
    :param list1: list
    :param list2: list
    :return: list
    """
    return [[m, n] for m, n in zip(list1, list2)]


# List Q2
def concatenate_list_of_lists(input_list):
    """
    Concatenate all list elements index-wise;
    :param input_list: list;list of list
    :return: list
    """
    res_list = []
    temp_list = []

    for index in range(len(input_list[0])):
        temp_list = []
        for sub_list in input_list:
            temp_list.append(sub_list[index])
        res_list.append(temp_list)

    return res_list


# List Q3
def remove_element_list(input_list, element):
    """
    Removes an element from given list;
    :param input_list: list
    :param element: target element
    :return: list
    """
    if element in input_list:
        input_list.remove(element)
        remove_element_list(input_list, element)
    
    return input_list


# List Q4
def deep_copy(input_list):
    """
    Deep copy of given list;
    :param input_list: list
    :return: list
    """
    return deepcopy(input_list)


# Dictionary Q1
def find(input_dict, specified_key):
    """
    Find all elements with specified key; make sure to account for the case
    where given dictionary is a dict of dicts;
    Traverse all elements of inner dict elements;
    :param input_dict: dictionary
    :param selected_key:
    :return: list
    """
    res_list = []

    for key, value in input_dict.items():
        if key == specified_key:
            res_list.append(value)
        if isinstance(value, dict):
            res_list += find(value, specified_key)

    return res_list


# Dictionary Q2
def min_value(input_dict):
    """
    Returns the key, corresponding to the min value from given dictionary;
    :param input_dict: dict
    :return: 
    """
    for key, value in input_dict.items():
        if value == min(input_dict.values()):
            return key


if __name__ == "__main__":
    # Tuple Q1
    test_tuple = (1, 0.1, "fre", [1, 1], (1, 1), {'1': 11})

    print('\nTuple Q1')
    print(tuple_types(test_tuple))

    # Tuple Q2
    print('\nTuple Q2')
    print(remove_element_tuple(test_tuple, 'fre'))

    # String Q1
    test_string = "XHJ"
    sub_string = 'XH'

    print('\nString Q1')
    print(check_containment(test_string, sub_string))

    # String Q2
    print('\nString Q2')
    print(reverse(test_string))

    # List Q1
    test_list1 = [1, 1, 2]
    test_list2 = [3, 3, 4]

    print('\nList Q1')
    print(concatenate(test_list1, test_list2))

    # List Q2
    print('\nList Q2')
    print(concatenate_list_of_lists([test_list1, test_list2]))

    # List Q3
    test_element = 1

    print('\nList Q3')
    print(remove_element_list(test_list1, test_element))

    # List Q4
    print('\nList Q4')
    print(deep_copy(test_list2))

    # Dictionary Q1
    test_dict1 = {'1': 1, '2': 2, '3': {'1': 11, '2': 22}}

    print('\nDictionary Q1')
    print(find(test_dict1, '1'))

    # Dictionary Q2
    test_dict2 = {'1': 3, '2': 2, '3': 1}

    print('\nDictionary Q2')
    print(min_value(test_dict2))