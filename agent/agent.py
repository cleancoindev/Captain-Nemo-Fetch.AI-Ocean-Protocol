from web3.auto import Web3
import time
import requests
import json



def create_ocean_request(query):
    pass

def process_response(response):
    pass

def sign_response(message):
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)
    ec_recover_args = (msghash, v, r, s) = (
        Web3.toHex(signed_message.messageHash),
        signed_message.v,
        to_32byte_hex(signed_message.r),
        to_32byte_hex(signed_message.s),
    )
    return ec_recover_args

def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))

    

def main_loop():
    length = 0
    print('starting agent main loop')
    while True:
        event_filter = contract.events.QueryCreated.createFilter(fromBlock="latest")
        
        event_filter.get_new_entries()
        
        if length < len(event_filter.get_all_entries()):
            event_args = event_filter.get_all_entries()[-1]["args"]
            query = event_args["query"]
            response = create_ocean_request(query)
            callback = event_args["callback"]
            result = process_response(response)
            updateQuery = contract.functions.updateQuery(queryhash, w3.toChecksumAddress(con_add), w3.toBytes(callback), result)
            nonce = w3.eth.getTransactionCount(account.address)  
            quert_txn = updateQuery.buildTransaction({
                'gas': 300000,
                'gasPrice': w3.toWei('1', 'gwei'),
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(quert_txn, private_key=private_key)
            w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            
            length = len(event_filter.get_all_entries())#maybe dont need this

        time.sleep(2)




if __name__ == '__main__':

    w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/4eb906a46726439288d56efaa45fc89a"))

    with open('../keystore/UTC--2019-10-19T15-13-02.082157851Z--719b682d53f15899376709fb372c98aa5a116799') as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, 'submarine')

    contract_address = '0x4B04928c8beEF8848920a8BA63176B7aB5Fc87e2'
    contractAddress = Web3.toChecksumAddress(contract_address)
    account =  w3.eth.account.privateKeyToAccount(private_key)
    w3.eth.defaultAccount = account.address

    with open("abi.json") as f:
        abi = json.load(f)

    contract = w3.eth.contract(address=contractAddress, abi=abi)
    contract.address = contractAddress 
    
    main_loop()
