import io
import json
import logging
import oci
from base64 import b64encode, b64decode
from fdk import response

STREAM_NAME = "SdkExampleStream"
PARTITIONS = 1

def publish_example_messages(client, stream_id):
    # Build up a PutMessagesDetails and publish some messages to the stream
    message_list = []
    for i in range(100):
        key = "key" + str(i)
        value = "value" + str(i)
        encoded_key = b64encode(key.encode()).decode()
        encoded_value = b64encode(value.encode()).decode()
        message_list.append(oci.streaming.models.PutMessagesDetailsEntry(key=encoded_key, value=encoded_value))

    print("Publishing {} messages to the stream {} ".format(len(message_list), stream_id))
    messages = oci.streaming.models.PutMessagesDetails(messages=message_list)
    put_message_result = client.put_messages(stream_id, messages)

    # The put_message_result can contain some useful metadata for handling failures
    for entry in put_message_result.data.entries:
        if entry.error:
            print("Error ({}) : {}".format(entry.error, entry.error_message))
        else:
            print("Published message to partition {} , offset {}".format(entry.partition, entry.offset))


def handler(ctx, data: io.BytesIO=None):
    name = "World"
    try:
        body = json.loads(data.getvalue())
        name = body.get("name")
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    logging.getLogger().info("Inside Python Hello World function")
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello {0}".format(name)}),
        headers={"Content-Type": "application/json"}
    )
