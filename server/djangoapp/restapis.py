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


def post_request(url, params={}, data={}, headers={}, auth=None):
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, params=params, data=json.dumps(data), headers=headers, auth=auth)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def create_dealer_obj(data):
    return CarDealer(address=data["address"], city=data["city"], full_name=data["full_name"],
                    id=data["id"], lat=data["lat"], long=data["long"],
                    short_name=data["short_name"], st=data["st"], zip=data["zip"])

def create_dealer_review_obj(data):
    return DealerReview(id=data["_id"], name=data["name"], dealership=data["dealership"],
                        review=data["review"], purchase=data["purchase"], purchase_date=data.get("purchase_date", None),
                        car_make=data.get("car_make", None), car_model=data.get("car_model", None), car_year=data.get("car_year", None),
                        sentiment=data.get("sentiment", None))

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
    params = { "id": id }

    headers = {'Content-Type': 'application/json'}
    
    dealer = get_request(url, params=params, headers=headers)
    dealer_obj = create_dealer_obj(dealer)
    
    return dealer_obj

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []

    params = { "dealerId": dealer_id }

    headers = {'Content-Type': 'application/json'}

    try:
        reviews = get_request(url, params=params, headers=headers)

        for review in reviews:
            sentiment = analyze_review_sentiments(review['review'])

            print(sentiment)
            
            review_obj = create_dealer_review_obj(review)
            review_obj.sentiment = sentiment

            results.append(review_obj)
    except:
        pass

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

    api_key = os.environ.get('SLU_API_KEY', None)
    
    sentiment = 'neutral'

    try:
        response = get_request(url, params=params, headers=headers, auth=HTTPBasicAuth('apikey', api_key))
        sentiment = response['sentiment']['document']['label']
    except Exception as e:
        print(e)
        pass

    return sentiment

def post_dealer_review(url, data):
    headers = {'Content-Type': 'application/json'}
    return post_request(url, data=data, headers=headers)