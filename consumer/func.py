import io
import json
import oci.object_storage
from datetime import datetime

from fdk import response

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
datahora = str(dt_string)

def put_object(bucketName, objectName, content):
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = client.get_namespace().data
    output=""
    try:
        object = client.put_object(namespace, bucketName, objectName, content)
        output = "Success: Put object '" + objectName + "' in bucket '" + bucketName + "'"
    except Exception as e:
        output = "Failed: " + str(e.message)
    return { "state": output }

def handler(ctx, data: io.BytesIO=None):

    try:
            cfg = ctx.Config()
            bucketName = cfg["bucketname"]
            
    except Exception as e:
        print('Missing function parameters', flush=True)
        raise

    content = data.getvalue()

    filename = 'KafkaDemo ' + datahora + '.txt'

    resp = put_object(bucketName, filename, content)
    
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
