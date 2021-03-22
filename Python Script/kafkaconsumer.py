import io
from kafka import KafkaConsumer
import logging
import json
import requests

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

if __name__ == '__main__':

    consumer = KafkaConsumer('Partition', bootstrap_servers = 'streaming.sa-saopaulo-1.oci.oraclecloud.com:9092', 
                            security_protocol = 'SASL_SSL', sasl_mechanism = 'PLAIN',
                            consumer_timeout_ms = 10000, auto_offset_reset = 'earliest',
                            group_id='group-0',
                            sasl_plain_username = 'ladcloudengineeringhub/KafkaUser/ocid1.streampool.oc1.sa-saopaulo-1.amaaaaaakeemx2yafx6ibx4pny7vicnvza734jsa3iltxsl247h46oiqamtq', 
                            sasl_plain_password = 'IpgfOK16p]q:XrQ;2[IV')

    dados = []
    for message in consumer:
        print("Topic: %s Partition: %d Offset: %d: key= %s value= %s" % (message.topic, message.partition, message.offset, message.key, message.value))
        dados.append(message.value.decode('UTF-8'))
    
    id = soda_insert('https://O0N9NSBNVTBZ9VB-DEMOJSON.adb.sa-saopaulo-1.oraclecloudapps.com/ords/', 'admin', 'Admin', 'Oracle123456', dados)

    print(id)