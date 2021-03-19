import io
from kafka import KafkaProducer
from fdk import response
import logging
import json

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

    data = json.loads(data.getvalue())
    body = str(data)

    producer = KafkaProducer(bootstrap_servers = server, 
                         security_protocol = 'SASL_SSL', sasl_mechanism = 'PLAIN',
                         sasl_plain_username = username, 
                         sasl_plain_password = password)
    
    key = 'Dados'.encode('utf-8')
    data = body.encode('utf-8')

    try:
        producer.send(partition, key=key, value=data)
        producer.flush()
        resp = 'Dados Inseridos com sucesso na Partition: ' + partition
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex)) 
        resp = 'error parsing json payload: ' + str(ex)

    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )