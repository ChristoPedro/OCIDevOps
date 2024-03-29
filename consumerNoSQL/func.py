import io
import json
import oci
import requests
import base64

from fdk import response

signer = oci.auth.signers.get_resource_principals_signer()

secret_client = oci.secrets.SecretsClient(config={}, signer=signer)

def read_secret_value(secret_client, secretid):
    secret_content = secret_client.get_secret_bundle(secretid).data.secret_bundle_content.content.encode('utf-8')
    decrypted_secret_content = base64.b64decode(secret_content).decode("utf-8")
    return decrypted_secret_content

def soda_insert(ordsbaseurl, schema, dbuser, dbpwd, document):
    auth=(dbuser, dbpwd)
    sodaurl = ordsbaseurl + schema + '/soda/latest/'
    collectionurl = sodaurl + "demodados"
    headers = {'Content-Type': 'application/json'}
    r = requests.post(collectionurl, auth=auth, headers=headers, data=document)
    r_json = {}
    try:
        r_json = json.loads(r.text)
    except ValueError as e:
        print(r.text, flush=True)
        raise
    return r_json

def handler(ctx, data: io.BytesIO=None):

    try:
        cfg = ctx.Config()
        ordsbaseurl = cfg["ordsbaseURL"]
        schema = cfg["schema"]
        dbuser = cfg["dbuser"]
        secretid = cfg["dbpwd"]

    except Exception as e:
        print('Missing function parameters', flush=True)
        raise

    content = data.getvalue()

    dbpwd = read_secret_value(secret_client, secretid)

    resp = soda_insert(ordsbaseurl, schema, dbuser, dbpwd, content)
    
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
