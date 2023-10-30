/**
* Get all dealerships
*/

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const { id, state } = params
    
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator });
    cloudant.setServiceUrl(params.COUCH_URL);
    
    try {
        if (id) {
            const response = await cloudant.postFind({ db: 'dealerships', selector: { id: Number(id) }, limit: 1})
            const doc = response.result.docs[0]
            
            const dealership = {
                "id": doc.id,
                "full_name": doc.full_name,
                "short_name": doc.short_name,
                "city": doc.city,
                "state": doc.state,
                "st": doc.st,
                "address": doc.address,
                "zip": doc.zip,
                "lat": doc.lat,
                "long": doc.long
            }
            
            return { body: dealership }
        }
        
        if (state) {
            const response = await cloudant.postFind({ db: 'dealerships', selector: { state }})
            const doc = response.result.docs[0]
            
            const dealership = {
                "id": doc.id,
                "full_name": doc.full_name,
                "short_name": doc.short_name,
                "city": doc.city,
                "state": doc.state,
                "st": doc.st,
                "address": doc.address,
                "zip": doc.zip,
                "lat": doc.lat,
                "long": doc.long
            }
            
            return { body: dealership }
        }
        
        let dealerships = await cloudant.postAllDocs({ db: 'dealerships', includeDocs: true })
            .then(response => {
                return response.result.rows.map(row => ({
                    "id": row.doc.id,
                    "full_name": row.doc.full_name,
                    "short_name": row.doc.short_name,
                    "city": row.doc.city,
                    "state": row.doc.state,
                    "st": row.doc.st,
                    "address": row.doc.address,
                    "zip": row.doc.zip,
                    "lat": row.doc.lat,
                    "long": row.doc.long
                }))
            })
        
        return { body: dealerships };
    } catch (error) {
        return { error: error.description };
    }
}
