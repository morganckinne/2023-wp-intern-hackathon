import requests
from datetime import datetime

set_of_positive_keywords = {"weekend", "wellness", "self-care", "healthy", "housing", "setting", "happy", "help", "goal", "best", "fitness"
                             "summer", "free", "less-crowded", "tourist", "fun", "funny", "comics", "Compassion", "positive",     
                            "adding", "improvement", "accessible", "empathy", "Hope", "Unity", "Inspiring", "Uplifting", "Heartwarming", "Empowering", "Gratitude", "Resilience", "Kindness",
                            "Progress", "Accomplishment", "Community", "Supportive", "Courageous", "Success", "Innovative", "Celebration", "Breakthrough",
                            "Transformative", "Connection", "Optimistic", "Solution-focused", "Wellness", "Mindfulness"}


"""
    Example ChatGPT prompt:

    You are a mental health professional and a news company has hired you to help increase the wellness of the readers.
Here is a list of 96 example article titles for you to understand journalistic vocabulary: 'United is adding Braille signage to its pl', 'Hot planes can be dangerous for fliers. Why are they so hard to cool?', 'How to search for bedbugs in hotels, according to pest exper', 'know about .... 'yphoon Doksuri kills five in Philippines as China, Taiwan brace for storm', 'wanese man is allowed to go home, four years after being arrested in C'
Generate a list of keywords that would have positive effects on readers based and prevent mental fatigue while reading the news. 
Justify your answer for each keyword and make sure they are specific to a journalistic setting.


"""


def retrieve_json_data(section_name):
    base_url = "https://prism.wpit.nile.works/api/v1/content/get?url=prism://prism.query/site,/"
    limit = 5 # number of articles to retrieve from each section in section_name list
    url = f"{base_url}{section_name}&limit={limit}"

    response = requests.get(url)
    response.raise_for_status()
    article_list = []
    
    if response.status_code == 200:
        json_data = response.json()
        items = json_data.get("items", [])

        for item in items:
            page_title = item.get("additional_properties", {}).get("page_title").strip(" - The Washington Post")
            publish_date = item.get("additional_properties", {}).get("publish_date")
            if not isinstance(publish_date, str):
                publish_date = item.get("additional_properties", {}).get("present_publish_date")
            if not isinstance(publish_date, str):
                publish_date = item.get("first_publish_date")
            formatted_date = convert_to_month_day(publish_date)
            original_url = item.get("additional_properties", {}).get("lead_art", {}).get("additional_properties", {}).get("originalUrl")
            canonical_url = item.get("canonical_url")
            authors = item.get("credits", {}).get("by", [])

            author_names = [author.get("name") for author in authors]
            author_names = ", ".join(author_names)

            item_dict = {
                "imageURL": original_url,   
                "title": page_title,
                "author": author_names,
                "date": formatted_date,
                "canonical_url": canonical_url
            }
            article_list.append(item_dict)
    
    return article_list


def retrieve_dict():
    section_names = ['travel', 'health', 'politics', 'weather', 'entertainment', 'national', 'business', 'wellbeing', 'sports', 'lifestyle', 'comics', 'photography', 'world']
    section_dict = {}

    for section_name in section_names:
        section_dict[section_name] = retrieve_json_data(section_name)

    return section_dict

def convert_to_month_day(date_str):
    date_only_str = date_str.split("T")[0]
    dt = datetime.fromisoformat(date_only_str)
    return dt.strftime("%B %d")

_initial_dict = retrieve_dict()

def get_titles():
    titles = []
    for key in _initial_dict:
        if(_initial_dict[key]):
            for j in range(len(_initial_dict[key])):
                titles.append(_initial_dict[key][j]["title"])
    return titles

def get_pos_titles():
    titles = get_titles()
    pos_titles = []
    count = 0
    for title in titles:
        for keyword in set_of_positive_keywords:
            if keyword in title:
                pos_titles.append(title)
                count += 1
                if count >= 3:
                    return pos_titles
                break
    return pos_titles

def search_titles_in_sections(title_list, data_dict):
    matching_portions = []
    for section, titles in data_dict.items():
        for entry in titles:
            if entry['title'] in title_list:
                matching_portions.append(entry)
    return matching_portions

print(search_titles_in_sections(get_pos_titles(), _initial_dict))