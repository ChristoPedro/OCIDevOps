import io
from kafka import KafkaProducer
import logging
import json

if __name__ == '__main__':

    message = '{"File": {"Dados": "Dados de arquivo"},"NoSQL":{"Dados": "NoSQL"}}'

    dados = json.loads(message)

    topics = [] 
    for keys in dados.keys():
        topics.append(keys)

    producer = KafkaProducer(bootstrap_servers = 'streaming.sa-saopaulo-1.oci.oraclecloud.com:9092', 
                         security_protocol = 'SASL_SSL', sasl_mechanism = 'PLAIN',
                         sasl_plain_username = 'ladcloudengineeringhub/KafkaUser/ocid1.streampool.oc1.sa-saopaulo-1.amaaaaaakeemx2yafx6ibx4pny7vicnvza734jsa3iltxsl247h46oiqamtq', 
                         sasl_plain_password = 'IpgfOK16p]q:XrQ;2[IV')
    key = 'Dados'.encode('utf-8')
    data = 'Hello'.encode('utf-8')

    for x in topics:

        data = json.dumps(dados[x]).encode('UTF-8')
        print(data)