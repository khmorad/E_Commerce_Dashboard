import pandas as pd
import requests

# "207c3389f3msh11486cf94cb0b1dp16574bjsn187424d96ce9"  //key not working --reached monthly limit :(--


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


def extract_walmart_data(json_data):
    data = json_data["item"]["props"]["pageProps"]["initialData"]["searchResult"][
        "itemStacks"
    ]
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
            except KeyError:
                print("Some data is missing")
    return pd.DataFrame(item_data)


def process_walmart_data_by_keyword(keyword):
    walmart_json_data = fetch_walmart_data_by_keyword(keyword)
    if walmart_json_data:
        walmart_df = extract_walmart_data(walmart_json_data)
        walmart_df.to_csv("walmart_data.csv", index=False)
        return walmart_df
    else:
        return None
