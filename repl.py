from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from web3.exceptions import TransactionNotFound


def get_user_input(prompt):
    return input(prompt)


def main():
    # Get user inputs
    tx_hash = get_user_input("Enter TX hash to revert>> ")
    node = get_user_input("Enter node>> ")
    sender_priv = get_user_input("Enter sender private key>> ")
    gas_limit = int(get_user_input("Enter new gas limit>> "))
    gwei_fee = get_user_input("Enter new fee in GWEI>> ")

    w3 = Web3(Web3.HTTPProvider(node))
    own_address = w3.eth.account.from_key(sender_priv).address

    tx = {
        'from': own_address,
        'to': own_address,
        'value': 0,
        'gas': gas_limit,
        'gasPrice': w3.to_wei(gwei_fee, 'gwei'),
        'nonce': 0
    }

    account = w3.eth.account.from_key(sender_priv)
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

    try:
        res = w3.eth.replace_transaction(tx_hash, tx)
        print("Successfully replaced transaction.")
        print(f"New TX Hash: {res.hex()}")
        print(w3.eth.get_transaction(res.hex()))
    except TransactionNotFound:
        print(f"Transaction with hash {tx_hash} not found.")
    except Exception as e:
        print(f"Error replacing transaction: {e}")


if __name__ == "__main__":
    main()
