

import requests
from datetime import datetime

def retrieve_json_data(canon_url):
    base_url = 'https://prism.ext.nile.works/content/v4/?website_url=/'
    key = "key"
    url = f"{base_url}{canon_url}&website=washpost&key={key}"

    response = requests.get(url)
    response.raise_for_status()
    
    if response.status_code == 200:
        json_data = response.json()
        additional_properties = json_data.get("additional_properties", {})
        page_title = additional_properties.get("page_title", "").replace(" - The Washington Post", "")
        publish_date = additional_properties.get("publish_date")
        if not isinstance(publish_date, str):
            publish_date = additional_properties.get("present_publish_date")
        if not isinstance(publish_date, str):
            publish_date = additional_properties.get("first_publish_date")
        formatted_date = convert_to_month_day(publish_date)
        original_url = additional_properties.get("lead_art", {}).get("additional_properties", {}).get("originalUrl")
        canonical_url = json_data.get("canonical_url")
        authors = json_data.get("credits", {}).get("by", [])
        author_names = ", ".join(author.get("name") for author in authors)
        item_dict = {
            "imageURL": original_url,   
            "title": page_title,
            "author": author_names,
            "date": formatted_date,
            "canonical_url": canonical_url
        }
    
    return item_dict

def retrieve_list():
    article_list = []
    urls = ['opinions/2023/07/24/bishop-menjivar-undocumented-el-salvador-catholic/', 'opinions/2023/01/18/how-to-fix-migrant-crisis/', 'lifestyle/2023/07/19/golden-retriever-scotland-breed-guisachan/']  # , 'opinions/2023/07/18/ukraine-war-west-gloom/', 'opinions/2022/04/11/how-else-can-we-help-ukraine/']

    for canon_url in urls:
        article_list.append(retrieve_json_data(canon_url))

    return article_list

def convert_to_month_day(date_str):
    date_only_str = date_str.split("T")[0]
    dt = datetime.fromisoformat(date_only_str)
    return dt.strftime("%B %d")

print(retrieve_list())