import io
import json
import oci
import base64
from fdk import response

def publish_notification(topic_id, msg_title, msg_body):
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.ons.NotificationDataPlaneClient({}, signer = signer)
    msg = oci.ons.models.MessageDetails(title = msg_title, body = msg_body)
    print(msg, flush=True)
    client.publish_message(topic_id, msg)

def base64_decode(encoded):
    print(type(encoded))
    base64_bytes = encoded.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')

def handler(ctx, data: io.BytesIO=None):
    try:
        body = json.loads(data.getvalue())
        cfg = ctx.Config()
        topic_id = cfg["topic_id"]
    except Exception as ex:
        print("Msg body and topic id needed!", ex, flush=True)
        raise
    for item in body:
        if 'value' in item:
            value = base64_decode(item['value'])
        else:
            value = 'Corpo Vazio'
        if 'key' in item:
            key = base64_decode(item['key'])
        else:
            key = 'Chave Vazia'
        publish_notification(topic_id, key, value)
    return response.Response(ctx,
        response_data={"response":"email sent"},
        headers={"Content-Type": "application/json"}
    )