import io
from kafka import KafkaProducer
from fdk import response
import oci
import logging
import json

signer = oci.auth.signers.get_resource_principals_signer()

secret_client = oci.secrets.SecretsClient(config={}, signer=signer)

def read_secret_value(secret_client, secretid):
    response = secret_client.get_secret_bundle(secret_id=secretid, version_number=1)
    base64_Secret_content = response.data.secret_bundle_content.content
    base64_secret_bytes = base64_Secret_content.encode('ascii')
    base64_message_bytes = base64.b64decode(base64_secret_bytes)
    secret_content = base64_message_bytes.decode('ascii')
    return secret_content

def handler(ctx, data: io.BytesIO=None):

    try:
        cfg = ctx.Config()
        server = cfg["server"]
        username = cfg["username"]
        secretid = cfg["password"]
    except Exception as e:
        print('Missing function parameters', flush=True)
        raise
    
    password = read_secret_value(secret_client, secretid)
    data = json.loads(data.getvalue())

    topics = [] 
    for keys in data.keys():
        topics.append(keys)

    producer = KafkaProducer(bootstrap_servers = server, 
                         security_protocol = 'SASL_SSL', sasl_mechanism = 'PLAIN',
                         sasl_plain_username = username, 
                         sasl_plain_password = password)
    
    key = 'Dados'.encode('utf-8')
    
    for x in topics:

        values = json.dumps(data[x]).encode('UTF-8')

        try:
            producer.send(x, key=key, value=values)
            producer.flush()
            resp = 'Dados Inseridos com sucesso'
        except (Exception, ValueError) as ex:
            logging.getLogger().info('error parsing json payload: ' + str(ex)) 
            resp = 'error parsing json payload: ' + str(ex)

    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )