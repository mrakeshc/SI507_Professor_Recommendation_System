import json
from common import common_functions

from profapi import serpapi_scrape_all_authors_from_university
from User_inputs import scrapping_caching_universities, inputs
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

    


def scraping_caching():
    print("Welcome to the Professor Recommendation System")
    final_dict_sorted = scrapping_caching_universities()
   
    name_university, research_area = inputs(final_dict_sorted)
    cache_new_file = 'Professors.json'
    json_cache_dict = common_functions().load_cache_scholar(cache_new_file)
    
    
    
    key_dict = name_university + ' ' + research_area
    if len(json_cache_dict) > 0:
        list_current_universities = [temp['text'] for temp in json_cache_dict]
    
    if (len(json_cache_dict)) == 0 or (key_dict not in list_current_universities):
        json_cache_dict_temp = {}
        json_cache_dict_temp["text"] = key_dict
        json_cache_dict_temp["nodes"] = []
        api_key = 'b9cff6a01b570d0396f69c2f1586994e8a82672bbe453259b4970dbaa4ee417c'
        google_scholar_api = serpapi_scrape_all_authors_from_university(api_key, research_area.replace(" ", "_"), name_university)
        json_scholar_cite = google_scholar_api.new()
        if len(json_scholar_cite) == 0:
            json_cache_dict_temp = {}
        for each_professor_info in json_scholar_cite:
            temp_dict = {}
            temp_dict['text'] = each_professor_info['name']
                        
            temp_dict['nodes'] = [
                {
                    'text': "Link to Google Scholar Page {}".format(each_professor_info['link'])
                # 'text': each_professor_info['link']
                    },
                {'text': "Total Number of Citations {}".format(each_professor_info['cited_by'])},
                {'text': "All Research Areas the Professor is Currently Working on: {}".format([add_int['title'] for add_int in each_professor_info['interests']])},
                {'text': "Similar Professors in the Above Research Areas: {}".format([add_int['link'] for add_int in each_professor_info['interests']])}
                ]
            json_cache_dict_temp['nodes'].append(temp_dict)
        if len(json_cache_dict_temp) != 0:
            json_cache_dict.append(json_cache_dict_temp)
            cache_file = open(cache_new_file, 'w')
            contents_to_write = json.dumps(json_cache_dict)
            cache_file.write(contents_to_write)
            cache_file.close()
        # save_cache(cache_new_file, json_cache_dict.append(json_cache_dict_temp))
    else:
        print('Using Cache for the google scholar page')
    return json_cache_dict

if __name__ == "__main__":
    scraping_caching()


        
    


