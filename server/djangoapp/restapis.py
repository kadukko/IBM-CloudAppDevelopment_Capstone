import requests
import json
import os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, params={}, headers={}, auth=None):
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, params=params, headers=headers, auth=auth)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def create_dealer_obj(data):
    return CarDealer(address=data["address"], city=data["city"], full_name=data["full_name"],
                    id=data["id"], lat=data["lat"], long=data["long"],
                    short_name=data["short_name"], st=data["st"], zip=data["zip"])

def create_dealer_review_obj(data):
    return DealerReview(id=review["_id"], name=review["name"], dealership=review["dealership"],
                        review=review["review"], purchase=review["purchase"], purchase_date=review.get("purchase_date", None),
                        car_maker=review.get("car_maker", None), car_model=review.get("car_model", None), car_year=review.get("car_year", None))

def get_dealers_from_cf(url, **kwargs):
    results = []
    
    headers = {'Content-Type': 'application/json'}
    
    dealers = get_request(url, headers=headers)
    if dealers:
        for dealer in dealers:
            dealer_obj = create_dealer_obj(dealer)
            results.append(dealer_obj)
    return results

def get_dealer_by_state_from_cf(url, state):
    results = []

    params = { "state": state }

    headers = {'Content-Type': 'application/json'}
    
    dealers = get_request(url, params=params, headers=headers)
    if dealers:
        for dealer in dealers:
            dealer_obj = create_dealer_obj(dealer)
            results.append(dealer_obj)
    return results

def get_dealer_by_id(url, id):
    results = []

    params = { "id": id }

    headers = {'Content-Type': 'application/json'}
    
    dealer = get_request(url, params=params, headers=headers)
    dealer_obj = create_dealer_obj(dealer)
    
    return dealer_obj

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []

    params = { "dealerId": dealer_id }

    headers = {'Content-Type': 'application/json'}

    reviews = get_request(url, params=params, headers=headers)
    if reviews:
        for review in reviews:
            review_obj = create_dealer_review_obj(review)
            results.append(review_obj)
    return results


def analyze_review_sentiments(text):
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/38645792-e114-4529-8dd8-0db2199593d0/v1/analyze'
    
    params = { 
        "text": text,
        "version": "2022-04-07",
        "features": "sentiment",
        "return_analyzed_text": True
    }

    headers = {'Content-Type': 'application/json'}

    api_key = os.environ['SLU_API_KEY']

    response = get_request(url, params=params, headers=headers, auth=HTTPBasicAuth('apikey', api_key))



