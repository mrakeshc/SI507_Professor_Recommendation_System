# SI507_Professor_Recommendation_System

## Getting Started
This github repository is a simple user interactive professor recommendation system developed for prospective PhD students. The user has to select the "University" and specify the Research Area they are interesed in to get the list of all professors. We conduct web scraping on the https://www.usnews.com/ website to extract information on all the schools based in the United States of America. All the useful information about the professors is cached in a JSON file, and can be used directly rather than web scrapping or calling APIs everytime the user interacts with the system. 

### Setup
Dependencies :-
- beautifulsoup4==4.11.1
- bs4==0.0.1
- Flask==2.2.2
- google-search-results==2.4.1
- jedi==0.18.0
- Jinja2==3.1.2
- matplotlib-inline==0.1.2
- numpy==1.23.5
- requests==2.28.1
- urllib3==1.26.13

Installation of all this library can be done by running ``pip install -r requirement.txt`` in the appropriate terminal.

## File distribution
This repository contains the following files:
1. `user_inputs.py`: A python file that helps users input information regarding universities and research areas. This file also has the capability to validate the user inputs and warn them.
2. `common.py`: This python file holds functions to load and save the json scripts for cacheing purposes.
3. `profapi.py`: Python file that can conduct web scrapping and perform api calls to extract universities and professors information.
4. `main.py`: Main python that does data processing and constructs a tree object based on the user inputs. This file also has a class object to save the data tree representation as a `JSON` file.
5. `app.py`: This python file first imports the tree constructed in the `main.py` file and then use the rendered html template to display the tree in the local host http://127.0.0.1:5000/ 
6. ``template/index.html`` A HTML script for flask.
