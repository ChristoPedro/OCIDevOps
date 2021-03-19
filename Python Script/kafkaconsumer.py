import io
from kafka import KafkaConsumer
import logging
import json

if __name__ == '__main__':

    consumer = KafkaConsumer('Partition', bootstrap_servers = 'streaming.sa-saopaulo-1.oci.oraclecloud.com:9092', 
                            security_protocol = 'SASL_SSL', sasl_mechanism = 'PLAIN',
                            consumer_timeout_ms = 10000, auto_offset_reset = 'earliest',
                            group_id='group-0',
                            sasl_plain_username = 'ladcloudengineeringhub/KafkaUser/ocid1.streampool.oc1.sa-saopaulo-1.amaaaaaakeemx2yafx6ibx4pny7vicnvza734jsa3iltxsl247h46oiqamtq', 
                            sasl_plain_password = 'IpgfOK16p]q:XrQ;2[IV')

    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value)) 