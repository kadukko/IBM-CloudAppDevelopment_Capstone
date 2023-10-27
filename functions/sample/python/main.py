"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """
    
    try:
        authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(param_dict["COUCH_URL"])
            
        if param_dict['__ow_method'] == 'get':
            dealerId = param_dict["dealerId"]
                
            response = service.post_find(
              db='reviews',
              selector={'dealership': int(dealerId)}
            ).get_result()
            
            if len(response["docs"]) == 0:
                return {"body": "DealerId not exists", "statusCode": 404}
            
            reviews = []
            
            for doc in response["docs"]:
                del doc["_rev"]
                reviews.append(doc)
    
            return {"body": reviews}
            
            
        if param_dict['__ow_method'] == 'post':
            review = None
        
            if param_dict['purchase']:
                review = Document(
                    name=param_dict['name'],
                    dealership=param_dict['dealership'],
                    review=param_dict['review'],
                    purchase=param_dict['purchase'],
                    purchase_date=param_dict['purchase_date'],
                    car_make=param_dict['car_make'],
                    car_model=param_dict['car_model'],
                    car_year=param_dict['car_year']
                )
            else:
                review = Document(
                    name=param_dict['name'],
                    dealership=param_dict['dealership'],
                    review=param_dict['review'],
                    purchase=param_dict['purchase']
                )
            
            response = service.post_document(
                db='reviews',
                document=review
            ).get_result()
            
            return { "body": response }
            
        return {"body": "Invalid request", "statusCode": 400}
    except:
        return {"body": "Internal error", "statusCode": 500}
