import time
from web3 import Web3
from eth_account.messages import encode_defunct
import requests

w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))


headers = {
    'authority': 'claim.frame-api.xyz',
    'accept': '*/*',
    'accept-language': 'en,ru;q=0.9,fr;q=0.8,ru-RU;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.frame.xyz',
    'referer': 'https://www.frame.xyz/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def siga(private):
    msg = f'You are claiming the Frame Chapter One Airdrop with the following address: {address.lower()}'
    message = encode_defunct(text=msg)
    signed_message = w3.eth.account.sign_message(message, private_key=private)
    return signed_message.signature.hex()


with open("p.txt", "r") as f:
    keys_list = [row.strip() for row in f if row.strip()]
    numbered_keys = list(enumerate(keys_list, start=1))

for wallet_number, private in numbered_keys:

    try:

        account = w3.eth.account.from_key(private)
        address = account.address

        json_data = {
            'signature': siga(private),
            'address': address.lower(),
        }
        #
        response = requests.post('https://claim.frame-api.xyz/authenticate', headers=headers, json=json_data)

        if response.json()['userInfo']['totalAllocation']:
            print(f'{address}: {response.json()["userInfo"]["totalAllocation"]} tokens')
            with open('wallets_with_drop.txt', 'a') as output:
                print(f'{address}: {response.json()["userInfo"]["totalAllocation"]}', file=output)
        else:
            print(f'{address} is not eligible: {response.json()["userInfo"]["totalAllocation"]} tokens')

        time.sleep(2)

    except Exception as err:
        print(err)
        with open('privates_with_error.txt', 'a') as output:
            print(f'{private}', file=output)
