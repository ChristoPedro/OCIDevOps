import io
from kafka import KafkaProducer
from fdk import response
import logging
import json

def handler(ctx, data: io.BytesIO=None):

    data = json.loads(data.getvalue())
    body = str(data)

    producer = KafkaProducer(bootstrap_servers = 'streaming.sa-saopaulo-1.oci.oraclecloud.com:9092', 
                         security_protocol = 'SASL_SSL', sasl_mechanism = 'PLAIN',
                         sasl_plain_username = 'ladcloudengineeringhub/KafkaUser/ocid1.streampool.oc1.sa-saopaulo-1.amaaaaaakeemx2yafx6ibx4pny7vicnvza734jsa3iltxsl247h46oiqamtq', 
                         sasl_plain_password = 'IpgfOK16p]q:XrQ;2[IV')
    
    key = 'Dados'.encode('utf-8')
    data = body.encode('utf-8')

    producer.send('Partition', key=key, value=data)

    producer.flush()