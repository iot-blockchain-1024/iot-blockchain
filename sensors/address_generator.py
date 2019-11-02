from bit import PrivateKeyTestnet

key = PrivateKeyTestnet()
print("ADDRESS:" + key.address)
print("WIF:" + key.to_wif())
print("HEX:" + key.to_hex())
