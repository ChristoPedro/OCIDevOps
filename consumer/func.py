import io
import json
import logging
import oci.object_storage
from kafka import KafkaConsumer

from fdk import response

path = '/tmp/'

def put_object(bucketName, objectName, content):
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = client.get_namespace().data
    output=""
    try:
        object = client.put_object(namespace, bucketName, objectName, json.dumps(content))
        output = "Success: Put object '" + objectName + "' in bucket '" + bucketName + "'"
    except Exception as e:
        output = "Failed: " + str(e.message)
    return { "state": output }

def handler(ctx, data: io.BytesIO=None):

    try:
        cfg = ctx.Config()
        partition = cfg["partition"]
        server = cfg["server"]
        username = cfg["username"]
        password = cfg["password"]
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
        
        content.append("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))

    resp = put_object('Dados', 'KafkaTeste.txt', content)
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
