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
    r = requests.post(collectionurl, auth=auth, headers=headers, data=json.dumps(document))
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
        partition = cfg["partition"]
        server = cfg["server"]
        username = cfg["username"]
        password = cfg["password"]
        ordsbaseurl = cfg["ordsbaseURL"]
        schema = cfg["schema"]
        dbuser = cfg["dbuser"]
        dbpwd = cfg["dbpwd"]

    except Exception as e:
        print('Missing function parameters', flush=True)
        raise

    consumer = KafkaConsumer(partition, 
                            bootstrap_servers = server, 
                            security_protocol = 'SASL_SSL', sasl_mechanism = 'PLAIN',
                            consumer_timeout_ms = 10000, auto_offset_reset = 'earliest',
                            group_id='group-0',
                            sasl_plain_username = username, 
                            sasl_plain_password = password)

    content = []

    for message in consumer:
        content.append(message.value.decode('UTF-8'))

    resp = soda_insert(ordsbaseurl, schema, dbuser, dbpwd, content)
    
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
