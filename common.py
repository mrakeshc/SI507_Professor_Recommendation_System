import json
import requests
from bs4 import BeautifulSoup
"""
Fields indicating the keys we use while scrapping the information regarding the universities
"""
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


class common_functions():
    """
    An Object that holds some commonly used function to make requests, load 
    cache, save_cache and other important function necessary for the main file
    """
    def traverse(self, root, path):
        value = root
        for segment in path.split('.'):
            if segment.isdigit():
                value = value[int(segment)]
            else:
                value = value[segment]
        return value

    #Loading the Cache
    def load_cache(self, CACHE_FILE_NAME):
        try:
            cache_file = open(CACHE_FILE_NAME, 'r')
            cache_file_contents = cache_file.read()
            cache = json.loads(cache_file_contents)
            cache_file.close()
        except:
            cache = {}
            # cache = dict(zip(keys_dict, ([] for _ in keys_dict)))

        return cache
    
    #Saving the Cache
    def save_cache(self, CACHE_FILE_NAME, cache):
        cache_file = open(CACHE_FILE_NAME, 'w')
        contents_to_write = json.dumps(cache)
        cache_file.write(contents_to_write)
        cache_file.close()
        
        
    #Loading cache for Google Scholar page
    def load_cache_scholar(self, CACHE_FILE_NAME):
        try:
            cache_file = open(CACHE_FILE_NAME, 'r')
            cache_file_contents = cache_file.read()
            cache = json.loads(cache_file_contents)
            cache_file.close()
        except:
            cache = []
        return cache
    
    
    def fetch_results_page(self, url, json_dict):
        """
        This below function is one of the main contributions in this project that scraps the USNews.com
        website to get information regarding the different kinds of universities and 
        their respective rankings in each of them.
        Args:
            inputs:
                url: link to the usnews.com website
                json_dict: A dictionary that holds the information regarding the universities (This is also the return here)
                As you can notice I used the recursion to effectivelyu load the data from different websites
        """
        print('Fetching ' + url + '...')
        resp = requests.get(url, headers=HEADERS)
        json_data = json.loads(resp.text)
        for school in json_data['data']['items']:
            for field in FIELDS:
                value = common_functions().traverse(school, field)
                json_dict[field].append(value)

            if DETAILED:
                resp = requests.get('https://www.usnews.com/best-colleges/' + common_functions().traverse(school, 'institution.urlName') + '-'
                                    + common_functions().traverse(school, 'institution.primaryKey'), headers=HEADERS)
                soup = BeautifulSoup(resp.text, 'html.parser')
                for field in DETAIL_FIELDS:
                    field_element = soup.find(text=field)
                    if field_element is None:
                        json_dict[field].append(value)
                        continue
                    parent = field_element.parent.parent
                    if field == 'School Website':
                        json_dict[field].append(parent.a['href'] if parent.a else None)
                    else:
                        json_data[field].append(parent.find_all('p')[-1].text)
        
        #This is where the recursion happens.
        if json_data['meta']['rel_next_page_url']:
            common_functions().fetch_results_page(json_data['meta']['rel_next_page_url'], json_dict)
        else:
            print('Done!')

