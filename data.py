import pandas as pd
import requests


def fetch_walmart_data_by_keyword(keyword):
    url = "https://axesso-walmart-data-service.p.rapidapi.com/wlm/walmart-search-by-keyword"
    headers = {
        "X-RapidAPI-Key": "API_KEY",
        "X-RapidAPI-Host": "axesso-walmart-data-service.p.rapidapi.com",
    }
    querystring = {"keyword": keyword, "page": "1", "sortBy": "best_match"}

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


# method used to extract the data from a large json file containing more than 1000
# of items
def extract_data(json_items):
    data = json_items["item"]["props"]["pageProps"]["initialData"]["searchResult"][
        "itemStacks"
    ]
    # defining a dictionary where each value contains
    # empty list
    item_data = {
        "id": [],
        "seller_name": [],
        "item_price": [],
        "Item_line_price": [],
        "availability": [],
        "avg_rating": [],
        "reviews": [],
        "item_name": [],
    }

    for stack in data:
        for item in stack["items"]:
            try:
                item_data["id"].append(item["usItemId"])
                item_data["seller_name"].append(item["sellerName"])
                item_data["item_price"].append(item["price"])
                item_data["Item_line_price"].append(item["priceInfo"]["linePrice"])
                item_data["availability"].append(not item["isOutOfStock"])
                item_data["avg_rating"].append(item["rating"]["averageRating"])
                item_data["reviews"].append(item["rating"]["numberOfReviews"])
                item_data["item_name"].append(item["name"])
            # exception raised when some data is missing
            # some items in the json file missed some data for ex
            # some missed item price or average rating
            # exception had to be made so it filtered those items
            except KeyError:
                print("Some data is missing")
    return pd.DataFrame(item_data)


# this is the main function which uses the other function in this file which is being used in gui.py
# using this function to which uses fetch_walmart_data_by_keyword and extract_walmart_data to get the data and save
# to a csv file "walmarrt_data.csv"
def process_walmart_data_by_keyword(item_keyword):
    walmart_json_data = fetch_walmart_data_by_keyword(item_keyword)
    # when data is retreived successfully extract the data  using extract_data() method
    # and save to a csv file
    if walmart_json_data:
        walmart_df = extract_data(walmart_json_data)
        walmart_df.to_csv("walmart_data.csv", index=False)
        return walmart_df
    else:
        return None
