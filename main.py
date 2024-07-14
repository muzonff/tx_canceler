import json
from web3 import Web3, Account


def get_user_input(prompt):
    return input(prompt)


def main():
    account = Account.create()
    token_from = account.address
    token_from_private_key = account.key.hex()

    token_to = get_user_input("Enter recipient address>> ")
    amount = int(get_user_input("Enter amount (to get real amount divide by the number of decimal)>> "))
    gas_limit = int(get_user_input("Enter gas limit>> "))
    node = get_user_input("Enter blockchain node>> ")
    gas_price_gwei = get_user_input("Enter MINIMAL gas in GWEI>> ")
    contract_address = get_user_input("Enter token contract address>> ")

    msg = f"""
==========================
Send money to pay fees on: {token_from}
Private key: {token_from_private_key} (keep it safe)
Press any button when deposited
==========================
    """
    print(msg)
    input()

    # Load the ABI
    with open("abi.json") as f:
        token_abi = json.load(f)

    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(node))
    contract = w3.eth.contract(address=contract_address, abi=token_abi)
    chain_id = w3.eth.chain_id

    # Build the transaction
    token_txn = contract.functions.transfer(
        token_to,
        amount
    ).build_transaction({
        'chainId': chain_id,
        'gas': gas_limit,
        'gasPrice': w3.to_wei(gas_price_gwei, 'gwei'),
        'nonce': 0,
    })

    signed_txn = w3.eth.account.sign_transaction(token_txn, private_key=token_from_private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(f"Transaction hash: {txn_hash.hex()}")
    txn_receipt = w3.eth.get_transaction(txn_hash)
    print(txn_receipt)


if __name__ == "__main__":
    main()
