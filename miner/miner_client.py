import hashlib
import time
import json
import random
import paho.mqtt.client as mqtt
import threading as thrd
from custom_encoder import CustomEncoder
from challenge_response import ChallengeResponse
from submit_payload import SubmitPayload
from multiprocessing import cpu_count, Manager
from time import perf_counter
import bitarray

c = thrd.Condition()
current_challenge = None


class SeedCalculator(thrd.Thread):
    def __init__(self, id):
        thrd.Thread.__init__(self)
        self.__seed = 0
        self.__time_to_finish = 0
        self.__id = id

    @property
    def seed(self):
        return self.__seed

    @property
    def time_to_finish(self):
        return self.__time_to_finish

    def run(self):
        start = perf_counter()
        print("SeedCalculator {} started".format(self.__id))
        while (True):
            global current_challenge
            if (current_challenge is None):
                continue
            challenge = current_challenge.challenge
            transaction_id = current_challenge.transaction_id
            seed = random.randint(0, 2000000000)
            ba = bitarray.bitarray()
            hash_byte = hashlib.sha1(seed.to_bytes(8, byteorder='big'))
            ba.frombytes(hash_byte.digest())
            prefix = ba[0:challenge]

            # iterate over prefix characters to check if it is a valid seed
            for i in range(0, challenge):
                if prefix[i] != 0:
                    break
            else:
                c.acquire()
                if (current_challenge.transaction_id != transaction_id):
                    c.release()
                    continue
                current_challenge = None

                submit = SubmitPayload(transaction_id=transaction_id,
                                       seed=seed, client_id=client_id)
                submit_json = json.dumps(submit, indent=4, cls=CustomEncoder)
                client.publish(topic="ppd/seed", payload=submit_json)

                end = perf_counter()

                self.__time_to_finish = end - start
                start = perf_counter()
                print("Solved transaction {} with thread {} in {} seconds".format(
                    transaction_id, self.__id, self.__time_to_finish))
                c.notify_all()
                c.release()


mqttBroker = "127.0.0.1"
#mqttBroker = "broker.emqx.io"
client_id = int(time.time())
client = mqtt.Client(
    "Client " + str(client_id))
print("Running for client id: " + str(client_id))
client.connect(mqttBroker)

client.loop_start()
client.subscribe(topic="ppd/challenge")
client.subscribe(topic="ppd/result")


def on_message(client, userdata, message):
    print("Incoming message...")
    data_in = json.loads(message.payload.decode("utf-8"))

    if (message.topic == "ppd/challenge"):
        print("Challenge: ", data_in)
        data_in = ChallengeResponse(**data_in)
        c.acquire()
        global current_challenge
        current_challenge = data_in
        c.notify_all()
        c.release()
    if (message.topic == "ppd/result"):
        print("Result: ", data_in)
        data_in = SubmitPayload(**data_in)


client.on_message = on_message


def mine():

    max_threads = int(cpu_count() / 2)
    threads: SeedCalculator = []
    for i in range(0, max_threads):
        seed_calculator = SeedCalculator(i)
        threads.append(seed_calculator)

        seed_calculator.start()

    for s in threads:
        s.join()


mine()
