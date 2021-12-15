import io
import json
import logging
import requests
from kafka import KafkaConsumer

from fdk import response

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
        dbpwd = cfg["dbpwd"]

    except Exception as e:
        print('Missing function parameters', flush=True)
        raise

    content = data.getvalue()

    resp = soda_insert(ordsbaseurl, schema, dbuser, dbpwd, content)
    
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
