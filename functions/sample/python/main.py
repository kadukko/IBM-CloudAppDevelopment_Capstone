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
        print(param_dict["dealerId"])
        
        if param_dict['__ow_method'] == 'get':
            reviews = []
        
            try:
                authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
                service = CloudantV1(authenticator=authenticator)
                service.set_service_url(param_dict["COUCH_URL"])
                
                dealerId = None
                
                try:
                    dealerId = param_dict["dealerId"]
                except:
                    pass
                
                if dealerId is None:
                    return { 
                        "statusCode": 404, 
                        "body": "DealerId not found." 
                    }
                
                    
                response = service.post_find(
                  db='reviews',
                  selector={'dealership': int(dealerId)}
                ).get_result()
                
                for doc in response["docs"]:
                    del doc["_id"]
                    del doc["_rev"]
                    reviews.append(doc)
            except Exception as err:
                return {"body": "Connection error", "statusCode": 500}
        
            return {"body": reviews}
            
        if param_dict['__ow_method'] == 'post':
            return {"body": "Pending implementation", "statusCode": 503}
            
        return {"body": "Invalid request", "statusCode": 401}
    except:
        return {"body": "Internal error", "statusCode": 500}
