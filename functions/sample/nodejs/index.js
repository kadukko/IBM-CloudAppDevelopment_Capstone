/**
* Get all dealerships
*/

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator });
    cloudant.setServiceUrl(params.COUCH_URL);
    try {
        let dealerships = [];
        
        if (params.state) {
            dealerships = await cloudant.postFind({db: 'dealerships', selector: {state: params.state}})
                .then(response => {
                    return response.result.docs.map(doc => ({
                        "id": doc.id,
                        "city": doc.city,
                        "state": doc.state,
                        "st": doc.st,
                        "address": doc.address,
                        "zip": doc.zip,
                        "lat": doc.lat,
                        "long": doc.long
                    }))
                })
        } else {
            dealerships = await cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 10 })
                .then(response => {
                    return response.result.rows.map(row => ({
                        "id": row.doc.id,
                        "city": row.doc.city,
                        "state": row.doc.state,
                        "st": row.doc.st,
                        "address": row.doc.address,
                        "zip": row.doc.zip,
                        "lat": row.doc.lat,
                        "long": row.doc.long
                    }))
                })
        }
        
        return { body: dealerships };
    } catch (error) {
        return { error: error.description };
    }
}
