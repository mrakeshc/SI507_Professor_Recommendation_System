# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 20:18:51 2022

@author: mrakeshc
"""

"""
Importing the necessary libraries for parsing and doing a google search
"""
from urllib.parse import urlsplit, parse_qsl
from serpapi import GoogleSearch


class serpapi_scrape_all_authors_from_university():
    def __init__(self, api_key, research_area, university_name):
        """
        An Object to scrape the dete from the google scholar page using the research interest and the University user has selected.
        Args:
            inputs:
                api_key: an API key to scrape data from the google scholar page
                research_area: Research Area the User has entered
                univesity_name: The University the user has chosen
            return:
                profile_results_data: a list that holds the information of professors working in the selected research in the chosen university,
        """
        self.api_key = api_key
        self.research_area = research_area
        self.university_name = university_name
    def new(self):
        # Params we are passing into the URL search
        params = {
            "api_key": self.api_key,                   
            "engine": "google_scholar_profiles",               
            "mauthors":  f'label:{self.research_area} "{self.university_name}"' 
        }
        # print(params)
        print('fetching data for {} in {}'.format(self.research_area, self.university_name))
        # Conducting the google search
        search = GoogleSearch(params)
    
        profile_results_data = []
    
        profiles_is_present = True
        while profiles_is_present:
            profile_results = search.get_dict()
            if 'error' in profile_results.keys():
                print("Either the Research Area/university name you entered is incorrect or there are no professors working in the specified research field/uiversity.")
                break
    
            for profile in profile_results["profiles"]:
                """
                These are the keys we scrape for each professor
                """
                name = profile["name"]
                link = profile["link"]
                affiliations = profile["affiliations"]
                cited_by = profile.get("cited_by")
                interests = profile.get("interests")
    
                profile_results_data.append({
                    "name": name,
                    "link": link,
                    "affiliations": affiliations,
                    "cited_by": cited_by,
                    "interests": interests
                })
    
            if "next" in profile_results.get("serpapi_pagination", {}):
                # splits URL in parts as a dict() and update search "params" variable to a new page that will be passed to GoogleSearch()
                search.params_dict.update(dict(parse_qsl(urlsplit(profile_results.get("serpapi_pagination").get("next")).query)))
            else:
                profiles_is_present = False
    
        return profile_results_data

