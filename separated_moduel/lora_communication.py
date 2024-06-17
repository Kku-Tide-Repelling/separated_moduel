import time
import datetime
import pickle
import hashlib
from LoRaRF import SX127x

data_file_path = "/home/hyun/pir_repelling_moduel/data.pkl"

busId = 0; csId = 0
resetPin = 22; irqPin = 4; txenPin = -1; rxenPin = -1
LoRa = SX127x()

def configure_LoRa():
    print("Begin LoRa radio")
    if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin):
        raise Exception("Something wrong, can't begin LoRa radio")

    print("Set frequency to 920.9 MHz")
    LoRa.setFrequency(920900000)
    print("Set TX power to +17 dBm")
    LoRa.setTxPower(17, LoRa.TX_POWER_PA_BOOST)
    print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
    LoRa.setSpreadingFactor(7)
    LoRa.setBandwidth(125000)
    LoRa.setCodeRate(5)
    print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
    LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)
    LoRa.setPreambleLength(12)
    LoRa.setPayloadLength(15)
    LoRa.setCrcEnable(True)
    print("Set synchronize word to 0x34")
    LoRa.setSyncWord(0x34)

def calculate_md5(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        return hashlib.md5(content).hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def get_top_ranking(ranking):
    sorted_ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    top_ranking = sorted_ranking[:1]
    return top_ranking

def packing_data():
    with open(data_file_path, "rb") as pickle_file:
        load_data = pickle.load(pickle_file)
        loaded_data = get_top_ranking(load_data)
    message = "HeLoRa,World\0"
    messageList = list(message)
    for i in range(len(messageList)): messageList[i] = ord(messageList[i])

    gateway_id = 0xCD
    node_id = 0xAA
    detectionType = "PIR"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
    all_data = f"{gateway_id} {node_id} {message} {loaded_data} {current_time} {detectionType}"
    data = all_data.encode('utf-8')
    data_list = list(data)
    print(loaded_data)
    return data_list

def lora_tx():
    data = packing_data()
    LoRa.beginPacket()
    LoRa.write(data, len(data))
    LoRa.endPacket()
    LoRa.wait()
    print("Transmit time: {0:0.2f} ms | Data rate: {1:0.2f} byte/s\n".format(LoRa.transmitTime(), LoRa.dataRate()))
    time.sleep(1)

