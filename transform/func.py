import io
import json
import base64
import logging

from fdk import response

def transform(content):
    
    indice = 0
    for i in content:
        content[indice]['key'] = base64.b64decode(i['key']).decode('UTF-8')
        content[indice]['value'] = json.loads(base64.b64decode(i['value']).decode('UTF-8'))
        indice +=1
    return content

def handler(ctx, data: io.BytesIO=None):

    content = json.loads(data.getvalue())

    resp = transform(content)
     
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
