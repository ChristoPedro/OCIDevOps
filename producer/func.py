import io
from kafka import KafkaProducer
from fdk import response
import logging
import json

def handler(ctx, data: io.BytesIO=None):

    try:
        cfg = ctx.Config()
        server = cfg["server"]
        username = cfg["username"]
        password = cfg["password"]
    except Exception as e:
        print('Missing function parameters', flush=True)
        raise

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