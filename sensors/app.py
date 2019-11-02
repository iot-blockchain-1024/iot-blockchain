import Adafruit_DHT
import time
import json, os
import mh_z19
import RPi.GPIO as GPIO
import requests
from bit import PrivateKeyTestnet
import numpy as np
from config import IS_POST_TO_SERVER, IS_BROADCAST_TO_BLOCKCHAIN, BITCOIN_IOT_RECEIVER, IS_SAVE_TO_LOCAL, \
    LOCAL_FOLDER_DIR, POST_INTERVAL_TIME, BROADCAST_INTERVAL, BITCOIN_IOT_SENDER_KEY, BITCOIN_TRANSFER_AMOUNT, API_URL

current_counts = 1
current_sets = []


def post_to_server(data):
    if not IS_POST_TO_SERVER:
        return "NOT POST TO SERVER"
    params = json.dumps(data)
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
    try:
        response = requests.post(url=API_URL, data=params,
                                 headers=headers)
        return response.text
    except:
        pass

    return ""


def broadcast_to_blockchain(info):
    if not IS_BROADCAST_TO_BLOCKCHAIN:
        return "NOT BROADCAST TO BLOCKCHAIN"
    key = PrivateKeyTestnet(BITCOIN_IOT_SENDER_KEY)
    output = [(BITCOIN_IOT_RECEIVER, BITCOIN_TRANSFER_AMOUNT, "btc")]
    key.send(output, message=info)
    return "BITCOIN TESTNET SUCCESS: " + info


def save_to_local_folder(date, data):
    if not IS_SAVE_TO_LOCAL:
        return "NOT SAVE TO LOCAL"
    file_path = LOCAL_FOLDER_DIR + "/" + date + ".json"
    if os.path.exists(file_path):
        file = open(file_path, "rb+")
        file.seek(-1, os.SEEK_END)
        file.truncate()
        file.write(bytes(',', encoding="utf8"))
        file.write(bytes(json.dumps(data), encoding="utf8"))
        file.write(bytes(']', encoding="utf8"))
        file.close()
    else:
        file = open(file_path, "w")
        file.write('[')
        json.dump(data, file)
        file.write(']')
        file.close()
    return ""


def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN)


def compute_average():
    result = {}
    current_sets_last = len(current_sets) - 1
    result['date'] = current_sets[current_sets_last]['date']
    result['time'] = current_sets[current_sets_last]['time']
    result['timestamp'] = current_sets[current_sets_last]['timestamp']
    result['hmt'] = format(compute_mean(current_sets, 'hmt'), ".1f")
    result['tmp'] = format(compute_mean(current_sets, 'tmp'), ".1f")
    result['ppm'] = format(compute_mean(current_sets, 'ppm'), ".1f")
    result['lx'] = format(compute_mean(current_sets, 'lx'), ".1f")
    result['ld'] = format(compute_mean(current_sets, 'ld'), ".1f")
    return result


def compute_mean(arr, keyword):
    tmp = []
    for item in arr:
        tmp.append(float(item[keyword]))
    return np.mean(tmp)


def start_monitoring():
    # dht and hmt senors
    dht_hmt_sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(dht_hmt_sensor, 26)
    # co2 senors
    co2 = mh_z19.read()
    # timestamp
    current_milli_time = str(int(round(time.time() * 1000)))
    # if every hardware is working
    if humidity is not None and temperature is not None and co2 != "9":
        data = {}
        data['date'] = time.strftime('%Y%m%d', time.localtime(time.time()))
        data['time'] = time.strftime('%H:%M', time.localtime(time.time()))
        data['tmp'] = format(temperature, ".1f")
        data['hmt'] = format(humidity, ".1f")
        data['ppm'] = str(co2['co2'])
        data['lx'] = str(GPIO.input(21))
        data['ld'] = '0'
        data['timestamp'] = current_milli_time
        # push to the sets
        current_sets.append(data)
        messages = {
            "time": data['time'],
            "tmp": data['tmp'],
            "hmt": data['tmp'],
            "ppm": data['ppm'],
            "lx": data['lx'],
            "ld": data['ld'],
            "date": data['date'],
            "timestamp": data['timestamp']
        }
        print(messages)
        # save to local folder
        print(save_to_local_folder(data['date'], messages))

        # post to remote server
        try:
            print(post_to_server(messages))
        except:
            pass
    return


if __name__ == '__main__':
    init_GPIO()
    while True:
        start_monitoring()
        current_counts = current_counts + 1
        if current_counts > BROADCAST_INTERVAL:
            req = compute_average()
            current_sets = []
            current_counts = 0
            messages = req['hmt'] + "|" + req['tmp'] + '|' + req['ppm'] + '|' + req['lx'] + '|' + req['timestamp']
            # broadcast to blockchain
            try:
                print(broadcast_to_blockchain(messages))
            except:
                pass

        time.sleep(POST_INTERVAL_TIME)
