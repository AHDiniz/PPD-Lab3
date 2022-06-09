import hashlib
import time
import json
import random
import paho.mqtt.client as mqtt
import threading as thrd
from custom_encoder import CustomEncoder
from challenge_response import ChallengeResponse
from submit_payload import SubmitPayload
from multiprocessing import cpu_count
from time import perf_counter

class SeedCalculator(thrd.Thread):
    def __init__(self, challenge, transactionID):
        thrd.Thread.__init__(self)
        self.__challenge = challenge
        self.__seed = 0
        self.__time_to_finish = 0
        self.__transactionID = transactionID
    
    @property
    def seed(self):
        return self.__seed
    
    @property
    def time_to_finish(self):
        return self.__time_to_finish

    @property
    def transactionID(self):
        return self.__transactionID

    def run(self):
        start = perf_counter()

        while True:
            self.__seed = random.randint(0, 2000000000)
            hashed_seed = hashlib.sha1(self.__seed.to_bytes(8, byteorder='big')).hexdigest()
            prefix = hashed_seed[0:self.__challenge]

            # iterate over prefix characters to check if it is a valid seed
            for i in range(0, self.__challenge):
                if prefix[i] != "0":
                    break
            else:
                print("Seed: " + str(self.__seed) + " Prefix: " + prefix)
                global current_challenge
                current_challenge = None
                submit = SubmitPayload(transaction_id=self.__transactionID,
                                   seed=self.__seed, client_id=client_id)
                submit_json = json.dumps(submit, indent=4, cls=CustomEncoder)
                client.publish(topic="ppd/seed", payload=submit_json)
                break

        end = perf_counter()

        self.__time_to_finish = end - start

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

    max_threads = cpu_count() / 2
    threads = []

    while (True):
        global current_challenge
        if (current_challenge is None):
            continue
        challenge = current_challenge.challenge
        transaction_id = current_challenge.transaction_id
        
        seed_calculator = SeedCalculator(challenge, transaction_id)
        threads.append(seed_calculator)

        seed_calculator.run()

        if len(threads) == max_threads - 1:
            for s in threads:
                s.join()

mine()
