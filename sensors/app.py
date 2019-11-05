import Adafruit_DHT
import time
import json, os
import mh_z19
import RPi.GPIO as GPIO
import requests
from bit import PrivateKeyTestnet
import numpy as np
import smbus

from config import IS_POST_TO_SERVER, IS_BROADCAST_TO_BLOCKCHAIN, BITCOIN_IOT_RECEIVER, IS_SAVE_TO_LOCAL, \
    LOCAL_FOLDER_DIR, POST_INTERVAL_TIME, BROADCAST_INTERVAL, BITCOIN_IOT_SENDER_KEY, BITCOIN_TRANSFER_AMOUNT, API_URL, \
    DEVICE_ID, __DEV_ADDR, __CMD_PWR_ON, __CMD_RESET, __CMD_SEN100H, __CMD_PWR_OFF, __CMD_SEN100L, __CMD_THRES2

current_counts = 1
current_sets = []
last_transaction = ''
key = PrivateKeyTestnet(BITCOIN_IOT_SENDER_KEY)
retries = 0
bus = smbus.SMBus(1)


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
    output = [(BITCOIN_IOT_RECEIVER, BITCOIN_TRANSFER_AMOUNT, "btc")]
    hex_str = key.send(output, message=info)
    return "BITCOIN TESTNET SUCCESS: " + hex_str


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
    bus.write_byte(__DEV_ADDR, __CMD_PWR_ON)
    bus.write_byte(__DEV_ADDR, __CMD_RESET)
    bus.write_byte(__DEV_ADDR, __CMD_SEN100H)
    bus.write_byte(__DEV_ADDR, __CMD_SEN100L)
    bus.write_byte(__DEV_ADDR, __CMD_PWR_OFF)


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
    # lx senors
    bus.write_byte(__DEV_ADDR, __CMD_PWR_ON)
    bus.write_byte(__DEV_ADDR, __CMD_THRES2)
    time.sleep(0.2)
    res = bus.read_word_data(__DEV_ADDR, 0)
    res = ((res >> 8) & 0xff) | (res << 8) & 0xff00
    lx = round(res / (2 * 1.2), 2)

    # if every hardware is working
    if humidity is not None and temperature is not None and co2 != "9":
        data = {}
        data['date'] = time.strftime('%Y%m%d', time.localtime(time.time()))
        data['time'] = time.strftime('%H:%M', time.localtime(time.time()))
        data['tmp'] = format(temperature, ".1f")
        data['hmt'] = format(humidity, ".1f")
        data['ppm'] = str(co2['co2'])
        data['lx'] = str(lx)
        data['ld'] = str(GPIO.input(21))
        data['timestamp'] = current_milli_time
        # push to the sets
        current_sets.append(data)
        messages = {
            "time": data['time'],
            "tmp": data['tmp'],
            "hmt": data['hmt'],
            "ppm": data['ppm'],
            "lx": data['lx'],
            "ld": data['ld'],
            "date": data['date'],
            "timestamp": data['timestamp'],
            "device": str(DEVICE_ID),
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
    last_transaction = key.get_transactions()[0]
    while True:
        start_monitoring()
        print("CURRENT OID", current_counts)
        current_counts = current_counts + 1
        if current_counts > BROADCAST_INTERVAL:
            req = compute_average()
            current_sets = []
            current_counts = 0
            messages = req['hmt'] + "|" + req['tmp'] + '|' + req['ppm'] + '|' + req['lx'] + '|' + req['timestamp'] + '|' + str(DEVICE_ID)
            # broadcast to blockchain
            try:
                print(broadcast_to_blockchain(messages))
                tmp = key.get_transactions()[0]
                if tmp is last_transaction:
                    print("waiting 1 min, retry")
                    time.sleep(1)
                    print(broadcast_to_blockchain(messages))
                else:
                    last_transaction = tmp
            except:
                pass

        time.sleep(POST_INTERVAL_TIME)
