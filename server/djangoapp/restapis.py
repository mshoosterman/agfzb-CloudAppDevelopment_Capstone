import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import time


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occured")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a CarDealer object list
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["body"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"],
                                   city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"],
                                   lat=dealer_doc["lat"],
                                   long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"],
                                   zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(url, id):
    """
    Finds the unique dealership in the database with id = <id>, and returns as a dealership object.
    """
    json_result = get_request(url, id=id)
    if json_result:
        dealer_doc = json_result["body"][0]
        dealer_obj = CarDealer(address=dealer_doc["address"],
                               city=dealer_doc["city"],
                               full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"],
                               lat=dealer_doc["lat"],
                               long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               st=dealer_doc["st"],
                               zip=dealer_doc["zip"])
        return dealer_obj


def get_dealers_by_st_from_cf(url, state):
    """
    Gets all dealerships in database from a given state, where ,<state> is a 2-word abbreviation of
    the states name. Returns a list of dealership objects
    """
    results = []
    json_result = get_request(url, st=state)
    if json_result:
        dealers = json_result["body"]
        for dealer_doc in dealers:
            dealer_obj = CarDealer(address=dealer_doc["address"],
                                   city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"],
                                   lat=dealer_doc["lat"],
                                   long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"],
                                   zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)

    if json_result:
        reviews = json_result["body"]["data"]["docs"]

        for dealer_review in reviews:
            sentiment = analyze_review_sentiments(dealer_review["review"])
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                      name=dealer_review["name"],
                                      purchase=dealer_review["review"],
                                      review=dealer_review["review"],
                                      sentiment=sentiment,
                                      id=dealer_review["id"])
            if "car_make" in dealer_review:
                review_obj.add_car(car_model=dealer_review["car_model"],
                                   car_make=dealer_review["car_make"],
                                   car_year=dealer_review["car_year"],
                                   purchase_date=dealer_review["purchase_date"])
            print(sentiment)
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    # - Call get_request() with specified arguments
    # - Get the returned sentiment label such as Positive or Negative
    url = ""
    api_key = ""
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-08-01', authenticator=authenticator)
    # new_text adds some neutral phrases to the string text to resolve an issue with NLU not returning results
    # when given strings that are too short.
    new_text = text + " hello hello hello"
    response = natural_language_understanding.analyze(text=new_text,
                                                      features=Features(
                                                          sentiment=SentimentOptions(targets=[new_text]))).get_result()
    response = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']

    return label



