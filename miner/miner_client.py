import hashlib
import time
from custom_encoder import CustomEncoder
from challenge_response import ChallengeResponse
from submit_payload import SubmitPayload
import paho.mqtt.client as mqtt
import json
import random


mqttBroker = "127.0.0.1"
mqttBroker = "broker.emqx.io"
client_id = int(time.time())
client = mqtt.Client(
    "Client " + str(client_id))
print("Running for client id: " + str(client_id))
client.connect(mqttBroker)

client.loop_start()
client.subscribe(topic="ppd/challenge")
client.subscribe(topic="ppd/result")


current_challenge = None


def on_message(client, userdata, message):
    print("Incoming message...")
    data_in = json.loads(message.payload.decode("utf-8"))

    if (message.topic == "ppd/challenge"):
        print("Challenge: ", data_in)
        data_in = ChallengeResponse(**data_in)
        global current_challenge
        current_challenge = data_in
    if (message.topic == "ppd/result"):
        print("Result: ", data_in)
        data_in = SubmitPayload(**data_in)


client.on_message = on_message


def mine():
    while (True):
        global current_challenge
        if (current_challenge is None):
            continue
        challenge = current_challenge.challenge
        transaction_id = current_challenge.transaction_id
        
        seed = random.randint(0, 2000000000)
        hashed_seed = hashlib.sha1(
            seed.to_bytes(8, byteorder='big')).hexdigest()
        prefix = hashed_seed[0:challenge]

        # iterate over prefix characters to check if it is a valid seed
        for i in range(0, challenge):
            if prefix[i] != "0":
                break
        else:
            print("Seed: " + str(seed) + " Prefix: " + prefix)
            current_challenge = None
            submit = SubmitPayload(transaction_id=transaction_id,
                                   seed=seed, client_id=client_id)
            submit_json = json.dumps(submit, indent=4, cls=CustomEncoder)
            client.publish(topic="ppd/seed", payload=submit_json)


mine()
