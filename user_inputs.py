from common import common_functions
import numpy as np
FIELDS = [
    'institution.displayName',
    'institution.schoolType',
   
    'ranking.sortRank',
   
]

DETAILED = False
DETAIL_FIELDS = [
   
    'School Website'
]

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}


def scrapping_caching_universities():
    """
    The function mainly works in concurrence with the common functions files, mainly with the 'fetch_results_page' function.
    Once we get the dictionary with a list of different types of universities and the their rankings we have to sort them. This function does
    and returns a sorted dictonary as can be noted
    Args:
        return: Sorted dictonary with universities sorted based on the rankings from the USNews.com.
    """
    keys_dict = FIELDS + (DETAIL_FIELDS if DETAILED else [])
    url = 'https://www.usnews.com/best-colleges/api/search?_sort=schoolName&_sortDirection=asc&_page=1'
    CACHE_FILE_NAME = 'Universities.json'
    json_dict = common_functions().load_cache(CACHE_FILE_NAME)
    if len(json_dict) == 0:
        json_dict = dict(zip(keys_dict, ([] for _ in keys_dict)))    
        common_functions().fetch_results_page(url, json_dict)
        common_functions().save_cache(CACHE_FILE_NAME, json_dict)
    else:
        print("using cache for finiding the list of top universities")
    
    keys = list(set(json_dict['institution.schoolType']))
    final_dict = dict(zip(keys, ({} for _ in keys)))
    for i in range(len(json_dict['institution.displayName'])):
        rank_sorted = json_dict['ranking.sortRank'][i]
        if int(rank_sorted) >0:
            final_dict[json_dict['institution.schoolType'][i]][json_dict['institution.displayName'][i]] = int(rank_sorted)
    
    final_dict_sorted = {}
    for k, v in final_dict.items():
        if v:
            temp_dict = sorted(v.items(), key=lambda x:x[1])
            final_dict_sorted[k] = np.array(temp_dict)[:, 0]
    return final_dict_sorted

def inputs(final_dict_sorted):
    """
    
    Parameters
    ----------
    final_dict_sorted : sorted dictionary
        Dictionary that contains information regarding types of universites and their ranks.

    Returns
    -------
    name: str
        Name of the university user has chosen.
    research: str
        Research Area user has entered
        

    """

    
    all_universities = list(final_dict_sorted.keys())
    print("These are the different kind of universities we scrapped:")
    for i in range(len(all_universities)):
        print("{}.{}".format(i+1, all_universities[i]))
    while True:
        select_type = input("Please select the type of university you are looking for:")
        if select_type.isdigit() and int(select_type) >= 1 and int(select_type) <= 9:
            select_type = int(select_type)
            break
        else:
            print("Please Enter a Number between 1 and 10.")

    university_type = final_dict_sorted[all_universities[select_type - 1]]

    while True:
        rank_range = input("Please Enter a number between 1 to {} to see that many number of universities:".format(len(university_type)))
        if rank_range.isdigit() and int(rank_range) <= len(university_type):
            rank_range = int(rank_range)
            break
        else:
            print("Please Enter a valid number between 1 to {}".format(len(university_type)))
    print("These are the top {} universities in {} :".format(rank_range, (all_universities)[select_type - 1]) )
    temp_list = university_type[:rank_range]
    for i in range(len(temp_list)):
        print("{}.{}".format(i+1, temp_list[i]))
    while True:
        rank_university = input("Please give the number for university you are interested to find professors in: ")
        if rank_university.isdigit() and int(rank_university) <= len(temp_list):
            rank_university = int(rank_university)
            break
        else:
            print("Please Enter a valid number between 1 to {}".format(len(temp_list)))
    research_area = input("Please enter the research area you are interested in:")

    name = university_type[rank_university - 1]
    return name, research_area