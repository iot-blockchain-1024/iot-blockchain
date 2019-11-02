from bit import PrivateKeyTestnet


def broadcast_to_blockchain(info):
    key = PrivateKeyTestnet('cNyYBxvt1BvAq3svjTZWg4LN828bzPimax2C7pipPjbUzgWYDXdp')
    output = [("n1EqLqM6ZBzErjioxXoE9QxyD87ETskFBa", 0.000001, "btc")]
    key.send(output, message=info)
    print("bitcoin testnet:" + info + " success")
